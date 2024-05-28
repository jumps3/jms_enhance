FROM python:3.11-slim

# 设置工作目录
WORKDIR /opt/jumpserver
# 复制整个应用程序到容器中
ADD backend .

ARG PIP_MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -i ${PIP_MIRROR} -r requirements.txt

# 暴露 Flask 应用程序的端口
EXPOSE 5000

# 设置环境变量，可选
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]