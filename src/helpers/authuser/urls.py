# encoding:utf-8
from __future__ import unicode_literals
from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^login/?$',views.login,name='login'),
    url(r'^regist/?$',views.regist_user,name='regist'),
    url(r'^logout/?$',views.logout,name='logout'),
    url(r'^pswd/?$',views.change_pswd,name='change_password'),
    url(r'forget/?$',views.forget),
    ]