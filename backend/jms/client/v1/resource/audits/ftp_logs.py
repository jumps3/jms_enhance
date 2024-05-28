from jms.client import base, mixin
from jms.client.v1.router import FTPLogRouter


class FTPLog(base.BaseResource):
    def __str__(self):
        operate = getattr(self, 'operate')
        filename = getattr(self, 'filename')
        return f'文件日志-> {filename}({operate})'

    def __repr__(self):
        return self.__str__()


class FTPLogManager(base.BaseManager,
                    mixin.NotGetUpdateDeleteMixin):
    resource_class = FTPLog

    def __init__(self, api_client):
        router = FTPLogRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()
