# -*- coding: utf-8 -*-
import requests
import urllib3

from . import authentication, utils
from . import session as jms_session

from datetime import datetime

from .exceptions import JMSException


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SessionClient(object):
    def __init__(self, session, *args, **kwargs):
        self.org_id = '00000000-0000-0000-0000-000000000002'
        self.session = session
        self.api_version = kwargs.pop('api_version', None)

    def set_org(self, org_id):
        self.org_id = org_id

    def request(self, url, method, headers=None, data=None, params=None, **kwargs):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        request_headers = {
            'X-JMS-ORG': self.org_id,
            'Accept': 'application/json',
            'Authorization': self.session.token,
            'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        }
        request_headers.update(headers)

        action = getattr(requests, method, 'get')
        resp = action(
            url, auth=self.session.access_key,
            headers=request_headers, json=data, params=params, verify=False
        )
        try:
            body = resp.json()
        except Exception:
            body = []

        if resp.status_code >= 400:
            raise JMSException(str(body) + '\n code: %s' % resp.status_code)

        return resp, body


def _construct_http_client(api_version=None,
                           auth=None,
                           auth_token=None,
                           web_url=None,
                           username=None,
                           password=None,
                           session=None,
                           **kwargs):
    if not session:
        key_id = kwargs.get('key_id')
        secret_id = kwargs.get('secret_id')
        if key_id and secret_id:
            auth = authentication.AccessKey(
                web_url=web_url,
                key_id=key_id, secret_id=secret_id
            )
        if not auth and auth_token:
            auth = authentication.Token(
                web_url=web_url,
                auth_token=auth_token
            )
        elif not auth:
            auth = authentication.Password(
                web_url=web_url,
                username=username, password=password,
            )
        session = jms_session.Session(auth=auth)

    return SessionClient(api_version=api_version,
                         auth=auth,
                         session=session,
                         **kwargs)


def _get_client_class_and_version(version):
    # 先写死，后期换成ApiVersion对象管理
    ver_major = 1
    version_list = str(version).split('.')
    # if len(version_list) > 0:
    #     ver_major = version_list[0]

    return version, utils.import_class(
        "jms.client.v%s.client.Client" % ver_major)


def client(version, username=None, password=None, web_url=None, **kwargs):
    """
    :param version: JumpServer堡垒机版本信息，如 2.15.3
    :param username: 认证用户名
    :param password: 认证密码
    :param web_url: JumpServer堡垒机网页地址，如 127.0.0.1：8080
    :param kwargs:
    :return:
    """
    if password:
        kwargs["password"] = password

    if isinstance(web_url, str) and web_url.endswith('/'):
        web_url = web_url[:-1]

    api_version, client_class = _get_client_class_and_version(version)

    return client_class(api_version=api_version,
                        web_url=web_url,
                        username=username,
                        **kwargs)
