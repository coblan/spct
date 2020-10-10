from .base import *

DATABASES = {

    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    
     #'default': { 
        #'ENGINE': 'sql_server.pyodbc',
        #'HOST':'192.168.40.165,1433',
        #'NAME':'BackendUserInfo_Merchant',
        ##'USER':  'develop',
        ##'PASSWORD': 'develop_cheer', 
        
        #'USER':  'develop_admin',
        #'PASSWORD': 'develop_admin_cheer123', 
        
        #'OPTIONS': {
              #},
               
       #} ,
    
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
    #'Betradar': {
        #'NAME': 'Betradar',
        #'ENGINE': 'sql_server.pyodbc',
        #'HOST': '192.168.40.79,1433',
        #'USER': 'sa',
        #'PASSWORD': 'cdqg@1215',
        ##'PORT': '1436',
        #'OPTIONS': {
              #},
       #} , 
    #'MainDB': {
        #'NAME': 'MainDB',
        #'ENGINE': 'sql_server.pyodbc',
        #'HOST': '192.168.40.79,1433',
        #'USER': 'Backend',
        #'PASSWORD': 'SSDEVdev@123',
        ##'PORT': '1436',
        #'OPTIONS': {
            ##'driver': 'ODBC Driver 11 for SQL Server',
            ##'driver':'SQL Server Native Client 11.0',
            ##'MARS_Connection': True,
              #},
        #'TEST': {
            #'NAME': 'MainDB_20180522',
            #},        
       #} ,  
    'Sports': { 
        'ENGINE': 'sql_server.pyodbc',
        
        'HOST':'192.168.40.165,1433',
        'NAME':'Sports_20190610_Part1',
        'USER':  'develop',#'Backend'  ,  
        'PASSWORD': 'develop_cheer', #'SSDEVdev@123',          
        
        #'NAME': 'Sports_Merchant', #'Sports',#'Sports', 
        #'USER':  'develop_admin',#'Backend'  ,  develop
        #'PASSWORD': 'develop_admin_cheer123', #'SSDEVdev@123',  develop_cheer
        
        #'NAME': 'Sports_20190829_Part1', #'Sports',#'Sports', 
        #'USER':  'develop_admin',#'Backend'  ,  develop
        #'PASSWORD': 'develop_admin_cheer123', #'SSDEVdev@123',  develop_cheer
        

        #'HOST':'192.168.40.166,1433',
        #'NAME':'Sports',
        #'USER':  'develop_admin',  
        #'PASSWORD': 'KKRKxZq4bRUf8kAu',  
        
        'OPTIONS': {
            #'driver': 'ODBC Driver 11 for SQL Server',
            #'driver':'SQL Server Native Client 11.0',
            #'MARS_Connection': True,
              },
               
       } ,  
    # options
    #https://pydigger.com/pypi/django-pyodbc-azure
    'Sports_nolock': { 
        'ENGINE': 'sql_server.pyodbc',
        
        'HOST':'192.168.40.165,1433',
        'NAME':'Sports_20190610_Part1',
        'USER':  'develop',#'Backend'  ,  
        'PASSWORD': 'develop_cheer', #'SSDEVdev@123',   
        
        
        #'NAME': 'Sports_Merchant', #'Sports',#'Sports', 
        #'USER':  'develop_admin',#'Backend'  ,  develop
        #'PASSWORD': 'develop_admin_cheer123', #'SSDEVdev@123',  develop_cheer
        
        
        #'NAME': 'Sports_20190829_Part1', #'Sports',#'Sports', 
        #'USER':  'develop_admin',#'Backend'  ,  develop
        #'PASSWORD': 'develop_admin_cheer123', #'SSDEVdev@123',  develop_cheer
       
        #'HOST':'192.168.40.166,1433',
        #'NAME':'Sports',
        #'USER':  'develop_admin',  
        #'PASSWORD': 'KKRKxZq4bRUf8kAu',  


        'OPTIONS': {
            'isolation_level':'READ UNCOMMITTED'
            },
               
       } ,  
    
}


ALLOWED_HOSTS=['*']
DATABASE_ROUTERS = ['hello.db_router.DbRouter']

MAX_BANNER_SIZE=1024*1024*2

# 下面两个地址没用了，现在采用mount路径解决了。
BANNER_UPLOAD_URL='http://103.246.219.202:9004/api/upload?folder=banner'
BANNER_ACCESS_URL='http://103.246.219.202:9004/static' 

APP_PKG_UPLOAD_URL='http://103.246.219.202:9004/api/upload?folder=package'
APP_PKG_ACCESS_URL='http://103.246.219.202:9004/static' 

# 各种服务地址
STATIC_SERVICE = 'https://static.rrystv.com'
CLOUD_STORAGE = 'http://103.246.219.202:9004/static'



