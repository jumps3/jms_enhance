from jms.client import base
from jms.client.v1.router import SysRoleRouter, OrgRoleRouter


class Role(base.BaseResource):

    def __str__(self):
        display_name = getattr(self, 'display_name')
        name = getattr(self, 'name')
        return f'角色-> {display_name}({name})'

    def __repr__(self):
        return self.__str__()


class SysRoleManager(base.BaseManager):
    resource_class = Role

    def __init__(self, api_client):
        router = SysRoleRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        return self._update(resource, attribute)

    def create(self, attribute=None, resource=None):
        must_attr = ('name')
        attrs = self.get_latest_attribute(resource, attribute)

        self.required_params_check(must_attr, attrs)

        return self._create(attribute=attribute, resource=resource)

    def delete(self, resource):
        self._delete(resource)


class OrgRoleManager(base.BaseManager):
    resource_class = Role

    def __init__(self, api_client):
        router = OrgRoleRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        return self._update(resource, attribute)

    def create(self, attribute=None, resource=None):
        must_attr = ('name')
        attrs = self.get_latest_attribute(resource, attribute)

        self.required_params_check(must_attr, attrs)

        return self._create(attribute=attribute, resource=resource)

    def delete(self, resource):
        self._delete(resource)
