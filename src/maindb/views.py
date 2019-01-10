from django.shortcuts import render,HttpResponse
from .app_update.app_upload import AppPackageReciever
# Create your views here.
from scripts.export_help import gen_help
from .ckeditor import CusCkeditor
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from .models import TbNotice, TbQa,TbActivityV2
import re
import json
import time
from helpers.director.model_func.dictfy import sim_dict
from helpers.director.engine import BaseEngine

def test(request):
    gen_help()
    return HttpResponse('ok')

def recieve_app_pkg(request):
    return AppPackageReciever().asView(request)


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

class ActivityIndex(View):
    def get(self, request): 
        baseengine = BaseEngine()
        baseengine.request = self.request
        rows=[]
        for row in TbActivityV2.objects.all().order_by('sort'):
            dc= sim_dict(row)
            dc['url'] = '%s.html'%row.pk
            rows.append(dc)
        ctx = {
            'rows':rows,
            'js_config':baseengine.getJsConfig()
        }        
        return render(request,'maindb/activity_v2/index.html',context=ctx)

class Activity(View):
    def get(self, request, pk = None): 
        act = TbActivityV2.objects.get(pk=pk)
        baseengine = BaseEngine()
        baseengine.request = self.request
        
        ctx = {
            'row':sim_dict(act),
            'js_config':baseengine.getJsConfig()
        }
        template = self.get_template()
        return render(request, template,context=ctx)
    def get_template(self):
        return 'maindb/activity_v2/white_template.html'

class TestAppH5View(View):
    def get(self,request):

        baseengine = BaseEngine()
        baseengine.request = self.request
        ctx = {
            'js_config':baseengine.getJsConfig()
        }
        return render(request, 'maindb/activity_v2/h5_app_test.html',context=ctx)        
