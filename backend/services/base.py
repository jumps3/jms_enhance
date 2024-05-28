import io

import pandas as pd

from jms.client import client


class BaseService(object):
    def __init__(self, base_url, key_id, secret_id):
        self.jms_client = client.client(version='v3.10.0', web_url=base_url, key_id=key_id, secret_id=secret_id)
        self._init_data()

    def _init_data(self):
        self.orgs = self._get_orgs()
        self.sys_roles = self._get_roles()
        self.sys_role_user = list(filter(lambda x: x.name == 'User', self.sys_roles))[0]
        self.org_roles = self._get_roles(sys=False)
        self.org_role_user = list(filter(lambda x: x.name == 'OrgUser', self.org_roles))[0]
        self.platforms = self._get_platforms()

    def _get_roles(self, sys=True):
        return self.jms_client.sys_role.list() if sys else self.jms_client.org_role.list()

    def _get_role_ids(self, role_names=None, sys=True):
        if not role_names:
            return [self.sys_role_user.id] if sys else [self.org_role_user.id]
        else:
            ids = []
            names = role_names.split(',')
            for nm in names:
                rids = [r.id for r in self.sys_roles if r.name == nm or r.display_name == nm] if sys else [r.id for r in self.org_roles if r.name == nm or r.display_name == nm]
                ids.extend(rids)
            return ids

    def _get_orgs(self):
        return self.jms_client.organization.list()

    def _get_platforms(self):
        return self.jms_client.platform.list()

    @staticmethod
    def _read_csv(data: io.BytesIO, usecols=None) -> pd.DataFrame:
        return pd.read_csv(data, usecols=usecols)

    @staticmethod
    def _read_xlsx(data: io.BytesIO, usecols=None) -> pd.DataFrame:
        return pd.read_excel(data, usecols=usecols)

    def _read_file(self, data: io.BytesIO, file_type='xlsx', usecols=None) -> pd.DataFrame:
        action = getattr(self, f'_read_{file_type}')
        return action(data, usecols)