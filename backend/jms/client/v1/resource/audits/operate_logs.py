from jms.client import base, mixin
from jms.client.v1.router import OperateLogRouter


class OperateLog(base.BaseResource):
    def __str__(self):
        resource = getattr(self, 'resource')
        action = getattr(self, 'action')
        return f'操作日志-> {resource}({action})'

    def __repr__(self):
        return self.__str__()


class OperateLogManager(base.BaseManager,
                        mixin.NotGetUpdateDeleteMixin):
    resource_class = OperateLog

    def __init__(self, api_client):
        router = OperateLogRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()
