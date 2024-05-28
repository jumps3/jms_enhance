from jms.client import base
from jms.client.v1.router import UserGroupRouter


class UserGroup(base.BaseResource):

    def bind_attrs(self):
        attrs = [
            'name', 'comment', 'date_created', 'created_by', 'labels',
            'users_amount', 'org_id', 'org_name'
        ]
        for attr in attrs:
            setattr(self, attr, self.get_body(attr))

    def __str__(self):
        name = getattr(self, 'name')
        return f'用户组-> {name}'

    def __repr__(self):
        return self.__str__()


class UserGroupManager(base.BaseManager):
    resource_class = UserGroup

    def __init__(self, api_client):
        router = UserGroupRouter(self)
        super().__init__(api_client, router)

    def list(self, **kwargs):
        return self._list(**kwargs)

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        return self._update(resource, attribute)

    def create(self, attribute=None, resource=None):
        must_attr = ['name']
        attrs = self.get_latest_attribute(resource, attribute)

        self.required_params_check(must_attr, attrs)

        return self._create(attribute=attribute, resource=resource)

    def delete(self, resource):
        self._delete(resource)
