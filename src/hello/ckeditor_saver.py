from helpers.director.network.ckeditor import Ckeditor
from helpers.director.shortcut import get_request_cache
from urllib.parse import urljoin
from django.conf import settings
from django.utils import timezone
import os

class StaticCkeditor(Ckeditor):
    
    def getParentPath(self):
        crt_user = get_request_cache()['request'].user
        self.today_str = timezone.now().strftime('%Y%m%d')
        if crt_user.merchant:
            self.path = 'public/%s/ckeditor/%s'%( crt_user.merchant.merchantname, self.today_str)
        else:
            self.path = 'public/ckeditor/%s'% self.today_str
        file_dir= os.path.join( settings.MEDIA_ROOT,self.path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        return file_dir
    
    def getUrl(self):
        domain =  settings.CKEDITOR_SAVER.get('static_domain')
        crt_user = get_request_cache()['request'].user
        if crt_user.merchant:
            path = '%s/ckeditor/%s'%( crt_user.merchant.merchantname, self.today_str)
        else:
            path = 'ckeditor/%s'% self.today_str
            
        file_url=urljoin(domain , '{path}/{file_name}'.format(path = path,file_name=self.file_name))
        return file_url