from jms.client import base
from jms.client.v1.router import NodeRouter


class Node(base.BaseResource):
    def __str__(self):
        # value = getattr(self, 'value')
        full_value = getattr(self, 'full_value')
        return f'资产节点-> {full_value}'

    def __repr__(self):
        return self.__str__()


class NodeManager(base.BaseManager):
    resource_class = Node

    def __init__(self, api_client):
        router = NodeRouter(self)
        super().__init__(api_client, router)

    @staticmethod
    def get_meta_id(resource):
        resource_id = resource
        if isinstance(resource, Node):
            resource_id = resource.meta['data']['id']
        return resource_id

    def list(self, **kwargs):
        return self._list(**kwargs)

    def get(self, resource):
        return self._get(resource)

    def update(self, resource, attribute=None):
        resource_id = self.get_meta_id(resource)
        return self._update(resource_id, attribute)

    def create(self, attribute=None, resource=None):
        return self._create(attribute=attribute, resource=resource)

    def delete(self, resource):
        self._delete(resource)

    def create_node_by_id(self, father_node_id, attribute):
        resource_id = self.get_meta_id(father_node_id)
        url = self.router.get_url(
            'create_node_by_id', resource_id=resource_id
        )
        resp, body = self.client.request(url, 'post', data=attribute)
        resource = self.resource_class(body)
        return resource

    def list_all(self):
        url = self.router.get_url('list_all')
        resp, body = self.client.request(url, 'get')
        resource = [self.resource_class(i) for i in body]
        return resource
