from .base import *

DATABASE_ROUTERS = ['hello.db_router.DbRouter']

MAX_BANNER_SIZE=1024*1024*2


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
        'general_log':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*5,
            'backupCount':3,
            'formatter':'standard',
            'filename': os.path.join(LOG_PATH,'general_log.log'),            
            },         
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'djangoout_warning', 'mail_admins', 'elk_warning'],
            'level': 'INFO',
            },
        'general_log': {
            'handlers': ['console', 'djangoout_warning', 'elk_info','general_log' ],
            'level': 'DEBUG',
            'propagate': True,            
            },
        'ModelFields.save_form': {
            'handlers': ['operation_log', 'elk_info'],
            'level': 'DEBUG',
            'propagate': True,              
            },
        'operation_log': {
            'handlers': ['operation_log', 'elk_info'],
            'level': 'DEBUG',
            'propagate': True,               
            },
        'task': {
            'handlers': ['elk_info'],
            'level': 'DEBUG',
            'propagate': True,                 
            },             
    }
}

