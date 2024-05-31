#/bin/bash

# 1、编译前端文件并移动到后端目录中

cd frontend
# 1.1、开始下载依赖
npm install
# 1.2、开始编译 vue 代码
npm run build

# 1.3、将前端编译好的文件放入指定位置
cd ..
rm -rf backend/static/assets
mv frontend/dist/* backend/static/

# 2、后端编译
cd backend
# 2.1、开始创建 venv 虚拟环境
python -m venv .venv
source .venv/bin/activate
# 2.2、开始下载依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 2.3、开始清空打包目录
rm -rf build dist app.spec

# 3、开始打包成可执行文件
pyinstaller --onefile --name="jms_aide" -D -p ./.venv/Lib/site-packages --add-data "jms:jms" --add-data "services:services" --add-data "static:static" app.py

echo 'Finished'