from jms.client import base
from jms.client.exceptions import JMSException
from jms.client.v1.router import SystemUserRouter


class SystemUser(base.BaseResource):
    def __str__(self):
        name = getattr(self, 'name')
        username = getattr(self, 'username')
        return f'系统用户-> {name}({username})'

    def __repr__(self):
        return self.__str__()


class SystemUserManager(base.BaseManager):
    resource_class = SystemUser

    def __init__(self, api_client):
        router = SystemUserRouter(self)
        super().__init__(api_client, router)

    def list(self, **params):
        system_user_type = ('common', 'admin')
        su_type = params.get('type')

        self.contain_params_check(system_user_type, su_type, 'type')

        return self._list(**params)

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        return self._update(resource, attribute)

    def create(self, attribute=None, resource=None):
        must_attr = ('name', 'username')
        attrs = self.get_latest_attribute(resource, attribute)

        self.required_params_check(must_attr, attrs)

        return self._create(attribute=attrs, resource=resource)

    def delete(self, resource):
        self._delete(resource)

    def update_auth_info(self, resource, data):
        resource_id = self.get_id(resource)
        url = self.router.get_url('update', resource_id=resource_id)
        resp, body = self.client.request(url, 'put', data=data)
        resource = self.resource_class(body)
        return resource

    def get_auth_info(self, resource):
        resource_id = self.get_id(resource)
        url = self.router.get_url('update', resource_id=resource_id)
        resp, body = self.client.request(f'{url}auth-info/', 'get')
        resource = self.resource_class(body)
        return resource
