# encoding:utf-8

from __future__ import unicode_literals

from django.http import HttpResponse
from django.conf import settings
import os
from datetime import datetime
import json
import hashlib
import io
import urlparse
import hashlib
import re
from django.views.decorators.csrf import csrf_exempt

try:
    banners= os.path.join(settings.MEDIA_ROOT,'banners')
    os.makedirs(banners)
except os.error:
    pass

def receive_banner(request):
    file_dict = request.FILES
    file_dir=banners
    file_url_list=[]
    for name, fl in file_dict.items():
        catch = io.BytesIO()
        m = hashlib.md5()        
        for chunk in fl.chunks():
            catch.write(chunk) 
            m.update(chunk)    
            
        catch.flush()
        mt_name=re.search('\.(\w+)$',fl.name)
        if mt_name:
            file_name=m.hexdigest()+'.'+ mt_name.group(1) #'_'+fl.name
        else:
            img_ext = re.search('image/(\w+)',fl.content_type)
            if img_ext:
                file_name =m.hexdigest()+'.'+img_ext.group(1)
            else:
                file_name=m.hexdigest()
                
        file_path=os.path.join(file_dir,file_name)
        if not os.path.exists( file_path ):
            with open(file_path,'wb') as general_file:
                general_file.write(catch.getvalue())
                
        file_url=urlparse.urljoin(settings.MEDIA_URL, 'banners/{file_name}'.format(file_name=file_name))
        file_url_list.append(file_url)
    
    return HttpResponse(json.dumps(file_url_list),content_type="application/json")