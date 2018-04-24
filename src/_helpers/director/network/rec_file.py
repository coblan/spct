# encoding:utf-8

from __future__ import unicode_literals

from django.http import HttpResponse
from django.conf import settings
import os
from django.utils.timezone import datetime
import json
import hashlib
import io
import urlparse
import hashlib
import re
from django.views.decorators.csrf import csrf_exempt

try:
    general_upload= os.path.join(settings.MEDIA_ROOT,'general_upload')
    os.makedirs(general_upload)
except os.error:
    pass

def general(request):
    file_dict = request.FILES
    par_path,par_dir= get_par_path() #general_upload
    file_url_list=[]
    for name, fl in file_dict.items():
        catch = io.BytesIO()
        m = hashlib.md5()        
        for chunk in fl.chunks():
            catch.write(chunk) 
            m.update(chunk)    
            
        catch.flush()
        
        fl_name =adapt_name(name)
        mt_name=re.search('\.(\w+)$',fl_name)
        if mt_name:
            file_name=m.hexdigest()+'___'+fl_name
        else:
            # 没有后缀名的img,使用md5.png的形式来标记它
            img_ext = re.search('image/(\w+)',fl.content_type)
            if img_ext:
                file_name =m.hexdigest()+'.'+img_ext.group(1)
            else:
                file_name=m.hexdigest()
        
        
        file_path=os.path.join(par_path,file_name)
        if not os.path.exists( file_path ):
            with open(file_path,'wb') as general_file:
                general_file.write(catch.getvalue())
                
        file_url=urlparse.urljoin(settings.MEDIA_URL, 'general_upload/{par_dir}/{file_name}'.format(par_dir=par_dir,file_name=file_name))
        file_url_list.append(file_url)
    
    return HttpResponse(json.dumps(file_url_list),content_type="application/json")

def get_par_path():
    today = datetime.today().date()
    today_str  = today.strftime('%Y_%m_%d')
    par_path = os.path.join(general_upload,today_str)
    try:
        os.makedirs(par_path)
    except os.error:
        pass
    return par_path,today_str

def adapt_name(fl_name):
    mt = re.search('\w+___(.+)',fl_name)
    if mt:
        return mt.group(1)
    else:
        return fl_name

#def general(request):
    #file_dict = request.FILES
    #file_dir=general_upload
    #file_url_list=[]
    #for name, fl in file_dict.items():
        #catch = io.BytesIO()
        #m = hashlib.md5()        
        #for chunk in fl.chunks():
            #catch.write(chunk) 
            #m.update(chunk)    
            
        #catch.flush()
        #mt_name=re.search('\.(\w+)$',fl.name)
        #if mt_name:
            #file_name=m.hexdigest()+'_'+fl.name
        #else:
            #img_ext = re.search('image/(\w+)',fl.content_type)
            #if img_ext:
                #file_name =m.hexdigest()+'.'+img_ext.group(1)
            #else:
                #file_name=m.hexdigest()
                
        #file_path=os.path.join(file_dir,file_name)
        #if not os.path.exists( file_path ):
            #with open(file_path,'wb') as general_file:
                #general_file.write(catch.getvalue())
                
        #file_url=urlparse.urljoin(settings.MEDIA_URL, 'general_upload/{file_name}'.format(file_name=file_name))
        #file_url_list.append(file_url)
    
    #return HttpResponse(json.dumps(file_url_list),content_type="application/json")