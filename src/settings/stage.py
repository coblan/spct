# encoding:utf-8
from __future__ import unicode_literals
from base import *

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
        'HOST': '103.246.219.202,1436',
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
        #'HOST': '192.168.40.79,1436',
        'HOST': '103.246.219.202,1436',
        'USER': 'sa',
        'PASSWORD': 'cdqg@1215',
        #'PORT': '1436',
        'OPTIONS': {
            #'driver': 'ODBC Driver 11 for SQL Server',
            #'driver':'SQL Server Native Client 11.0',
            #'driver': 'FreeTDS',
            #'MARS_Connection': True,
            'AUTOCOMMIT': True,
            'host_is_server': True,
            'unicode_results': True,
            'driver': 'FreeTDS',
            'extra_params': 'TDS_VERSION=8.0',            
              },
       } ,     
}

ALLOWED_HOSTS=['192.168.0.244','103.246.219.202']
DATABASE_ROUTERS = ['hello.db_router.DbRouter']

MAX_BANNER_SIZE=1024*1024*2

# 上传时，由后端服务器发起post，所以采用局域网ip
BANNER_UPLOAD_URL='http://192.168.40.103:9004/upload?folder=banner'
# 访问时由浏览器发起get，所以采用公网地址
BANNER_ACCESS_URL='http://103.246.219.202:9004/file' 

#from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import SET
#SET(globals()) 
