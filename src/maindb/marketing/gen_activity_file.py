# encoding:utf-8
from __future__ import unicode_literals
from ..models import TbActivity
import json
from django.template import loader, Context
import re
import os
from django.conf import settings
import re
import zipfile
from django.conf import settings

def gen_activity_file():
    ls = []
    for itm in TbActivity.objects.filter(status=1).order_by('-createtime'):
        if itm.zip:
            mt = re.search(r'([^\/\\]+).zip$',itm.zip)
            if mt:
                file_name = mt.group(0)
                zip_path = os.path.join( settings.MEDIA_ROOT,'general_upload',file_name )
                par_path = os.path.join( settings.MEDIA_ROOT,'public','activity',mt.group(1) )
                try:
                    os.makedirs(par_path)
                except:
                    pass
                
                unzip(par_path,zip_path)
                ls.append({'cover':'/static'+itm.cover,
                           'url':'%s/index.html'%mt.group(1)})
    
    index_temp = loader.get_template('maindb/activity_index.html')
    index_html = index_temp.render({'activity_list': json.dumps(ls)})
    index_path = os.path.join(settings.MEDIA_ROOT,'public','activity','index.html')
    with open(index_path,'wb') as index_file:
        index_file.write(index_html.encode('utf-8'))    

                
        
        #content_temp = loader.get_template('maindb/notice_content.html')
        #page_html = content_temp.render({'content':itm.content,'title':itm.title})
        #page_path = os.path.join(settings.MEDIA_ROOT,'public/notice/%s'%get_html_name(itm.title))
        #ls.append({'title':itm.title,
                   #'url':get_html_name(itm.title),
                   #'update_date':itm.createtime.strftime('%Y-%m-%d')})
        #with open(page_path,'wb') as page_file:
            #page_file.write(page_html.encode('utf-8'))
    
    #index_temp = loader.get_template('maindb/notice_index.html')
    #index_html= index_temp.render({'notice_list':json.dumps(ls)})
    #index_path = os.path.join(settings.MEDIA_ROOT,'public/notice/index.html')
    #with open(index_path,'wb') as index_file:
        #index_file.write(index_html.encode('utf-8'))
      
def get_html_name(title):
    '''根据分页的名字，获取index页面里面链接到分页的url'''
    fl_name = re.search('\w+',title,re.U).group()
    return fl_name+'.html'

def unzip(par_path,path):
    zip_ref = zipfile.ZipFile(path.encode('utf-8', 'r'))
    zip_ref.extractall(par_path.encode('utf-8'))
    zip_ref.close()    
    
    #zfile = zipfile.ZipFile(path,'r')
    #for filename in zfile.namelist():
        #data = zfile.read(filename)
        #file_path = os.path.join(par_path,filename)
        #file = open(file_path, 'w+b')
        #file.write(data)
        #file.close()
