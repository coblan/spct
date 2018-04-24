# encoding:utf-8
"""
>5>helpers/db.rst>
redis
=======
目标是全局只有一个到redis的连接::

    from helpers.db.redis_utils import redis_conn

<-<
"""
from django.conf import settings
import redis

redis_conn = None

def redis_init():
    global redis_conn
    if not isinstance(redis_conn, redis.client.StrictRedis):
        redis_conn = redis.StrictRedis(settings.REDIS_HOST,
                                       settings.REDIS_PORT,
                                       settings.REDIS_DB)
    return redis_conn

redis_init()