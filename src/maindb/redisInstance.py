import redis
from django.conf import settings
#192.168.40.222:6379
REDIS = settings.REDIS_SERVER
redisInst = redis.Redis(host=REDIS, port=6379, decode_responses=True,db=1)  
redisInst0 = redis.Redis(host=REDIS, port=6379, decode_responses=True,db=0)  
redisInst6 = redis.Redis(host=REDIS, port=6379, decode_responses=True,db=6)  

