"""
"""
from django.conf.urls import include, url

#from . import  rec_file
from . import views


urlpatterns = [ 
    #url(r'^upload/?$',rec_file.receive_banner,name='banner_upload'),
    url(r'^app_upload/?$',views.recieve_app_pkg,name='app_pkg_upload'),
    url(r'^ckeditor_img/?$',views.recieve_ckeditor_img,name='ckeditor_img')
]