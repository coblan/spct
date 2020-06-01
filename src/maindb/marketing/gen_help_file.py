# encoding:utf-8
from __future__ import unicode_literals
from ..models import TbQa
import json
from django.template import loader, Context
import re
import os
from django.conf import settings
from helpers.func.sim_signal import sim_signal
from ..static_html_builder import StaticHtmlBuilder
from urllib.parse import urljoin
from maindb.models import TbMerchants

def gen_help_file(merchant): 
    index_url = urljoin(settings.SELF_URL, '/help/index.html?merchant=%s'%merchant)
    merchant_inst = TbMerchants.objects.get(pk = merchant)
    
    root_path = os.path.join(settings.MEDIA_ROOT, 'public/%s/help'%merchant_inst.merchantname)
    spd = StaticHtmlBuilder(url= index_url, root_path= root_path)
    spd.run()
    for itm in TbQa.objects.filter(status=1):
        page_url =  urljoin(settings.SELF_URL, '/help/%s.html' % itm.pk )
        spd = StaticHtmlBuilder(url= page_url, root_path= root_path)
        spd.run()        
    sim_signal.send('help.static.changed')
    

def gen_help_file1():
    """老的函数，被替换"""
    sections=[]
    
    for itm in TbQa.objects.filter(mtype=0,status=1).order_by('-priority'):
        index_dc={'title':itm.title}
        pages=[]
        for sub_itm in TbQa.objects.filter(mtype=itm.type,status=1).order_by('-priority'):
            pages.append({'title':sub_itm.title,'description':sub_itm.description})
        index_dc['pages']=pages
        sections.append(index_dc)

    index_section=[]
    
    for index_dc in sections:
        index_section.append({
            'title':index_dc['title'],
            'items':[ {'title':x['title'],
                       'url':get_html_name(x['title'])} for x in index_dc['pages'] ],
                     
            })    
        
    help_temp = loader.get_template('maindb/help_index.html')
    #t.template.origin.name # 这是home.html的绝对路径    
    #c = Context({'section_list':json.dumps(index_section) })
    index_html = help_temp.render({'section_list':json.dumps(index_section)})    
    
    # create index page
    index_path = os.path.join(settings.MEDIA_ROOT,'public/help/index.html')
    with open(index_path,'wb') as f:
        f.write(index_html.encode('utf-8'))  

    content_temp = loader.get_template('maindb/help_content.html')
    # create page

    for sec in sections:
        for page in sec['pages']:
            rendered_html = content_temp.render({'content':json.dumps(page),'title':sec['title']})
            page_html = rendered_html.encode('utf-8')
            page_path = os.path.join(settings.MEDIA_ROOT,'public/help/%s'%get_html_name(page['title']))
            with open(page_path,'wb') as page_file:
                page_file.write(page_html)  
    sim_signal.send('help.static.changed')
    
        
def get_html_name(title):
    '''根据分页的名字，获取index页面里面链接到分页的url'''
    fl_name = re.search('\w+',title,re.U).group()
    return fl_name+'.html'
