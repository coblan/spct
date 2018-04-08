# encoding:utf-8

from django.conf.urls import include, url

from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls.static import static
import views as director_views
from helpers.director.ex_interface import rec_file



urlpatterns = [
    url(r'^ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
    url(r'^ajax/?$',director_views.ajax_views), 
    #url(r'^face/', include(face_urls)),
    url(r'^download/(?P<app>\w+)?/?$',director_views.donwload_views,name='download_url'), 
    url(r'^upload/?$',rec_file.general),  
]

