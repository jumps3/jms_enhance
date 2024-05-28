from jms.client import base
from jms.client.v1.router import AssetRouter, AssetHostRouter


class Asset(base.BaseResource):
    def __str__(self):
        name = getattr(self, 'name')
        address = getattr(self, 'address')
        return f'资产-> {name}({address})'

    def __repr__(self):
        return self.__str__()


class AssetAccount(base.BaseResource):
    def __str__(self):
        name = getattr(self, 'name')
        username = getattr(self, 'username')
        return f'资产账号-> {name}({username})'

    def __repr__(self):
        return self.__str__()


class AssetManager(base.BaseManager):
    resource_class = Asset

    def __init__(self, api_client):
        router = AssetRouter(self)
        super().__init__(api_client, router)

    def list(self, **kwargs):
        return self._list(**kwargs)

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        return self._update(resource, attribute)

    def create(self, attribute=None, resource=None):
        must_attr = ('address', 'name', 'platform')
        attrs = self.get_latest_attribute(resource, attribute)

        self.required_params_check(must_attr, attrs)

        return self._create(attribute=attribute, resource=resource)

    def delete(self, resource):
        self._delete(resource)

    def list_account(self, attribute=None):
        must_attr = ('asset',)
        self.required_params_check(must_attr, attribute)

        url = self.router.get_url('list_account')

        resp, body = self.client.request(url, 'get', params=attribute)
        resource = [AssetAccount(i) for i in body]
        return resource

    def edit_account(self, resource, attribute):
        # 修改密码(password)或者秘钥(private_key)
        resource_id = self.get_id(resource)
        attrs = self.get_latest_attribute(resource, attribute)
        url = self.router.get_url('edit_account', resource_id=resource_id)

        resp, body = self.client.request(url, 'patch', data=attrs)
        return AssetAccount(body)


class AssetHostManager(base.BaseManager):
    resource_class = Asset

    def __init__(self, api_client):
        router = AssetHostRouter(self)
        super().__init__(api_client, router)

    def list(self):
        return self._list()

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        return self._update(resource, attribute)

    def create(self, attribute=None, resource=None):
        must_attr = ('address', 'name', 'platform')
        attrs = self.get_latest_attribute(resource, attribute)

        self.required_params_check(must_attr, attrs)

        return self._create(attribute=attribute, resource=resource)

    def delete(self, resource):
        self._delete(resource)