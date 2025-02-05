import aiomysql
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.getenv('MYSQL_PORT', 3309)),
    'user': os.getenv('MYSQL_USER', 'linda_news'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DBNAME', 'linda_news')
}

async def get_db_pool():
    return await aiomysql.create_pool(
        host=MYSQL_CONFIG['host'],
        port=MYSQL_CONFIG['port'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        db=MYSQL_CONFIG['database'],
        charset='utf8mb4',
        autocommit=True
    )