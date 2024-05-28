from jms.client import base
from jms.client.v1.router import AccountRouter


class Account(base.BaseResource):
    def __str__(self):
        name = getattr(self, 'name')
        username = getattr(self, 'username')
        return f'账号-> {name}({username})'

    def __repr__(self):
        return self.__str__()


class AccountManager(base.BaseManager):
    resource_class = Account

    def __init__(self, api_client):
        router = AccountRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        return self._update(resource, attribute)

    def create(self, attribute=None, resource=None):
        must_attr = ('username', 'name')
        attrs = self.get_latest_attribute(resource, attribute)

        self.required_params_check(must_attr, attrs)

        return self._create(attribute=attribute, resource=resource)

    def delete(self, resource):
        self._delete(resource)