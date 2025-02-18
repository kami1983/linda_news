import os
import pymysql
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def getDbConn():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', '123456'),
        database=os.getenv('MYSQL_DBNAME', 'wscn'),
        charset='utf8mb4'
    )