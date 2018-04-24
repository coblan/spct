# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import ModelTable,TablePage,ModelFields,FieldsPage,page_dc,model_dc
from .models import KVModel
import cgi

class KVTable(ModelTable):
    model=KVModel
    exclude=[]
    def dict_row(self, inst):
        if len(inst.value)>50:
            value=inst.value[:50]+'...'
        else:
            value=inst.value
        return {
            'value':cgi.escape(value)
        }

class KvTablePage(TablePage):
    tableCls=KVTable

class KvFields(ModelFields):
    class Meta:
        model=KVModel
        exclude=[]

class KvFormPage(FieldsPage):
    fieldsCls=KvFields
    def get_template(self, prefer=None):
        if prefer=='wx':
            return 'wx/kvform.html'
        else:
            return 'director/kvform.html'

# short_gen.regist_director(['kv','kv.wx'],KVModel)
page_dc.update({
    'kv':KvTablePage,
    'kv.edit':KvFormPage,
})

model_dc[KVModel]={'fields':KvFields}
