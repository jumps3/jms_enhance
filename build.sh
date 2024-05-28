#/bin/bash

# 编译前端文件并移动到后端目录中

cd frontend
# 下载依赖
npm install
# 编译 vue 代码
npm run build

cd ..
rm -rf backend/static/dist
# 将前端编译好的文件放入指定位置
mv frontend/dist backend/static/
