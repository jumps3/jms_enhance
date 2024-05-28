from jms.client import base, mixin
from jms.client.v1.router import LoginLogRouter


class LoginLog(base.BaseResource):
    def __str__(self):
        username = getattr(self, 'username')
        type_display = getattr(self, 'type_display')
        return f'登录日志-> {username}({type_display})'

    def __repr__(self):
        return self.__str__()


class LoginLogManager(base.BaseManager,
                      mixin.NotGetUpdateDeleteMixin):
    resource_class = LoginLog

    def __init__(self, api_client):
        router = LoginLogRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()
