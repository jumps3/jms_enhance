import datetime
import io
import os
import time
from urllib.parse import urljoin

import pandas as pd
import pytz
import requests
from httpsig.requests_auth import HTTPSignatureAuth

from services.base import BaseService

FAILED = '失败'
SUCCESS = '成功'


class CheckJmsConfig(object):
    def __init__(self, base_url, key_id, secret_id):
        signature_headers = ['(request-target)', 'accept', 'date']
        auth = HTTPSignatureAuth(key_id=key_id, secret=secret_id, algorithm='hmac-sha256', headers=signature_headers)
        url = urljoin(base_url, '/api/v1/orgs/orgs/?limit=1&offset=0')
        headers = {
            'Accept': 'application/json',
            'X-JMS-ORG': '00000000-0000-0000-0000-000000000000',
            'Date': datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        }
        resp = requests.get(url, auth=auth, headers=headers)
        if resp.status_code != 200:
            raise Exception(resp.text)


class EnhanceService(BaseService):
    def __init__(self, base_url, key_id, secret_id, app_static_dir):
        self.app_static_dir = app_static_dir
        super().__init__(base_url=base_url, key_id=key_id, secret_id=secret_id)
        self.user_cols = ['*昵称', '*用户名', '密码', '*邮箱', '用户组', '系统角色', '组织角色', '组织', '手机', '启用MFA', '需要更新密码', '激活', '失效日期', '组织', '备注']
        self.asset_cols = ['*名称', '*地址', '*系统平台', '账号', '私钥', '密码', '协议组', '节点路径', '激活', '组织', '备注']
        self.perm_cols = ['*名称', '用户', '用户组', '资产', '节点', '所有账号', '指定账号', '手动账号', '同名账号', '匿名账号', '连接', '上传', '下载', '删除', '复制', '粘贴', '分享','激活', '开始日期', '失效日期', '组织', '备注']

    # 检查必须字段哪些字段未填
    @staticmethod
    def _check_cols(row: pd.Series, cols: list):
        # miss_cols = []
        # for col in cols:
        #     if col.startswith('*') and not row[col]:
        #         miss_cols.append(row[col])
        miss_cols = [col for col in cols if col.startswith('*') and pd.isna(row[col])]
        return miss_cols if len(miss_cols) > 0 else None

    def _get_org_id(self, org_name, create=True):
        params = {'name': org_name}
        orgs = self.jms_client.organization.list(**params)
        if len(orgs) <= 0:
            if create:
                # 创建组织
                params['comment'] = '通过 jms_enhance 文件导入创建'
                org = self.jms_client.organization.create(params)
                return org.id
            else:
                return None
        return orgs[0].id

    def _set_org(self, org_name, create=True):
        if not org_name:
            # 组织列值为空，使用默认组织
            self.jms_client.set_org(self.jms_client.default_org)
        else:
            org_id = self._get_org_id(org_name, create)
            if org_id:
                self.jms_client.set_org(org_id)
            else:
                return '未找到名为 [%s] 的组织' % org_name
        return None

    def _check_nodes(self, node_path):
        names = self._split_commas(node_path)
        node_ids = []
        for nm in names:
            params = {'search': nm}
            nodes = self.jms_client.node.list(**params)
            if len(nodes) <= 0:
                node = self.jms_client.node.create({'full_value': nm})
                node_ids.append(node.id)
            else:
                ids = [nd.id for nd in nodes if nd.full_value == nm]
                node_ids.extend(ids)
        return node_ids

    @staticmethod
    def _get_account(account, secret, password):
        if not pd.isna(account):
            params = {
                'name': account,
                'username': account,
                'is_active': True,
                'push_now': False,
                'on_invalid': 'error',
                'privileged': True if account.lower() in ['root', 'administrator'] else False
            }
            # 私钥
            if not pd.isna(secret):
                params['secret_type'] = 'ssh_key'
                params['secret'] = secret
                params['password'] = password
            else:
                params['secret_type'] = 'password'
                params['secret'] = password
            return params
        else:
            return None

    def _get_platform(self, name):
        for pf in self.platforms:
            if pf.name.lower() == name.lower():
                return pf
        raise Exception('平台名称[%s]未找到' % name)

    def _get_protocols(self, protocolstr, platform):
        protocols = []
        if pd.isna(protocolstr):
            protocols = [{'name': p.name, 'port': p.port} for p in platform.protocols if p.default]
        else:
            ss = self._split_commas(protocolstr)
            for s in ss:
                pt = s.split("/")
                protocols.append({'name': pt[0], 'port': int(pt[1])})
        return protocols

    def _add_asset_host(self, platform, row: pd.Series):
        node_ids = self._check_nodes(row['节点路径'])
        account = self._get_account(row['账号'], row['私钥'], row['密码'])
        accounts = [account] if account else []
        protocols = self._get_protocols(row['协议组'], platform)
        is_active = False if not pd.isna(row['激活']) and row['激活'].lower() == 'no' else True
        try:
            params = {
                'accounts': accounts,
                'name': self._pure(row['*名称']),
                'address': self._pure(row['*地址']),
                'nodes': node_ids,
                'platform': {'id': platform.id,'name': platform.name},
                'protocols': protocols,
                'active': is_active,
                'comment': self._pure(row['备注'])
            }
            asset = self.jms_client.asset_host.create(params)
        except Exception as e:
            return FAILED, '资产添加失败，%s' % e
        return SUCCESS, ''

    def _add_account(self, asset_id, account, secret, password):
        try:
            account = self._get_account(account, secret, password)
            if not account:
                return SUCCESS, ''
            account['asset'] = asset_id
            self.jms_client.account.create(account)
            return SUCCESS, '账号添加成功'
        except Exception as e:
            return FAILED, '账号添加失败：%s' % e

    def _exist_asset(self, name, address):
        params = {'name': name, 'address': address}
        assets = self.jms_client.asset.list(**params)
        return assets[0] if len(assets) > 0 else None

    # 按行处理
    # ['*名称', '*地址', '*系统平台', '账号', '私钥', '密码', '协议组', '节点路径', '激活', '组织', '备注']
    def _add_asset(self, row: pd.Series):
        miss_cols = self._check_cols(row, self.asset_cols)
        if miss_cols:
            return FAILED, '参数缺失，请检查以下必填列：%s' % miss_cols

        self._set_org(self._pure(row['组织']))

        asset = self._exist_asset(self._pure(row['*名称']), self._pure(row['*地址']))
        if asset:
            # 资产存在，添加账号
            return self._add_account(asset.id, self._pure(row['账号']), self._pure(row['私钥']), self._pure(row['密码']))
        else:
            platform = self._get_platform(self._pure(row['*系统平台']))
            category = platform.category.get('value')
            action = getattr(self, f'_add_asset_{category}')
            return action(platform, row)

    def _exist_user(self, nickname, username):
        parmas = {'name': nickname, 'username': username}
        users = self.jms_client.user.list(**parmas)
        return users[0] if len(users) > 0 else None

    @staticmethod
    def _check_enable(value, enable_value='yes'):
        return not pd.isna(value) and value.lower() == enable_value

    @staticmethod
    def _pure(value, default=None):
        if pd.isna(value):
            return default if default else ''
        else:
            return value.strip()

    def _get_user_groups(self, groupstr):
        ids = []
        unexists = []
        if groupstr:
            group_names = self._split_commas(groupstr)
            for gn in group_names:
                gn = gn.strip()
                params = {'name': gn}
                groups = self.jms_client.user_group.list(**params)
                if len(groups) > 0:
                    gids = [g.id for g in groups]
                    ids.extend(gids)
                else:
                    unexists.append(gn)
        return ids, unexists

    def _get_or_create_user_groups(self, groupstr):
        if groupstr:
            ids = []
            group_names = self._split_commas(groupstr)
            for gn in group_names:
                gn = gn.strip()
                params = {'name': gn}
                groups = self.jms_client.user_group.list(**params)
                if len(groups) > 0:
                    gids = [g.id for g in groups]
                    ids.extend(gids)
                else:
                    group = self.jms_client.user_group.create(params)
                    ids.append(group.id)
            return ids
        else:
            return []

    # 按行处理
    # ['*昵称', '*用户名', '密码', '*邮箱', '用户组', '系统角色', '组织角色', '组织', '手机', '启用MFA', '需要更新密码', '激活', '失效日期', '组织', '备注']
    def _add_user(self, row: pd.Series):
        miss_cols = self._check_cols(row, self.user_cols)
        if miss_cols:
            return FAILED, '参数缺失，请检查以下必填列：%s' % miss_cols

        try:
            msg = []
            org_role_ids = self._get_role_ids(self._pure(row['组织角色']), sys=False)

            org_names = self._split_commas(self._pure(row['组织']))
            # 多组织处理
            for oname in org_names:
                # 全局搜索用户
                self.jms_client.set_org(self.jms_client.root_org)
                root_user = self._exist_user(self._pure(row['*昵称']), self._pure(row['*用户名']))

                self._set_org(oname)
                # 平台中存在用户
                if root_user:
                    user = self._exist_user(self._pure(row['*昵称']), self._pure(row['*用户名']))
                    if not user:
                        # 组织中无此用户，邀请
                        user_ids = [root_user.id]
                        self.jms_client.user.invite(user_ids, org_role_ids)
                        continue

                # 不存在用户则创建
                data = {
                    "password_strategy": "custom",
                    "password": self._pure(row['密码']),
                    "need_update_password": self._check_enable(row['需要更新密码']),
                    "mfa_level": 1 if self._check_enable(row['启用MFA']) else 0,
                    "source": "local",
                    "system_roles": self._get_role_ids(self._pure(row['系统角色'])),
                    "org_roles": org_role_ids,
                    "is_active": self._check_enable(row['激活']),
                    "date_expired": self._pure(row['失效日期']),
                    "phone":  str(self._pure(row['手机'])),
                    "name": self._pure(row['*昵称']),
                    "username": self._pure(row['*用户名']),
                    "email": self._pure(row['*邮箱']),
                    "groups": self._get_or_create_user_groups(self._pure(row['用户组'])),
                    "comment": self._pure(row['备注'])
                }
                self.jms_client.user.create(data)
            return SUCCESS, ''
        except Exception as e:
            return FAILED, '添加用户失败: %s' % e

    def _get_users(self, userstr):
        ids = []
        unexists = []
        if userstr:
            user_names = self._split_commas(userstr)
            for name in user_names:
                name = name.strip()
                params = {'name': name}
                users = self.jms_client.user.list(**params)
                if len(users) > 0:
                    gids = [g.id for g in users]
                    ids.extend(gids)
                else:
                    unexists.append(name)
        return ids, unexists

    def _get_assets(self, assetstr):
        ids = []
        unexists = []
        if assetstr:
            asset_names = self._split_commas(assetstr)
            for name in asset_names:
                name = name.strip()
                params = {'name': name}
                assets = self.jms_client.asset.list(**params)
                if len(assets) > 0:
                    gids = [g.id for g in assets]
                    ids.extend(gids)
                else:
                    unexists.append(name)
        return ids, unexists

    def _get_nodes(self, nodestr):
        ids = []
        unexists = []
        if nodestr:
            node_names = self._split_commas(nodestr)
            for name in node_names:
                name = name.strip()
                params = {'search': name}
                assets = self.jms_client.node.list(**params)
                if len(assets) > 0:
                    gids = [g.id for g in assets if g.full_value == name]
                    ids.extend(gids)
                else:
                    unexists.append(name)
        return ids, unexists

    def _get_accounts(self, row: pd.Series):
        input_accounts = {
            '@ALL': self._check_enable(row['所有账号']),
            '@SPEC': self._pure(row['指定账号']),
            '@INPUT': self._check_enable(row['手动账号']),
            '@USER': self._check_enable(row['同名账号']),
            '@ANON': self._check_enable(row['匿名账号']),
        }
        accounts = []
        for ia in input_accounts.keys():
            value = input_accounts[ia]
            if isinstance(value, bool):
                if value:
                    accounts.append(ia)
            else:
                accounts.append(ia)
                names = value.strip().split(',')
                accounts.extend(names)
        return accounts

    def _get_actions(self, row: pd.Series):
        input_actions = {
            'connect': self._check_enable(row['连接']),
            'upload': self._check_enable(row['上传']),
            'download': self._check_enable(row['下载']),
            'copy': self._check_enable(row['复制']),
            'paste': self._check_enable(row['粘贴']),
            'delete': self._check_enable(row['删除']),
            'share': self._check_enable(row['分享']),
        }
        actions = [ia for ia in input_actions.keys() if input_actions[ia]]
        return actions


    def _get_perms_date(self, start_date, end_date):
        if start_date == '':
            now = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
            # 格式化时间字符串
            start_date = now.strftime('%Y/%m/%d %H:%M:%S %z')
        if end_date == '':
            try:
                sd = datetime.datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S %z')
            except Exception as e:
                print(e)
                sd = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
            ed = sd.replace(year=sd.year+70)
            end_date = ed.strftime('%Y/%m/%d %H:%M:%S %z')
        try:
            datetime.datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S %z')
        except Exception as e:
            print(e)
            return self._get_perms_date(start_date, '')
        return start_date, end_date

    # 按行处理
    # ['*名称', '用户', '用户组', '资产', '节点', '账号', '动作', '激活', '开始日期', '失效日期', '组织', '备注']
    def _add_perm(self, row: pd.Series):
        miss_cols = self._check_cols(row, self.perm_cols)
        if miss_cols:
            return FAILED, '参数缺失，请检查以下必填列：%s' % miss_cols

        user_ids, unexists_users = self._get_users(self._pure(row['用户']))
        if len(unexists_users) > 0:
            return FAILED, '存在用户未找到，请检查用户名：%s' % unexists_users

        user_group_ids, unexists_groups = self._get_user_groups(self._pure(row['用户组']))
        if len(unexists_groups) > 0:
            return FAILED, '存在用户组未找到，请检查用户组：%s' % unexists_groups

        asset_ids, unexists_assets = self._get_assets(self._pure(row['资产']))
        if len(unexists_assets) > 0:
            return FAILED, '存在资产未找到，请检查资产名：%s' % unexists_assets

        node_ids, unexists_nodes = self._get_nodes(self._pure(row['节点']))
        if len(unexists_assets) > 0:
            return FAILED, '存在资产未找到，请检查资产名：%s' % unexists_nodes

        accounts = self._get_accounts(row)

        actions = self._get_actions(row)

        date_start, date_end = self._get_perms_date(self._pure(row['开始日期']), self._pure(row['失效日期']))
        try:
            err = self._set_org(self._pure(row['组织']), create=False)
            if err:
                return FAILED, err
            data = {
                'name': self._pure(row['*名称']),
                'users': user_ids,
                'user_groups': user_group_ids,
                'assets': asset_ids,
                'nodes': node_ids,
                'accounts': accounts,
                'protocols': ['all'],
                'actions': actions,
                'is_active': self._check_enable(self._pure(row['激活'], 'yes')),
                'date_start': date_start,
                'date_expired': date_end,
                'comment': self._pure(row['备注'])
            }
            perm = self.jms_client.asset_permission.create(data)
            return SUCCESS, ''
        except Exception as e:
            return FAILED, '创建授权失败, %s' % e

    '''
    导入用户
    用户组不存在时自动添加
    '''
    def import_users(self, data: io.BytesIO, file_type='xlsx'):
        try:
            df = self._read_file(data, file_type=file_type, usecols=self.user_cols)
        except Exception as e:
            raise e
        df[['状态', '异常']] = df.apply(self._add_user, axis=1, result_type='expand')

        # 结果保存到本地
        now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        filename = f'users-{now}.xlsx'
        df.to_excel(os.path.join(self.app_static_dir, 'results', filename), index=False)
        res = df['状态'].value_counts().to_dict()
        res['filename'] = filename
        return res

    '''
    导入资产
    资产不存在则创建，存在时添加账号
    创建资产时，组织不存在时自动创建，节点不存在时自动创建
    '''
    def import_assets(self, data: io.BytesIO, file_type='xlsx'):
        try:
            df = self._read_file(data, file_type=file_type, usecols=self.asset_cols)
        except Exception as e:
            raise e

        df[['状态', '异常']] = df.apply(self._add_asset, axis=1, result_type='expand')

        # 结果保存到本地
        now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        filename = f'assets-{now}.xlsx'
        df.to_excel(os.path.join(self.app_static_dir, 'results', filename), index=False)
        res = df['状态'].value_counts().to_dict()
        res['filename'] = filename
        return res

    # 导入授权
    def import_perms(self, data: io.BytesIO, file_type='xlsx'):
        df = self._read_file(data, file_type=file_type, header=[0, 1], usecols=self.perm_cols)
        df[['状态', '异常']] = df.apply(self._add_perm, axis=1, result_type='expand')

        # 结果保存到本地
        now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        filename = f'perms-{now}.xlsx'
        path = os.path.join(self.app_static_dir, 'results', filename)
        df.to_excel(path, index=False)
        res = df['状态'].value_counts().to_dict()
        res['filename'] = filename
        return res

