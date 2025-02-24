import redis
import os

from dotenv import load_dotenv
load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

def getRedisConn():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def setConfBeatNum(value: int):
    client = getRedisConn()
    client.set('conf_beat_num', value)

def getConfBeatNum()->int:
    client = getRedisConn()
    value = client.get('conf_beat_num')
    return int(value) if value else 0
