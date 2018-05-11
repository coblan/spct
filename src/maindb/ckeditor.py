from helpers.director.network.ckeditor import Ckeditor
from django.conf import settings
import os
import urlparse

class CusCkeditor(Ckeditor):
    def getParentPath(self):
        file_dir= os.path.join(settings.MEDIA_ROOT,'public','ckeditor')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return file_dir
    
    def getUrl(self):
        file_url='/static/ckeditor/{file_name}'.format(file_name=self.file_name)
        return file_url
    