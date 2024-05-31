import io
import os

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

import services.service

app_path = os.path.abspath(__file__)
static_path = os.path.join(os.path.dirname(app_path), 'static')

app = Flask(__name__, static_folder=static_path)
# 允许跨域
CORS(app)
app.config['APP_STATIC_DIR'] = static_path


# 首页
@app.route('/')
def index():
    return app.send_static_file('index.html')


# 前端静态文件下载
@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)


def get_config(key, default=None):
    return app.config.get(key, os.environ.get(key, default))


# 设置堡垒机的 URL 及密钥信息
@app.route('/api/settings', methods=['POST', 'GET'])
def setting():
    if request.method.lower() == 'get':
        return jsonify({
            'jms_base_url': get_config('JMS_BASE_URL', ''),
            'jms_access_key': get_config('JMS_ACCESS_KEY', ''),
            'jms_access_secret': get_config('JMS_ACCESS_SECRET', '')
        })
    else:
        data = request.get_json()
        app.config['JMS_BASE_URL'] = data.get('jms_base_url').strip()
        app.config['JMS_ACCESS_KEY'] = data.get('jms_access_key').strip()
        app.config['JMS_ACCESS_SECRET'] = data.get('jms_access_secret').strip()
        # 校验正确性
        try:
            # service 初始化时会查询组织等信息，可用于判断配置正确与否
            services.service.CheckJmsConfig(app.config['JMS_BASE_URL'], app.config['JMS_ACCESS_KEY'], app.config['JMS_ACCESS_SECRET'])
            return jsonify({'code': 200, 'data': None})
        except Exception as e:
            return jsonify({'code': 400, 'msg': '参数错误, %s' % e})


def get_enhance_service():
    service = app.config.get('AIDE_SERVICE', None)
    if not service:
        base_url = get_config('JMS_BASE_URL')
        key_id = get_config('JMS_ACCESS_KEY')
        secret_id = get_config('JMS_ACCESS_SECRET')
        service = services.service.EnhanceService(base_url=base_url, key_id=key_id, secret_id=secret_id, app_static_dir=static_path)
        app.config['AIDE_SERVICE'] = service
    return service


# 上传文件
@app.route('/api/<string:category>/upload', methods=['POST'])
def upload(category):  # put application's code here
    file = request.files['file']
    extension = os.path.splitext(file.filename)[-1][1:]
    fbs = io.BytesIO(file.read())
    s = get_enhance_service()
    try:
        action = getattr(s, f'import_{category}')
        res = action(fbs, extension)
        return jsonify({'code': 200, 'data': res})
    except Exception as e:
        return jsonify({'code': 500, 'data': {'exception': str(e)}})


@app.route('/api/<string:category>/tpl', methods=['GET'])
def download_template(category):
    tpl_file = f'{category}_tpl.xlsx'
    file_path = os.path.join(app.config['APP_STATIC_DIR'], 'tpl', tpl_file)
    resp = send_file(file_path, as_attachment=True)
    resp.headers["Content-Disposition"] = f"attachment; filename={tpl_file}"
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
