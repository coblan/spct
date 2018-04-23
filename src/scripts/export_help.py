#if getattr(settings,'DEV_STATUS',None)=='dev':
from __future__ import unicode_literals
import json
#import wingdbstub
from maindb.models import TbQa
import re
def export_help():
    
    sections=[]

    for itm in TbQa.objects.filter(mtype=0).order_by('-priority'):
        index_dc={'title':itm.title}
        pages=[]
        for sub_itm in TbQa.objects.filter(mtype=itm.type).order_by('-priority'):
            pages.append({'title':sub_itm.title,'description':sub_itm.description})
        index_dc['pages']=pages
        sections.append(index_dc)
    with open('scripts/help.json','wb') as f:
        json.dump(sections,f)


def gen_help():
    with open('scripts/help.json') as f:
        sections = json.load(f)
    index_section=[]
    
    # index page data
    for index_dc in sections:
        index_section.append({
            'title':index_dc['title'],
            'items':[ {'title':x['title'],
                       'url':get_html_name(x['title'])} for x in index_dc['pages'] ],
                     
        })
    # create index page
    with open('scripts/index.html') as f:
        text = f.read()
        formated_text = text %{'section_list':json.dumps(index_section)}
        with open('scripts/help/index.html','w') as index_html:
            index_html.write(formated_text)
    
    # create page
    with open('scripts/content.html') as f:
        text = f.read()   
        text = text.decode('utf-8')
        for sec in sections:
            for page in sec['pages']:
                formated_text = text %{'content':json.dumps(page),'title':page['title']}
                #print(page['title'])
                #fl_name = re.search('\w+',page['title'],re.U).group()
                with open('scripts/help/'+get_html_name(page['title']),'w') as page_html:
                    page_html.write(formated_text.encode('utf-8'))         
        
        
    
def get_html_name(title):
    fl_name = re.search('\w+',title,re.U).group()
    return fl_name+'.html'
