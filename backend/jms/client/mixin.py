import inspect

from .exceptions import JMSException


class UnsupportedOperationMixin:
    @staticmethod
    def raise_unsupported_operation():
        name = inspect.stack()[1].function
        raise JMSException(f"当前操作 {name} 不被支持")


class NotListMixin(UnsupportedOperationMixin):
    def list(self, *args, **kwargs):
        self.raise_unsupported_operation()


class NotGetMixin(UnsupportedOperationMixin):
    def get(self, *args, **kwargs):
        self.raise_unsupported_operation()


class NotUpdateMixin(UnsupportedOperationMixin):
    def update(self, *args, **kwargs):
        self.raise_unsupported_operation()


class NotDeleteMixin(UnsupportedOperationMixin):
    def delete(self, *args, **kwargs):
        self.raise_unsupported_operation()


class NotGetUpdateDeleteMixin(NotGetMixin,
                              NotUpdateMixin,
                              NotDeleteMixin):
    pass


class ApplicationMixin:
    @staticmethod
    def validated_category_and_type(attrs):
        category = attrs['category']
        type = attrs['type']
        mapping = {
            'db': ['mysql', 'oracle', 'postgresql', 'mariadb'],
            'remote_app': ['chrome', 'mysql_workbench',
                           'vmware_client', 'custom'],
            'cloud': ['k8s']
        }
        if type not in mapping.get(category, []):
            mapping_str = '\n'.join([f'{k} -> {v}' for k, v in mapping.items()])
            error = f'参数 category({category}) 和参数 type ({type}) 不匹配, ' \
                    f'映射关系如下 ↓ \n{mapping_str}'
            raise JMSException(error)

    @staticmethod
    def attrs_check(attrs: dict, app_type: str):
        db_attrs = ('host', 'database')
        remote_app_attrs = ('asset',)
        mapping = {
            'mysql': db_attrs, 'oracle': db_attrs,
            'postgresql': db_attrs, 'mariadb': db_attrs,
            'k8s': ('cluster',), 'chrome': remote_app_attrs,
            'mysql_workbench': remote_app_attrs,
            'vmware_client': remote_app_attrs,
            'custom': ('assets', 'path')
        }
        for key in attrs.keys():
            if key in mapping[app_type]:
                break
        else:
            raise JMSException(f"attrs 参数必须包含 {mapping[app_type]}")

