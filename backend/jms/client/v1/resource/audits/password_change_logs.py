from jms.client import base, mixin
from jms.client.v1.router import PasswordChangeLogRouter


class PasswordChangeLog(base.BaseResource):
    def __str__(self):
        user = getattr(self, 'user')
        change_by = getattr(self, 'change_by')
        return f"改密日志-> {change_by} change {user}'s password"

    def __repr__(self):
        return self.__str__()


class PasswordChangeLogManager(base.BaseManager,
                               mixin.NotGetUpdateDeleteMixin):
    resource_class = PasswordChangeLog

    def __init__(self, api_client):
        router = PasswordChangeLogRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()
