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
}


DATABASE_ROUTERS = ['hello.db_router.DbRouter']

MAX_BANNER_SIZE=1024*1024*1

#from helpers.maintenance.debug.debug_toolbar.debugtoolbar_setting import SET
#SET(globals()) 
