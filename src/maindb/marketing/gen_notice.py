# encoding:utf-8
from __future__ import unicode_literals
from ..models import TbNotice
import json
from django.template import loader, Context
import re
import os
from django.conf import settings
from helpers.func.sim_signal import sim_signal
from ..static_html_builder import StaticHtmlBuilder
from urllib.parse import urljoin

def gen_notice_file():
    has_download_url=[]
    root_path = os.path.join(settings.MEDIA_ROOT, 'public/notice')
    
    index_url = urljoin(settings.SELF_URL, '/notice/index')
    spd = StaticHtmlBuilder(url= index_url, root_path= root_path,downloaded_urls=has_download_url)
    spd.run()
    
    index_url = urljoin(settings.SELF_URL, '/notice/index1')
    spd = StaticHtmlBuilder(url= index_url, root_path= root_path,downloaded_urls=has_download_url)
    spd.run()    
    
    
    
    for itm in TbNotice.objects.filter(status=1):
        page_url =  urljoin(settings.SELF_URL, '/notice/%s.html' % itm.pk )
        spd = StaticHtmlBuilder(url= page_url, root_path= root_path,downloaded_urls=has_download_url)
        spd.run()        
    sim_signal.send('notice.static.changed')

#def gen_notice_file1():
    #ls = []
    #for itm in TbNotice.objects.filter(status=1).order_by('-createtime'):
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
    #sim_signal.send('notice.static.changed')
    
def get_html_name(title):
    '''根据分页的名字，获取index页面里面链接到分页的url'''
    fl_name = re.search('\w+',title,re.U).group()
    return fl_name+'.html'
