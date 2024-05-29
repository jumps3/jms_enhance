## JumpServer 扩展

### 关于程序
> 功能：由于 JumpServer 自带的资产导入、用户导入、授权导入对部分字段格式要求较高，导致易用性下降，所以编写此程序用于优化导入体验。
 
> 架构：jms_enhance 服务后端使用 python 的 Flask 框架，前端使用 vue 编写。

### 开发运行

- 前端打包
```shell
cd frontend
# 下载依赖
npm install
# 编译 vue 代码
npm run build 
```

- 运行服务
```shell
# 将前端编译好的文件放入指定位置
mv frontend/dist backend/static/
# 创建 venv 虚拟环境
python3 -m venv venv
source venv/bin/activate
# 下载 python 依赖
cd backend
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./requirements.txt

# 运行 flask 程序，默认监听 127.0.0.1  5000 端口
python -m flask run
```

如需修改监听地址或端口  

**1、在命令行中设置环境变量（Unix/Linux/macOS）**
```shell
# 设置监听地址
export FLASK_RUN_HOST=0.0.0.0
# 设置监听端口
export FLASK_RUN_PORT=8000
# 运行 flask 程序
python -m flask run
```
**2、在命令行中设置环境变量（Windows）**
```shell
# 设置监听地址
set FLASK_RUN_HOST=0.0.0.0
# 设置监听端口
set FLASK_RUN_PORT=8000
# 运行 flask 程序
python -m flask run
```

### 生产运行

#### 方式 1、基于 docker 
```shell
# 编译
docker buildx build --platform=linux/amd64 jms_enhance:v1.0 .
# 运行
docker run -d -p 5000:5000 --name jms_enhance jms_enhance:v1.0
```

#### 方式 2、基于可执行文件
> 基于 PyInstaller 将程序打包成 exe 文件  
> 注：不支持跨平台编译，需在对应平台上打包

```shell
# 安装 pyinstaller
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyinstaller

cd backend
# 打包, 打包文件在 dist 目录下
# windows 平台打包 exe 命令
pyinstaller --onefile --hidden-import=blinker --hidden-import=certifi --hidden-import=charset-normalizer --hidden-import=click --hidden-import=colorama --hidden-import=et-xmlfile --hidden-import=Flask --hidden-import=Flask-Cors --hidden-import=httpsig --hidden-import=idna --hidden-import=itsdangerous --hidden-import=Jinja2 --hidden-import=MarkupSafe --hidden-import=numpy --hidden-import=openpyxl --hidden-import=pandas --hidden-import=pycryptodome --hidden-import=python-dateutil --hidden-import=pytz --hidden-import=requests --hidden-import=setuptools --hidden-import=six --hidden-import=tzdata --hidden-import=urllib3 --hidden-import=Werkzeug --add-data "jms;jms" --add-data "services;services" --add-data "static;static" app.py

# MacOS 电脑打包执行文件命令
pyinstaller --onefile --hidden-import=blinker --hidden-import=certifi --hidden-import=charset-normalizer --hidden-import=click --hidden-import=colorama --hidden-import=et-xmlfile --hidden-import=Flask --hidden-import=Flask-Cors --hidden-import=httpsig --hidden-import=idna --hidden-import=itsdangerous --hidden-import=Jinja2 --hidden-import=MarkupSafe --hidden-import=numpy --hidden-import=openpyxl --hidden-import=pandas --hidden-import=pycryptodome --hidden-import=python-dateutil --hidden-import=pytz --hidden-import=requests --hidden-import=setuptools --hidden-import=six --hidden-import=tzdata --hidden-import=urllib3 --hidden-import=Werkzeug --add-data "jms:jms" --add-data "services:services" --add-data "static:static" app.py
```
双击运行 dist 目录下的可执行程序，浏览器访问 http://127.0.0.1:5000

如果需要修改端口, 修改 app.py 文件中最后一行中 port 值编译即可
```shell
app.run(host='0.0.0.0', port=5000)
```