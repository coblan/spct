# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,field_map,model_to_name
from helpers.director.model_func.dictfy import model_to_name
from ..models import TbActivity
from ..status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc

class ActivityPage(TablePage):
    template='jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    
    def get_label(self):
        return '活动'
    
    class tableCls(ModelTable):
        pop_edit_field='id'
        model = TbActivity
        exclude=[]
        
        def dict_head(self, head):
            dc={
                'cover':190,
                'zip':160,
                'createuser':80,
                'createtime':150,
            
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
                
            if head['name'] =='createuser':
                head['editor']='com-table-label-shower'   
            return head
        
        def dict_row(self, row):
            return {
                'createtime':row.createtime.strftime('%Y-%m-%d %H:%M:%S') if row.createtime else None,
                '_createuser_label':str(User.objects.get(pk=row.createuser)) if row.createuser else "",
            }  
        
        def get_operation(self):
            operations = ModelTable.get_operation(self)
            operations.append({
                'fun':'update_activity_file',
                'label':'更新活动页面',
                'editor':'com-op-btn'
            })
            return operations
        
        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['extra_table_logic'] = 'activity_logic'
            return ctx        
        
class ActiveForm(ModelFields):
    class Meta:
        model = TbActivity
        exclude=[]
    
    def save_form(self):
        ModelFields.save_form(self)
        if not self.instance.createuser:
            self.instance.createuser=self.crt_user.pk
            self.instance.save()
        return self.instance   

    def dict_row(self, row):
        return {
            'createtime':row.createtime.strftime('%Y-%m-%d %H:%M:%S') if row.createtime else None,
            '_createuser_label':str(User.objects.get(pk=row.createuser)) if row.createuser else "",
        }   
    
    def dict_head(self, head):
        #if head['name']=='cover':
            #head['editor'] = 'picture'
        if head['name'] == 'zip':
            head['editor'] = 'com-field-plain-file'
            head['config']={
                'multiple':False,
                'accept':'.zip',
                #'upload_url':reverse('app_pkg_upload')
            }          
        elif head['name'] =='createuser':
            head['editor']='com-field-label-shower'  
            
        return head

director.update({
    'activity.table':ActivityPage.tableCls,
    'activity.table.edit':ActiveForm,
})


page_dc.update({
    'maindb.TBActive':ActivityPage,
    
})