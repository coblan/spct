# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from django.contrib import admin

# Register your models here.
from helpers.director.shortcut import page_dc,FormPage,\
     TablePage,ModelTable,ModelFields,model_dc,RowFilter,permit_list,has_permit,ModelPermit,RowFilter
from .models import DakaRecord
from django.utils import timezone
import json

class DakaMain(object):
    def __init__(self,request):
        pass
    
    def get_context(self):
        return {
            'app':'map_daka',
            'page_label':'地图打卡'
        }
    
    def get_template(self,prefer=None):
        if prefer=='f7':
            return 'map_daka/main.html'
        else:
            pass

class DakaForm(ModelFields):
    class Meta:
        model=DakaRecord
        exclude=[]

class DakaRecordFilter(RowFilter):
    model=DakaRecord
    range_fields=[{'name':'create_time','type':'date'}]

class DakaRecordTable(ModelTable):
    model=DakaRecord
    filters=DakaRecordFilter
    exclude=[]
    
    def dict_row(self, inst):
        tm = timezone.localtime(inst.create_time)
        return {
            '_label':unicode(tm),
            'pos':json.loads(inst.pos)
        }

class DakaRecordTablePage(TablePage):
    tableCls=DakaRecordTable
    template='map_daka/daka_record_f7.html'
    
    def get_label(self):
        return  unicode(self.crt_user)+'的打卡记录'
    
    
model_dc[DakaRecord]={'fields':DakaForm}
permit_list.append(DakaRecord)

page_dc.update({
    'map_daka.map.f7':DakaMain,
    'map_daka.dakarecord.f7':DakaRecordTablePage
})