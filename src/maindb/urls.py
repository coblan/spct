"""
"""
from django.conf.urls import include, url

import rec_file
import views


urlpatterns = [ 
    url(r'^upload/?$',rec_file.receive_banner,name='banner_upload'),
    url(r'^app_upload/?$',views.recieve_app_pkg,name='app_pkg_upload'),
]