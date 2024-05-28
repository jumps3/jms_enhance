"""
JumpServer 所有的 API 接口映射
"""
from .. import base


class AssetRouter(base.BaseRouter):

    name = 'assets'

    @staticmethod
    def get_url_mapping():
        return {
            'assets': 'assets/assets/',
            'list_account': 'accounts/accounts/'
        }

    def list_account(self):
        url = self.url_mapping.get('list_account')
        return f"{self.host}{url}"

    def edit_account(self, resource_id):
        return f"{self.list_account()}{resource_id}/"


class AssetHostRouter(base.BaseRouter):

    name = 'assets_host'

    @staticmethod
    def get_url_mapping():
        return {
            'assets_host': 'assets/hosts/',
        }


class AccountRouter(base.BaseRouter):
    name = 'accounts'

    @staticmethod
    def get_url_mapping():
        return {
            'accounts': 'accounts/accounts/',
        }


class UserRouter(base.BaseRouter):

    name = 'users'

    @staticmethod
    def get_url_mapping():
        return {
            'users': 'users/users/',
            'invite': 'users/users/invite/'
        }

    def invite(self):
        url = self.url_mapping.get('invite')
        return f"{self.host}{url}"


class SysRoleRouter(base.BaseRouter):

    name = 'system-roles'

    @staticmethod
    def get_url_mapping():
        return {
            'system-roles': 'rbac/system-roles/',
        }


class OrgRoleRouter(base.BaseRouter):

    name = 'org-roles'

    @staticmethod
    def get_url_mapping():
        return {
            'org-roles': 'rbac/org-roles/',
        }


class SystemUserRouter(base.BaseRouter):

    name = 'system_users'

    @staticmethod
    def get_url_mapping():
        return {
            'system_users': 'assets/system-users/'
        }


class UserGroupRouter(base.BaseRouter):

    name = 'user_groups'

    @staticmethod
    def get_url_mapping():
        return {
            'user_groups': 'users/groups/'
        }


class PlatformRouter(base.BaseRouter):

    name = 'platforms'

    @staticmethod
    def get_url_mapping():
        return {
            'platforms': 'assets/platforms/'
        }


class OrganizationRouter(base.BaseRouter):

    name = 'organizations'

    @staticmethod
    def get_url_mapping():
        return {
            'organizations': 'orgs/orgs/'
        }


class DomainRouter(base.BaseRouter):

    name = 'domains'

    @staticmethod
    def get_url_mapping():
        return {
            'domains': 'assets/domains/'
        }


class CMDFilterRouter(base.BaseRouter):
    name = 'cmd_filters'

    @staticmethod
    def get_url_mapping():
        return {
            'cmd_filters': 'assets/cmd-filters/'
        }


class LabelRouter(base.BaseRouter):
    name = 'labels'

    @staticmethod
    def get_url_mapping():
        return {
            'labels': 'assets/labels/'
        }


class AssetPermissionRouter(base.BaseRouter):
    name = 'asset_permissions'

    @staticmethod
    def get_url_mapping():
        return {
            'asset_permissions': 'perms/asset-permissions/'
        }


class ApplicationPermissionRouter(base.BaseRouter):
    name = 'application_permissions'

    @staticmethod
    def get_url_mapping():
        return {
            'application_permissions': 'perms/application-permissions/'
        }


class LoginLogRouter(base.BaseRouter):
    name = 'login_logs'

    @staticmethod
    def get_url_mapping():
        return {
            'login_logs': 'audits/login-logs/'
        }


class FTPLogRouter(base.BaseRouter):
    name = 'ftp_logs'

    @staticmethod
    def get_url_mapping():
        return {
            'ftp_logs': 'audits/ftp-logs/'
        }


class OperateLogRouter(base.BaseRouter):
    name = 'operate_logs'

    @staticmethod
    def get_url_mapping():
        return {
            'operate_logs': 'audits/operate-logs/'
        }


class PasswordChangeLogRouter(base.BaseRouter):
    name = 'password_change_logs'

    @staticmethod
    def get_url_mapping():
        return {
            'password_change_logs': 'audits/password-change-logs/'
        }


class CommandExecutionLogRouter(base.BaseRouter):
    name = 'command_execution_logs'

    @staticmethod
    def get_url_mapping():
        return {
            'command_execution_logs': 'audits/command-execution-logs/'
        }


class ApplicationRouter(base.BaseRouter):
    name = 'applications'

    @staticmethod
    def get_url_mapping():
        return {
            'applications': 'applications/applications/'
        }


class NodeRouter(base.BaseRouter):
    name = 'nodes'

    @staticmethod
    def get_url_mapping():
        return {
            'nodes': 'assets/nodes/',
            'node': 'assets/nodes/',
            'create_node_by_id': 'assets/nodes/{}/children/'
        }

    def create(self):
        url = self.url_mapping.get('node')
        return f"{self.host}{url}"

    def update(self, resource_id):
        return f"{self.create()}{resource_id}/"

    def create_node_by_id(self, resource_id):
        base_url = self.url_mapping.get('create_node_by_id')
        url = base_url.format(resource_id)
        return f"{self.host}{url}"

    def list_all(self):
        url = self.url_mapping.get('node')
        return f"{self.host}{url}"
