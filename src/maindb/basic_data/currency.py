# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,field_map,model_to_name
from helpers.director.model_func.dictfy import model_to_name
from maindb.models import TbCurrency
from maindb.status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director

class CurrencyPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return '金币管理'
    
    class tableCls(ModelTable):
        model=TbCurrency
        exclude=['id']
        pop_edit_field='price'

        def dict_head(self, head):
            dc={
                'description':150,
                'icon':160,
        
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head

class CurrencyForm(ModelFields):
    class Meta:
        model = TbCurrency
        exclude=[]
    def dict_head(self, head):
        if head['name'] =='icon':
            head['up_url']='/d/upload?path=public/currency'
        if head['name'] == 'price':
            head['fv_rule'] = 'integer(+);range(-2147483648~2147483647)'
        if head['name'] == 'value':
            head['fv_rule'] ='range(0.01~)'
        if head['name'] == 'description':
            head['fv_rule'] = 'length(~60)'
        return head
     

director.update({
    'currency.table':CurrencyPage.tableCls,
    'currency.table.edit':CurrencyForm
})

page_dc.update({
    'currency':CurrencyPage,
})
