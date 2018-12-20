from django.shortcuts import render,HttpResponse
from .app_update.app_upload import AppPackageReciever
# Create your views here.
from scripts.export_help import gen_help
from .ckeditor import CusCkeditor
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from .models import TbNotice, TbQa
import re
import json
import time
from django.conf import settings
from subprocess import Popen

def test(request):
    gen_help()
    return HttpResponse('ok')

def recieve_app_pkg(request):
    key_list = list( request.FILES.keys() )
    file_name = key_list[0]
        
    rt =  AppPackageReciever().asView(request)
    if file_name.endswith('.apk'):
        arg= 'android'
    else:
        arg='ios'
    if getattr(settings,'UPLOAD_CLOUD_SHELL'):
        shell = getattr(settings,'UPLOAD_CLOUD_SHELL')
        Popen([shell,arg])
        #os.system('%(shell)s %(arg)s'%{'shell':shell,'arg':arg})
    return rt


@csrf_exempt
def recieve_ckeditor_img(request):
    return CusCkeditor().RecieveView(request)


class Notice(View):
    def get(self, request, name = None): 
        if not name or name == 'index.html':
            ls = []
            for itm in TbNotice.objects.filter(status=1).order_by('-createtime'):
                ls.append({'title':itm.title,
                           'url':  '%s.html?t=%s' % (itm.pk , int(time.time()) ), #self.get_html_name(itm.title),
                           'update_date':itm.createtime.strftime('%Y-%m-%d')})      
            return render(request, 'maindb/notice_index.html', context= {'notice_list':ls})
        else:
            real_name = name[:-5]
            page = TbNotice.objects.get(pk = real_name)
            return render(request, 'maindb/notice_content.html', context= {'content':page.content,'title':page.title})


    def get_html_name(self, title):
        '''根据分页的名字，获取index页面里面链接到分页的url'''
        fl_name = re.search('\w+',title,re.U).group()
        return fl_name+'.html'

class Help(Notice):
    def get(self, request, name = None): 
        if not name or name == 'index.html':
            index_section=[]
            for itm in TbQa.objects.filter(mtype=0,status=1).order_by('-priority'):
                index_dc={'title':itm.title}
                pages=[]
                for sub_itm in TbQa.objects.filter(mtype=itm.type,status=1).order_by('-priority'):
                    pages.append({'title':sub_itm.title,
                                  'url': '%s.html?t=%s' % (sub_itm.pk , int(time.time()) ),})
                index_dc['items']=pages
                #sections.append(index_dc)
                
                index_section.append(index_dc)
                #index_section.append({
                    #'title':itm.title,
                    #'items':[ {'title':x['title'],
                               #'url':'%s.html?t=%s' % (itm.pk , int(time.time()) )} for itm in index_dc['pages'] ],
                             
                    #})             
            return render(request, 'maindb/help_index.html', context= {'section_list': index_section})
        else:
            real_name = name[:-5]
            page = TbQa.objects.get(pk = real_name)
            return render(request, 'maindb/help_content.html', context= {'page': {'description':page.description,'title':page.title} })
    