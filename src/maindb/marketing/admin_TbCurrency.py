# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,field_map,model_to_name
from helpers.director.model_func.dictfy import model_to_name
from ..models import TbCurrency
from ..status_code import *
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
        #def dict_row(self, inst):
            #return {
                #'_createuser_label':unicode( User.objects.get(pk = inst.createuser) )
            #}
        #def dict_head(self, head):
            #if head['name']=='createuser':
                #head['editor']='com-table-label-shower'
            #return head

class CurrencyForm(ModelFields):
    class Meta:
        model = TbCurrency
        exclude=[]
    #def dict_head(self, head):
        #if head['name'] =='createuser':
            #head['editor']='com-field-label-shower'  
        #return head
    
    #def save_form(self):
        #ModelFields.save_form(self)
        #if not self.instance.createuser:
            #self.instance.createuser=self.crt_user.pk
            #self.instance.save()
        #return self.instance
    
    #def dict_row(self, row):
        #return {
            #'createtime':row.createtime.strftime('%Y-%m-%d %H:%M:%S') if row.createtime else None,
            #'_createuser_label':unicode(User.objects.get(pk=row.createuser)) if row.createuser else "",
            ##'picturename':'/media/banner/'+row.picturename if row.picturename else ""
        #}    

director.update({
    'currency.table':CurrencyPage.tableCls,
    'currency.table.edit':CurrencyForm
})

page_dc.update({
    'maindb.TbCurrency':CurrencyPage,
})
