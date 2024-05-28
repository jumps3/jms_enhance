import abc
import inspect

from urllib.parse import urlencode

from .exceptions import JMSException


class BaseResource(object):

    def __init__(self, body=None):
        self._body = body or {}
        self.id = self.get_body('id')
        self.bind_attrs()

    def get_body(self, name):
        return self._body.get(name)

    def bind_attrs(self):
        for key, value in self._body.items():
            object.__setattr__(self, key, value)

    def to_dict(self):
        return self._body

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        if key != '_body':
            self._body[key] = value


class BaseManager(object):
    resource_class = None

    def __init__(self, api_client, router):
        self.api_client = api_client
        self.host = self.api_client.web_url
        self.router = router

    @property
    def client(self):
        return self.api_client.client

    @staticmethod
    def get_id(resource):
        if isinstance(resource, BaseResource):
            resource_id = resource.id
        elif isinstance(resource, dict):
            resource_id = resource.get('id')
        else:
            resource_id = resource
        return resource_id

    @staticmethod
    def get_latest_attribute(resource, attribute):
        if attribute is None:
            attribute = {}
        elif not isinstance(attribute, dict):
            raise JMSException('资产属性 attribute 应该为字典类型')
        if isinstance(resource, BaseResource):
            attribute.update(resource.to_dict())
        return attribute

    @staticmethod
    def required_params_check(needs: tuple, params: dict):
        error_msg = '下列参数为必填项: %s' % str(needs)
        if params is None:
            raise JMSException(error_msg)

        has_all = all([params.get(a, '') for a in needs])
        if not has_all:
            raise JMSException(error_msg)

    @staticmethod
    def contain_params_check(contain_elements: tuple, param: str, tip_title=''):
        if param and param not in contain_elements:
            raise JMSException(
                f'参数错误: {tip_title} 必须为 {contain_elements} 中的一个'
            )

    @staticmethod
    def raise_exception(error):
        raise JMSException(error)

    @staticmethod
    def raise_unsupported_operation():
        name = inspect.stack()[1].function
        raise JMSException(f"当前操作 {name} 不被支持")

    def _list(self, **params):
        url = self.router.get_url('list')
        if params:
            url += '?' + urlencode(params)

        resp, body = self.client.request(url, 'get')

        resource = [self.resource_class(i) for i in body]
        return resource

    def _get(self, resource):
        resource_id = self.get_id(resource)
        url = self.router.get_url('get', resource_id=resource_id)
        resp, body = self.client.request(url, 'get')
        resource = self.resource_class(body)
        return resource

    def _update(self, resource, attribute):
        resource_id = self.get_id(resource)
        attribute = self.get_latest_attribute(resource, attribute)
        url = self.router.get_url('update', resource_id=resource_id)
        resp, body = self.client.request(url, 'patch', data=attribute)
        resource = self.resource_class(body)
        return resource

    def _create(self, attribute=None, resource=None, **params):
        attribute = self.get_latest_attribute(resource, attribute)
        url = self.router.get_url('create')
        if params:
            url += '?' + urlencode(params)

        resp, body = self.client.request(url, 'post', data=attribute)

        resource = self.resource_class(body)
        return resource

    def _delete(self, resource):
        resource_id = self.get_id(resource)
        url = self.router.get_url('delete', resource_id=resource_id)
        self.client.request(url, 'delete')


class BaseRouter(object):
    """
    JumpServer API 接口路由
    """

    name = None
    base_url = 'api/v1/'

    def __init__(self, manager):
        self.manager = manager
        self.url_mapping = self.get_url_mapping()

    @property
    def host(self):
        url = self.manager.host
        if not url.endswith('/'):
            url += '/'
        url += self.base_url
        return url

    @abc.abstractmethod
    def get_url_mapping(self):
        raise NotImplementedError()

    def get_url(self, action, **params):
        function = getattr(self, action)
        return function(**params)

    def list(self):
        url = self.url_mapping.get(self.name)
        return f"{self.host}{url}"

    def get(self, resource_id):
        url = self.url_mapping.get(self.name)
        return f"{self.host}{url}{resource_id}/"

    def update(self, resource_id):
        return self.get(resource_id)

    def create(self):
        return self.list()

    def delete(self, resource_id):
        return self.get(resource_id)
