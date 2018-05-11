# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,field_map,model_to_name
from helpers.director.model_func.dictfy import model_to_name
from ..models import TbNotice
from ..status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc

class NoticePage(TablePage):
    template='jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    
    def get_label(self):
        return '通知'
    
    def get_context(self):
        ctx = TablePage.get_context(self)
        notice_form = NoticeForm(crt_user=self.crt_user)
        ls = [
            {'name':'notice_form',
             'label':'基本信息',
             'com':'com_tab_fields',
             'get_data':{
                 'fun':'table_row',
                 #'kws':{
                    #'director_name':help_form.get_director_name(),
                    #'relat_field':'pk',              
                 #}
             },
             'after_save':{
                 'fun':'update_or_insert'
             },
             'heads': notice_form.get_heads(),
             'ops': notice_form.get_operations()                 
             },
            ]
        ctx['tabs']=ls
        return ctx        
    
    class tableCls(ModelTable):
        model=TbNotice
        exclude=['id','url']

        def dict_row(self, inst):
            return {
                '_createuser_label':unicode( User.objects.get(pk = inst.createuser) )
            }
        def dict_head(self, head):
            if head['name']=='createuser':
                head['editor']='com-table-label-shower'
            elif head['name'] =='title':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'notice_form'            
            return head
        
        def get_operation(self):
            operations= ModelTable.get_operation(self)
            operations.append({'fun':'update_notice_file','label':'更新通知文件','editor':'com-op-a',})
            return operations        
        
        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['extra_table_logic'] = 'notice_logic'
            return ctx        

class NoticeForm(ModelFields):
    class Meta:
        model = TbNotice
        exclude=[]
    def dict_head(self, head):
        if head['name'] =='createuser':
            head['editor']='com-field-label-shower'  
        elif head['name']=='content':
            head['editor']='richtext'
            head['config'] = {
                'imageUploadUrl':reverse('ckeditor_img'),
                }         
        return head
    
    def save_form(self):
        ModelFields.save_form(self)
        if not self.instance.createuser:
            self.instance.createuser=self.crt_user.pk
            self.instance.save()
        return self.instance
    
    def dict_row(self, row):
        return {
            'createtime':row.createtime.strftime('%Y-%m-%d %H:%M:%S') if row.createtime else None,
            '_createuser_label':unicode(User.objects.get(pk=row.createuser)) if row.createuser else "",
            #'picturename':'/media/banner/'+row.picturename if row.picturename else ""
        }    

director.update({
    'notice.table':NoticePage.tableCls,
    'notice.table.edit':NoticeForm
})

page_dc.update({
    'maindb.TbNotice':NoticePage,
})
