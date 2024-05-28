import inspect

from jms.client import base, mixin
from jms.client.v1.router import CommandExecutionLogRouter


class CommandExecutionLog(base.BaseResource):
    def __str__(self):
        command = getattr(self, 'command')
        return f'批量命令-> {command[:10]}'

    def __repr__(self):
        return self.__str__()


class CommandExecutionLogManager(base.BaseManager,
                                 mixin.NotGetUpdateDeleteMixin):
    resource_class = CommandExecutionLog

    def __init__(self, api_client):
        router = CommandExecutionLogRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()
