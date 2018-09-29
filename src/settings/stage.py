# encoding:utf-8
from __future__ import unicode_literals
from .base import *

DATABASES = {

    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    #'default': {
        #'NAME': 'BackOffice',
        #'ENGINE': 'sql_server.pyodbc',
        #'HOST': '103.246.219.202,1436',
        #'USER': 'sa',
        #'PASSWORD': 'cdqg@1215',
        ##'PORT': '1436',
        #'OPTIONS': {
            ##'driver': 'ODBC Driver 11 for SQL Server',
            ##'driver':'SQL Server Native Client 11.0',
            ##'MARS_Connection': True,
              #},
       #},
    'Betradar': {
        'NAME': 'Betradar',
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '192.168.40.79,1433',
        'USER': 'sa',
        'PASSWORD': 'cdqg@1215',
        #'PORT': '1436',
        'OPTIONS': {
            #'driver': 'ODBC Driver 11 for SQL Server',
            #'driver':'SQL Server Native Client 11.0',
            #'MARS_Connection': True,
              },
       } , 
    'MainDB': {
        'NAME': 'MainDB',
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '192.168.40.79,1433',
        #'HOST': '103.246.219.202,1436',
        'USER': 'sa',
        'PASSWORD': 'cdqg@1215',
        #'PORT': '1436',
        'OPTIONS': {
            #'driver': 'ODBC Driver 11 for SQL Server',
            #'driver':'SQL Server Native Client 11.0',
            #'driver': 'FreeTDS',
            #'MARS_Connection': True,
            
            
            'autocommit': True,
            'host_is_server': True,
            'unicode_results': True,
            'driver': 'FreeTDS',
            'extra_params': 'tds_version=8.0',
            },
       } , 
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
DATABASE_ROUTERS = ['hello.db_router.DbRouter']

MAX_BANNER_SIZE=1024*1024*2

# 下面两个地址没用了，现在采用mount路径解决了。
# 上传时，由后端服务器发起post，所以采用局域网ip
BANNER_UPLOAD_URL='http://192.168.40.103:9004/api/upload?folder=banner'
# 访问时由浏览器发起get，所以采用公网地址
BANNER_ACCESS_URL='http://103.246.219.202:9004/static' 

APP_PKG_UPLOAD_URL='http://192.168.40.103:9004/api/upload?folder=package'
APP_PKG_ACCESS_URL='http://103.246.219.202:9004/static' 

#MONGO_SERVER ="mongodb://192.168.40.104:27017,192.168.40.104:27018,192.168.40.104:27019/?replicaSet=jingbo;slaveok=true"
MONGO_SERVER ="mongodb://admin:lishen123@192.168.40.210:27017,192.168.40.211:27017,192.168.40.212:27017/?replicaSet=testrs;slaveok=true"

RABBITMQ = '192.168.40.20'
RABBITMA_PORT = '5673'
RAB_USER = 'publisher'
RAB_PSWD = 'publisher@123'

#RAB_USER = 'stageuser'
#RAB_PSWD = 'YXNkZmFmc2RmbAo'

REDIS_SERVER = '192.168.40.222'
ELASTIC = 'http://192.168.40.217:9200'

AGENT_SERVICE = 'http://192.168.40.137:8001'
CENTER_SERVICE = 'http://192.168.40.103:9022'

#from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import SET
#SET(globals()) 

import os
LOG_PATH= os.path.join( os.path.dirname(BASE_DIR),'log')

LOGGING = {
    'version': 1, # 标示配置模板版本，int 类型，目前只接收 `1`这个值。
    'disable_existing_loggers': False, 
    'formatters': {
        'standard': {
             'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'filters': {
        # 这里是定义过滤器，需要注意的是，由于 'filters' 是 logging.config.dictConfig 方法要求在配置字典中必须给订的 key ,所以即使不使用过滤器也需要明确给出一个空的结构。
    },
    'handlers': {
         'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard',
        },
        'elk_warning':{
            'level': 'ERROR',
            'class': 'hello.log_to_elastic.EsHandler',         
            }, 
        'elk_info':{
            'level': 'DEBUG',
            'class': 'hello.log_to_elastic.EsHandler',         
            },         
        'console': {
            'level':'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
            },  
        'djangoout_warning':{
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'backupCount':3,
            'formatter':'standard',
            'filename': os.path.join(LOG_PATH,'django.log'),            
            }, 
        'operation_log': {
            'level': 'INFO',
            'class': 'hello.operation_log.DBOperationHandler',
            },        
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'djangoout_warning', 'mail_admins', 'elk_warning'],
            'level': 'INFO',
            },
        #'director.sql_op': {
            #'handlers': ['console', 'elk_info'],
            #'level': 'DEBUG',
            #'propagate': True,
            #},
        'extra.error': {
            'handlers': ['console', 'djangoout_warning'],
            'level': 'DEBUG',
            'propagate': True,            
            },
        'ModelFields.save_form': {
            'handlers': ['operation_log', 'elk_info'],
            'level': 'DEBUG',
            'propagate': True,              
            },
        'task': {
            'handlers': ['elk_info'],
            'level': 'DEBUG',
            'propagate': True,                 
            },        
        #'django.request': {
            #'handlers': ['rotfile'],
            #'level': 'ERROR',
            #'propagate': True,
        #},        
    }
}

