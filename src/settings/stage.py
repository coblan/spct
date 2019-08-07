# encoding:utf-8
from __future__ import unicode_literals
from .prod_base import * 

DEBUG=False

DATABASES = {

    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    'Sports': {
        'NAME': 'Sports_20190610_Part1',#'Sports',
        'ENGINE': 'sql_server.pyodbc',
         'HOST':'192.168.40.6,1433',
          'USER': 'develop',#'Backend',
        'PASSWORD': 'develop_cheer',#'SSDEVdev@123',
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

#ALLOWED_HOSTS=['103.246.219.202', '192.168.40.116', '103.242.109.37']
ALLOWED_HOSTS = ['*']

# 静态文件服务地址
STATIC_SERVICE = 'https://static.rrystv.com'
#CLOUD_STORAGE = 'http://103.246.219.202:9004/static'  #云存储路径，用于生成plist文件的app下载路径
CLOUD_STORAGE = 'https://static.rrystv.com'
SELF_URL = 'http://192.168.40.145:9019'   # 后台系统自身的访问url，用户爬取helper，notice页面，生成静态文件

AGENT_SERVICE = 'http://192.168.40.144:8001'
#CENTER_SERVICE = 'http://192.168.40.104:9022'
CENTER_SERVICE = 'http://192.168.40.138:9022'

SPREAD_SERVICE = 'http://192.168.40.139:9030'

PHONE_MESSAGE_SERVICE = 'http://192.168.40.88:15002/message/send'
MONGO_SERVER ="mongodb://admin:lishen123@192.168.40.210:27017,192.168.40.211:27017,192.168.40.212:27017/?replicaSet=testrs;slaveok=true"

# RABBITMQ 
RABBITMQ = '192.168.40.99'
RABBITMA_PORT = '5673'
# RABBITMQ 用户密码
RAB_USER = 'publisher'
RAB_PSWD = 'publisher@123'

REDIS_SERVER = '192.168.40.222'


PRODUCT_NAME = '飞球竞猜'
PACKAGE_NAME = 'com.jingbo.flyingball'

UPLOAD_CLOUD_SHELL='/pypro/shell/upload-app.sh'




#from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import SET
#SET(globals()) 

WEBSOCKET={
    'url': "wss://mq.mv03.com/websocket",
    'user': "stageuser",
    'pswd': "YXNkZmFmc2RmbAo"
}

ELK={
    'elastic':'http://192.168.40.199:9200',
    'user':'elastic',
    'pwsd':'Nr2IFuu78CYDKR4qNask'
}

NOTICE = {
    'logo':'/media/public/manual/feiqiu.png',
    'logo_text':'飞球体育运营',
    'water_mark':'/media/public/manual/shuiyin.png',
}