AGENT_SERVICE = 'http://192.168.40.144:8001'
#CENTER_SERVICE = 'http://192.168.40.104:9022'
CENTER_SERVICE = 'http://192.168.40.138:9022'

SPREAD_SERVICE = 'http://192.168.40.139:9030'
PHONE_MESSAGE_SERVICE = 'http://192.168.40.88:15002/message/send'
#MONGO_SERVER = "mongodb://192.168.40.104:27017"
#MONGO_SERVER ="mongodb://192.168.40.104:27017,192.168.40.104:27018,192.168.40.104:27019/?replicaSet=jingbo;slaveok=true"
MONGO_SERVER ="mongodb://admin:lishen123@192.168.40.210:27017,192.168.40.211:27017,192.168.40.212:27017/?replicaSet=testrs;slaveok=true"


REDIS_SERVER = '192.168.40.222'

ELK={
    'elastic':'http://192.168.40.199:9200',
    'user':'elastic',
    'pwsd':'Nr2IFuu78CYDKR4qNask'
}

SELF_URL = 'http://localhost:8000'

RABBITMQ = '192.168.40.99'
RABBITMA_PORT = '5673'
RAB_USER = 'stageuser'
RAB_PSWD = 'YXNkZmFmc2RmbAo'

RABBIT_FORWORD={
    'ip':'61.220.213.93',
    'port':'5672',
    'username':'angela',
    'password':'baby123',
    'virtual_host':'uat'
}


BET_DATA_SOURCE=2

INSPECT_DICT_STATIC = 'D:\work\sportscenter\src\index.py'

#from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import SET
#SET(globals()) 

#MIDDLEWARE_CLASSES += ['django_cprofile_middleware.middleware.ProfilerMiddleware']


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
            'handlers': ['console', 'djangoout_warning', 'mail_admins','elk_warning' ],
            'level': 'INFO',
            },
        #'director.sql_op': {
            #'handlers': ['console', ],
            #'level': 'DEBUG',
            #'propagate': True,
            #},
        'general_log': {
            'handlers': ['console', 'djangoout_warning'],
            'level': 'DEBUG',
            'propagate': True,            
            },
        'ModelFields.save_form': {
            'handlers': ['console', 'operation_log'],
            'level': 'DEBUG',
            'propagate': True,              
            },
        'task': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,                 
            },
        'operation_log': {
            'handlers': ['operation_log','console'],
            'level': 'DEBUG',
            'propagate': True,               
            },        
        'requests': {
            'handlers': ['console'],
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


WEBSOCKET={
    'url': "wss://mq.mv03.com:50443/websocket",
    'user': "stageuser",
    'pswd': "YXNkZmFmc2RmbAo"
}

NOTICE = {
    'logo':'/media/public/manual/feiqiu.png',
    'logo_text':'飞球体育运营',
    'water_mark':'/media/public/manual/shuiyin.png',
}

#OPEN_SECRET = True
OPEN_SECRET = False


#JPUSH = {
    #'zq':{
          #'app_key': '28ee0a4aae701e01d974bce6',
          #'master_secret' : '38fa20f39645037ce2eb6667',
          #'ios_production':False,
          #'proxy':{
              ##'https': 'http://1sapa_proxy006.ccxdd.com:61111',
              #},
    #},
    #'fq':{
        #'app_key': '28ee0a4aae701e01d974bce6',
          #'master_secret' : '38fa20f39645037ce2eb6667',
          #'ios_production':False,
          #'proxy':{
              ##'https': 'http://1sapa_proxy006.ccxdd.com:61111',
              #},
    #}
#}

DES3_KEY= '3E35EB83050243D589482F2E'

CKEDITOR_SAVER = {
    'class':'hello.ckeditor_saver.StaticCkeditor',
    'static_domain':'https://static.rrystv.com',
}

MERCHANT = {
    'zq':{
        'jpush':{
             'app_key': '28ee0a4aae701e01d974bce6',
             'master_secret' : '38fa20f39645037ce2eb6667',
             'ios_production':False,
             'proxy':{
                 #'https': 'http://1sapa_proxy006.ccxdd.com:61111',
              },
        },
        'PRODUCT_NAME' : '追球竞猜',
        'PACKAGE_NAME' : 'com.jingbo.DQGuess',
        
    },
    'fq':{
        'jpush':{
             'app_key': '28ee0a4aae701e01d974bce6',
             'master_secret' : '38fa20f39645037ce2eb6667',
             'ios_production':False,
             'proxy':{
                 #'https': 'http://1sapa_proxy006.ccxdd.com:61111',
              },
        },
        'PRODUCT_NAME' : '飞球竞猜',
        'PACKAGE_NAME' : 'com.jingbo.DQGuess',
        
    }
}

ADMIN_USER_CHECK_IP = False