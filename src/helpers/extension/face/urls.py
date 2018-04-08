"""
"""
from django.conf.urls import include, url

import ckeditor
import rec_file


urlpatterns = [ 
    url(r'^ckeditor_upload_image/?$',ckeditor.upload_image),
    url(r'^upload/?$',rec_file.general)
]

