python3.10.11

安装

pip install -r requirements.txt

pip install pymysql

pip install pytz

python pre_start.py

启动

set ENV=development
uvicorn main:app --reload


http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc
