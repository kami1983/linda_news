import os
import pymysql
from dotenv import load_dotenv

from libs.constants import CONST_DB_PUBLIC_LABEL_CSV_LABEL_NAME

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

def getPublicLabel(label):
    conn = getDbConn()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM linda_public_label WHERE label = %s", (label,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return None
    
def updatePublicLabel(label, value):
    conn = getDbConn()
    cursor = conn.cursor()
    try:
        # 使用 INSERT ... ON DUPLICATE KEY UPDATE 语法
        cursor.execute("""
            INSERT INTO linda_public_label (label, value) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE value = VALUES(value)
        """, (label, value))
        conn.commit()
    except Exception as e:
        print(f"Error updating label: {e}")
    finally:
        cursor.close()

def getScvLabel()->int:
    result = getPublicLabel(CONST_DB_PUBLIC_LABEL_CSV_LABEL_NAME)
    if result:
        return int(result)
    else:
        return 0
