@echo off

echo 1、编译前端文件并移动到后端目录中
cd frontend
echo 1.1、开始下载前端依赖
call npm install
echo 1.2、开始编译 vue 代码
call npm run build

echo 1.3、将前端编译好的文件放入指定位置
cd ..
rmdir /s /q backend\static\dist
move frontend\dist\* backend\static\

echo 2、开始后端编译
cd backend
echo 2.1、开始创建 venv 虚拟环境
call python -m venv .venv
call .venv\Scripts\activate
echo 2.2、开始下载依赖
call pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo 2.3、开始清空打包目录
rmdir /s /q build dist app.spec

echo 3、开始打包成可执行文件
call pyinstaller --onefile --name="jms_aide" -D -p .\.venv\Lib\site-packages --add-data "jms;jms" --add-data "services;services" --add-data "static;static" app.py

echo 打包完成！