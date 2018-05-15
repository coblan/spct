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
        'USER': 'sa',
        'PASSWORD': 'cdqg@1215',
        #'PORT': '1436',
        'OPTIONS': {
            #'driver': 'ODBC Driver 11 for SQL Server',
            #'driver':'SQL Server Native Client 11.0',
            #'MARS_Connection': True,
              },
       } ,     
}

ALLOWED_HOSTS=['192.168.0.244','localhost']
DATABASE_ROUTERS = ['hello.db_router.DbRouter']

MAX_BANNER_SIZE=1024*1024*2

BANNER_UPLOAD_URL='http://103.246.219.202:9004/api/upload?folder=banner'
BANNER_ACCESS_URL='http://103.246.219.202:9004/static' 


APP_PKG_UPLOAD_URL='http://103.246.219.202:9004/api/upload?folder=package'
APP_PKG_ACCESS_URL='http://103.246.219.202:9004/static' 

#from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import SET
#SET(globals()) 
