# encoding:utf-8
from __future__ import unicode_literals
from .prod_base import * 

DATABASES = {

    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    'Sports': {
        'NAME': 'Sports',
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '192.168.40.79,1433',
        'USER': 'sa',
        'PASSWORD': 'cdqg@1216',
        #'PORT': '1436',
        'OPTIONS': {
             
            'autocommit': True,
            'host_is_server': True,
            'unicode_results': True,
            'driver': 'FreeTDS',
            'extra_params': 'tds_version=8.0',
              },
               
       } ,       
}

ALLOWED_HOSTS=['103.246.219.202', '192.168.40.116', '103.242.109.37']

# 静态文件服务地址
STATIC_SERVICE = 'http://103.246.219.202:9004/static'
AGENT_SERVICE = 'http://192.168.40.137:8001'
CENTER_SERVICE = 'http://192.168.40.103:9022'
SPREAD_SERVICE = 'http://192.168.40.103:9030'

MONGO_SERVER ="mongodb://admin:lishen123@192.168.40.210:27017,192.168.40.211:27017,192.168.40.212:27017/?replicaSet=testrs;slaveok=true"

# RABBITMQ 
RABBITMQ = '192.168.40.20'
RABBITMA_PORT = '5673'
# RABBITMQ 用户密码
RAB_USER = 'publisher'
RAB_PSWD = 'publisher@123'

REDIS_SERVER = '192.168.40.222'
ELASTIC = 'http://192.168.40.217:9200'

PHONE_MESSAGE_SERVICE = 'http://192.168.40.137:5002/message/send'

