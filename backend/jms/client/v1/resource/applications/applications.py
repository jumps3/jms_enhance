from jms.client import base, mixin
from jms.client.v1.router import ApplicationRouter


class Application(base.BaseResource):

    def __str__(self):
        name = getattr(self, 'name')
        type_display = getattr(self, 'type_display')
        return f'{name}({type_display})'

    def __repr__(self):
        return self.__str__()


class ApplicationManager(base.BaseManager,
                         mixin.ApplicationMixin):
    resource_class = Application

    def __init__(self, api_client):
        router = ApplicationRouter(self)
        super().__init__(api_client, router)
        self.category_list = ('db', 'remote_app', 'cloud')

    def list(self, **params):
        category_list = tuple(self.category_list)
        category = params.get('category')

        self.contain_params_check(category_list, category, 'category')
        return self._list(**params)

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        return self._update(resource, attribute)

    def create(self, attribute=None, resource=None, **params):
        must_attr = ('name', 'category', 'type', 'attrs')
        attrs = self.get_latest_attribute(resource, attribute)

        self.validated_category_and_type(attrs)
        self.required_params_check(must_attr, attrs)
        self.attrs_check(attrs['attrs'], attrs['type'])

        return self._create(attribute=attribute, resource=resource,
                            type=attrs['type'], **params)

    def delete(self, resource):
        self._delete(resource)
