import inspect

from .client import client

# c.assets.list()

# 变量注解: c -> 客户端, assets -> 资源管理器, list -> 操作类型
# 资源管理器有：
# assets(资产)、 system_users(系统用户)、domains(网域)、cmd_filters(命令过滤)、platform(平台)、labels(标签)
# users(用户)、user_groups(用户组)、application(应用)
# organizations(组织)

# c = client(
#     version='2.15.3', web_url='web_url',
#     username='username', password='password',
#     # key_id='8ac60d35-a129-45c0-b26f-3ee8141b180d',
#     # secret_id='7f1daee1-e34d-4238-922f-b8151a44b05a'
# )

# 获取资产列表
# assets = c.asset.list()
# print(assets)

# # 获取单个资产, 参数可以为资产id，也可以为资产对象
# c.asset.get('asset_id' or 'asset_object')

# # 更新资产信息
# c.asset.update('asset_id' or 'asset_object', {'ip': '2.2.2.2'})

# 删除资产
# a = c.asset.delete('asset_id' or 'asset_object')

# 新建资产
# attribute = {'ip': '1.1.1.1', 'hostname': 'test_asset', 'platform': 'Linux'}
# a = c.asset.create(attribute=attribute)

# 获取用户列表
# users = c.user.list()

# 获取单个用户, 参数可以为资源(用户)id，也可以为资产对象(用户)
# user = c.user.get('asset_id' or 'asset_object')

# 更新用户信息
# 其中第一个参数既可以为资源id，也可以为获取的资源对象
# user = c.user.update(users[1], {'name': 'hello'})

# 新建用户
# 第一种方式，直接传递属性
# attribute = {'name': 'dong', 'username': 'dong', 'email': 'dong@qq.com'}
# user = c.user.create(attribute=attribute)
# 第二种方式，构建User对象
# from jms_client.v1.resource.users import User
# user = User()
# user.name = 'dong'
# user.username = 'dong'
# user.email = 'dong@qq.com'
# user = c.user.create(resource=user)

# 删除用户
# c.user.delete('asset_id' or 'asset_object')

#
# res = c.application.list(category='remote_app')
# c.application.update(res[0], attribute={'name': 'coudnell'})

# res = c.ftp_log.list()
# print(res)
# res = c.operate_log.list()
# print(res)
# res = c.password_change_log.list()
# print(res)
# res = c.command_execution_log.list()
# print(res)
# attribute = {'name': 'chrome2mysql', 'type': 'mysql', 'category': 'db'}
# res = c.application_permission.create(attribute=attribute)
# res = c.application_permission.get(res[0])
# res = c.application_permission.delete(res[0])
# print(res[0].to_dict())

from string import ascii_letters
from random import sample

# c = client(
#     version='2.15.3', web_url='http://10.1.13.205',
#     username='admin', password='adminadmin',
# )
# print(res)
# c.application.update(res[0], attribute={'name': 'coudnell'})

# # 生成拥有10个随机字符串元素的列表，充当node名字
# random_nodes = [''.join(sample(ascii_letters, 10)) for i in range(10)]
#
# # 获取所有的一级节点，默认有default节点
# node_list = c.node.list()
#
# for node in random_nodes:
#     # 构建子节点的属性，这里只需要一个名称
#     attribute = {'value': node}
#     # 把随机node加入到default节点下
#     new_node = c.node.create_node_by_id(node_list[0], attribute)
#     print('新节点创建成功，信息: {}\n'.format(new_node.to_dict()))


# c = client(
#     version='2.15.3', web_url='http://10.1.13.205',
#     username='admin', password='adminadmin',
# )
import time


def check_system_user_has_auth(su):
    password = getattr(su, 'password')
    private_key = getattr(su, 'private_key')
    return bool(password) or bool(private_key)


c = client(
    version='2.15.3', web_url='https://10.200.193.23',
    username='admin', password='f2c@2022',
)

# const_attr = {"protocol": "ssh", "username_same_with_user": False, "login_mode": "auto", "auto_generate_key": False,
#               "auto_push": False, "sudo": "/bin/whoami", "shell": "/bin/bash", "su_enabled": False, "priority": 81,
#               "sftp_root": "tmp"}
# c.set_org('00000000-0000-0000-0000-000000000000')
# c.set_org('3b411154-7ce0-485a-8e06-75766d861f93')
# username = 'centos'
# attr = {
#     'name': 'ddd', 'username': username, 'home': f'/home/{username}/bbb',
#     'private_key': "-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAst3c7eh8W1GM04cFLxlwJt6x9gde6Y4qa01k8W8mujSiMRCx\n4Alz8yKGFCUq/uM2OYvdIUU/kUvZW0OYmpaXxP5pWwN6WKTN39A2RM0Y2Rf77G+R\n3qfrPIcJLXogU8Nje+yw/kYsNwkVmhmXYK2W0lw2QzSFHcRQPa1qV1s8HIXXXxRg\ni32hDFuhwPulivueCFFb1gc+zw56SuhxymEvyWNHUm/ee0kzvrzQx4EGr4blMJjx\nTfA7nZP+RasrzMOVaw37P/mwy7lJynkl7vPwkDadxDpMappafa4hDPPYRr64R/Yz\n7AXvAuk8WZWGHacRgQCJtuh7jeYrdy5BPvnk+QIDAQABAoIBAGMCRon2t+eAk7h/\nM9JnfVo2yUGLwPD9feOZmre+NCy8d887E4sVEHbUdG1wSYV/1gMytXv2LgLKfo1z\nNGTV2Tr1LPJxUWcCCufKBFA/S3LYQN4WwCMExkTh5qWixYQ4UrhFQ4/s3gq0351G\nbzHXxPW6j1rSFqFsipIpjQS//t02F3k3pXrjP9+QDgGHZpNrK/wPkrjcimNgl98D\nzyqPkjOCu55OhEPF9yICq+5mHKUZpybRYjau2Y4qNKaeSwPrsnDR3t8HQLyKk5yx\nIqJbgNQSF8Mj2Sq0P4SgHxZwtdW/snI6E8Msy3sMiJwt4OfNLXQPmNPkWPTsMN7W\nXyeQVwECgYEA5qioU7Ufp5mXJjvKOvNZPgxTWsueJ02CzroA+A8ycjxNHsQM0stW\nM3b2tTXYCCBkZri6h9D+fQ6C1AYcGL/4FzWXfXSCr0DEocVwBQOwRf40/+ZKRp9L\nneBBpgpHW9XUdVs3IQ+hdB8IiasJu774vmow1+qdMO8AVCUwy1wR/CECgYEAxoSJ\nX5Mhtf5aDgBhhZ03zqIu6pcCM6RinKTFeXl6e55luuoKMkPNTBW21lAb7anikIfF\nZTt6UfuNmV+G0g4jQYt55Rtz9YplX6vcSYx0f4UM8awI2Kl1zT3et91Llkl06Y0A\nvpRhf1gW1xqjjNnOwYFgOdQpRYuBMPSpejg9jdkCgYBBtZ5ualTgPCMRI0tTS+wK\nfxxn60Xc0HoJRnfsMvgeDwuxTgyRKJggBS33JaWrev7fPJT3CBTXr4CZwjvS2S1l\n/0Bu3vgz0PGzXDmzU/+tkOOsWwCh6dNy4GYTVS5K/TmPTTMBWiCWohiej3kwYREf\nvcS4Xf/15sBjOE0UQeBlwQKBgAi5SlAo5xJYWxzCZ4a3ofwypF0qxa3/S1YW55au\n//Luwwmzvz72O89cJOzGGHQZQxuW29XXB0kTBOX4jLQuat42guTOkAn6SvopU0To\nJzZzYl48cScUS1j5nw/1aZzxHXImACJf4uj1tgs94HIQIEXgqZng+O9Vchf0qH32\ner4BAoGAfWqLMUbwImLUIc0v4Yptl3rZjs0/djmBiTqQkeLpUCA1OgQS8PdEE+s2\nflc3aotD8qxO/tkL2HJr6Y4uknq6jLRn3PgNHX7dTFIx33Bz/CkPP29LLknM9FAP\n6kM8T50Pqcc/FnnhjU2YTUTGl6/B0bsgPgFHXhqfmfCQjqDk3co=\n-----END RSA PRIVATE KEY-----",
#     'password': '', 'comment': 'test ddd'
# }
# attr.update(const_attr)
# su = c.system_user.create(attr)
# res = c.system_user.get_auth_info(su.id)
# res = c.system_user.get_auth_info('d2bc6af6-21e3-41eb-aaf2-7ab255b0c821')
# print(res.to_dict())

# data = {
#     'private_key': attr['private_key'], 'name': attr['name'], 'password': 'root'
# }
# c.system_user.update_auth_info('4d5a6668-786b-48f9-a7dd-7c425fc0b5c4', data)
# su = c.system_user.create(attr)
# url1 = f'https://10.200.193.23/api/v1/assets/system-users/{su.id}/assets/d9b3edbb-0e0d-4b96-96b3-2a44bb4b6ce1/auth-info/'
# url2 = f'https://10.200.193.23/api/v1/assets/system-users/{su.id}/auth-info/'
# print(url1)
# print(url2)
# for i in range(1, 11):
#     new_su = c.system_user.get_auth_info(su)
#     res = check_system_user_has_auth(new_su)
#     if not check_system_user_has_auth(new_su):
#         data = {
#             'private_key': attr['private_key'], 'name': attr['name']
#         }
#         c.system_user.update_auth_info(su, data)
#         print(f'重置密码{i}次')
#     else:
#         break

# c.asset_permission.create({
#     'name': f"test perm",
#     'assets': ['d9b3edbb-0e0d-4b96-96b3-2a44bb4b6ce1'], 'user_groups': ['aa2a09d1-2a00-461c-b0c3-9ec398c306c5'],
#     'system_users': [su.id]
# })


c.set_org('00000000-0000-0000-0000-000000000000')
res = c.user.list()
for u in res:
    c.user.delete(u)
    print(f'{u} delete.')

res = c.asset.list()
for u in res:
    c.asset.delete(u)
    print(f'{u} delete.')

res = c.user_group.list()
for u in res:
    c.user_group.delete(u)
    print(f'{u} delete.')

res = c.asset_permission.list()
for u in res:
    c.asset_permission.delete(u)
    print(f'{u} delete.')

res = c.system_user.list()
for u in res:
    c.system_user.delete(u)
    print(f'{u} delete.')

res = c.organization.list()
for u in res:
    if u.name != 'Default':
        c.organization.delete(u)
        print(f'{u} delete.')


# org_list = c.organization.list()
# for org in org_list:
#     c.set_org(org.id)
#     for asset in c.asset.list():
#         c.asset.delete(asset)
#
#     for platform in c.platform.list():
#         try:
#             c.platform.delete(platform)
#         except Exception as err:
#             # print(err)
#             pass
#     c.set_org()
#     try:
#         c.organization.delete(org)
#     except Exception as err:
#         print(err)


# res = c.application.list(category='remote_app')
#
# attribute = {
#     "type": "chrome", "name": "'$test'", "category": "remote_app",
#     "attrs": {
#         "path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
#         "chrome_username": "admin", "chrome_password": "123456",
#         "asset": "a4e7528f-224c-441c-a84c-95894c061e6d", "chrome_target": "'$test'"
#     }
# }
# c.application.create(attribute=attribute)
