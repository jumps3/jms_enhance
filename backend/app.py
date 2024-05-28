import io
import os

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS

import services.service

app_path = os.path.abspath(__file__)
static_path = os.path.join(os.path.dirname(app_path), 'static')

app = Flask(__name__, static_folder=static_path + '/dist')
# 允许跨域
CORS(app)
app.config['APP_STATIC_DIR'] = static_path


# 首页
@app.route('/')
def index():
    return app.send_static_file('index.html')

# 前端静态文件下载
@app.route('/assets/<path:filename>')
def serve_static(filename):
    return app.send_static_file(f'assets/{filename}')

# 设置堡垒机的 URL 及密钥信息
@app.route('/api/settings', methods=['POST', 'GET'])
def setting():
    if request.method.lower() == 'get':
        return jsonify({
            'jms_base_url': app.config.get('JMS_BASE_URL', ''),
            'jms_access_key': app.config.get('JMS_ACCESS_KEY', ''),
            'jms_access_secret': app.config.get('JMS_ACCESS_SECRET', '')
        })
    else:
        data = request.get_json()
        app.config['JMS_BASE_URL'] = data.get('jms_base_url')
        app.config['JMS_ACCESS_KEY'] = data.get('jms_access_key')
        app.config['JMS_ACCESS_SECRET'] = data.get('jms_access_secret')
        # 校验正确性
        try:
            # service 初始化时会查询组织等信息，可用于判断配置正确与否
            get_enhance_service()
            return jsonify({'code': 200, 'data': None})
        except Exception as e:
            return jsonify({'code': 400, 'msg': '参数错误, %s' % e})


def get_enhance_service():
    base_url = app.config['JMS_BASE_URL']
    key_id = app.config['JMS_ACCESS_KEY']
    secret_id = app.config['JMS_ACCESS_SECRET']
    s = services.service.EnhanceService(base_url=base_url, key_id=key_id, secret_id=secret_id, app_static_dir=static_path)
    return s

# 上传文件
@app.route('/api/<string:category>/upload', methods=['POST'])
def upload(category):  # put application's code here
    file = request.files['file']
    extension = os.path.splitext(file.filename)[-1][1:]
    fbs = io.BytesIO(file.read())
    s = get_enhance_service()
    try:
        action = getattr(s, f'import_{category}')
        filename = action(fbs, extension)
        return jsonify({'code': 200, 'data': {'filename': filename}})
    except Exception as e:
        return jsonify({'code': 500, 'data': {}, 'msg': str(e)})


@app.route('/api/<string:category>/tpl', methods=['GET'])
def download_template(category):
    tpl_file = f'{category}_tpl.xlsx'
    file_path = os.path.join(app.config['APP_STATIC_DIR'], 'tpl', tpl_file)
    resp = send_file(file_path, as_attachment=True)
    resp.headers["Content-Disposition"] = f"attachment; filename={tpl_file}"
    return resp


@app.route('/api/result/<string:filename>', methods=['GET'])
def download_result(filename):
    file_path = os.path.join(app.config['APP_STATIC_DIR'], 'results', filename)
    return send_file(str(file_path), as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)