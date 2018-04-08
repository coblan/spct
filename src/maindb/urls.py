"""
"""
from django.conf.urls import include, url

import rec_file


urlpatterns = [ 
    url(r'^upload/?$',rec_file.receive_banner,name='banner_upload')
]