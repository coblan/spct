#encoding:utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse

import json

from pydoc import locate
from django.utils.translation import ugettext as _
from . import ajax
import urllib
from django.apps import apps
from helpers.func.network.ajax_router import ajax_router

"""
>5>helpers/port.rst>
总的ajax view
===============
源码路径为:director/views.ajax_views

作用是，将所有模块的ajax访问，聚集到一个url，再根据url中的app路由到不同app.ajax模块去。

该函数的url现在嵌入到了director.urls中，所以url设置为::

    from helpers.director import urls as director_urls
        url(r'^_ajax/(?P<app>\w+)?/?$',director_views.ajax_views,name='ajax_url'),
    url(r'^_ajax/?$',director_views.ajax_views), 
<-<
"""

def ajax_views(request,app=None):
    if not app:
        ajax_module = ajax
    else:
        conf= apps.get_app_config(app)
        app_dot_path=conf.module.__name__
        ajax_module=locate('%(app)s.ajax'%{'app':app_dot_path})
    try:
        return ajax_router(request, ajax_module.get_global())
    except KeyError as e:
        rt={'status':'error','msg':'key error '+str(e) +' \n may function name error'}
        return HttpResponse(json.dumps(rt),content_type="application/json")  
    

    


    