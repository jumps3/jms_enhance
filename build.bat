@echo off

echo 1������ǰ���ļ����ƶ������Ŀ¼��
cd frontend
echo 1.1����ʼ����ǰ������
call npm install
echo 1.2����ʼ���� vue ����
call npm run build

echo 1.3����ǰ�˱���õ��ļ�����ָ��λ��
cd ..
rmdir /s /q backend\static\dist
move frontend\dist\* backend\static\

echo 2����ʼ��˱���
cd backend
echo 2.1����ʼ���� venv ���⻷��
call python -m venv .venv
call .venv\Scripts\activate
echo 2.2����ʼ��������
call pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo 2.3����ʼ��մ��Ŀ¼
rmdir /s /q build dist app.spec

echo 3����ʼ����ɿ�ִ���ļ�
call pyinstaller --onefile --name="jms_aide" -D -p .\.venv\Lib\site-packages --add-data "jms;jms" --add-data "services;services" --add-data "static;static" app.py

echo �����ɣ