from jms.client import client
from jms.client.v1.resource import (
    assets, users, permissions, audits, applications,
    xpack
)


class Client(object):
    """
    访问 JumpServer 资源客户端
    """
    def __init__(self,
                 api_version=None,
                 auth=None,
                 auth_token=None,
                 web_url=None,
                 username=None,
                 password=None,
                 session=None,
                 timeout=None,
                 **kwargs):
        self.root_org = '00000000-0000-0000-0000-000000000000'
        self.default_org = '00000000-0000-0000-0000-000000000002'
        self.web_url = web_url
        # 用户类资源管理器
        self.user = users.UserManager(self)
        self.user_group = users.UserGroupManager(self)
        self.sys_role = users.SysRoleManager(self)
        self.org_role = users.OrgRoleManager(self)
        # 资产类资源管理器
        self.asset = assets.AssetManager(self)
        self.asset_host = assets.AssetHostManager(self)
        self.platform = assets.PlatformManager(self)
        self.domain = assets.DomainManager(self)
        self.system_user = assets.SystemUserManager(self)
        self.account = assets.AccountManager(self)
        self.cmd_filter = assets.CMDFilterManager(self)
        self.label = assets.LabelManager(self)
        self.node = assets.NodeManager(self)
        # 应用类型资源管理器
        self.application = applications.ApplicationManager(self)
        # 授权类资源管理器
        self.asset_permission = permissions.AssetPermissionManager(self)
        self.application_permission = permissions.ApplicationPermissionManager(self)
        # 日志审计类资源管理器
        self.login_log = audits.LoginLogManager(self)
        self.ftp_log = audits.FTPLogManager(self)
        self.operate_log = audits.OperateLogManager(self)
        self.password_change_log = audits.PasswordChangeLogManager(self)
        self.command_execution_log = audits.CommandExecutionLogManager(self)
        # X-Pack类资源管理器
        self.organization = xpack.OrganizationManager(self)

        self.client = client._construct_http_client(
            api_version=api_version,
            auth=auth,
            auth_token=auth_token,
            web_url=web_url,
            username=username,
            password=password,
            session=session,
            timeout=timeout,
            **kwargs
        )

    def set_org(self, org_id='00000000-0000-0000-0000-000000000000'):
        self.client.set_org(org_id)
