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
                           'url':  '%s.html' % itm.pk , #self.get_html_name(itm.title),
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
                               'url':self.get_html_name(x['title'])} for x in index_dc['pages'] ],
                             
                    })             
            return render(request, 'maindb/help_index.html', context= {'section_list': index_section})
        else:
            real_name = name[:-5]
            page = TbQa.objects.get(pk = real_name)
            return render(request, 'maindb/help_content.html', context= {'page': {'description':page.description,'title':page.title} })
    