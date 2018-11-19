from django.shortcuts import render,HttpResponse
from .app_update.app_upload import AppPackageReciever
# Create your views here.
from scripts.export_help import gen_help
from .ckeditor import CusCkeditor
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from .models import TbNotice
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