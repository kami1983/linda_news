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


def addCsvRecord(csv_label, update_date):
    conn = getDbConn()
    cursor = conn.cursor()
    try:
        # 检查是否存在相同的记录 csv_label 是否存在存在更新否则插入
        cursor.execute("""
            INSERT INTO linda_csv_record (csv_label, update_date) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE update_date = VALUES(update_date)
        """, (csv_label, update_date))
        conn.commit()
    except Exception as e:
        print(f"Error adding CSV record: {e}")
    finally:
        cursor.close()
