import io
import os

from services import service


def test_import_users(base_url, key_id, secret_id):
    filepath = 'static/tpl/users.xlsx'
    extension = os.path.splitext(filepath)[-1][1:]
    s = service.EnhanceService(base_url=base_url, key_id=key_id, secret_id=secret_id)
    # s.read_file(filepath)
    with open(filepath, 'rb') as f:
        fio = io.BytesIO(f.read())
    s.import_users(fio, file_type=extension)


def test_import_assets(base_url, key_id, secret_id):
    filepath = 'static/tpl/hosts.xlsx'
    extension = os.path.splitext(filepath)[-1][1:]
    s = service.EnhanceService(base_url=base_url, key_id=key_id, secret_id=secret_id)
    # s.read_file(filepath)
    with open(filepath, 'rb') as f:
        fio = io.BytesIO(f.read())
    s.import_assets(fio, file_type=extension)


def test_import_perms(base_url, key_id, secret_id):
    filepath = 'static/tpl/perms.xlsx'
    extension = os.path.splitext(filepath)[-1][1:]
    s = service.EnhanceService(base_url=base_url, key_id=key_id, secret_id=secret_id)
    # s.read_file(filepath)
    with open(filepath, 'rb') as f:
        fio = io.BytesIO(f.read())
    s.import_perms(fio, file_type=extension)


if __name__ == '__main__':
    base_url = 'https://jumps3.fit2cloud.com/'
    key_id = 'c06004bb-732a-493b-9fa7-740ecd8c6a58'
    secret_id = 'xu6gFtSQaonGTFMYUfRMUQLGfBwZglYFwzpl'
    # jms_client = client.client(version='v3.10.9', web_url=base_url, key_id=key_id, secret_id=secret_id)
    #
    # jms_client.set_org(jms_client.default_org)
    # organizations = jms_client.asset.list_account({'asset': 'f910acfe-5da7-4477-bbb2-691aea8fcef4', 'search': 'root'})
    # print(organizations)

    test_import_users(base_url, key_id, secret_id)

    # test_import_assets(base_url, key_id, secret_id)

    # test_import_perms(base_url, key_id, secret_id)