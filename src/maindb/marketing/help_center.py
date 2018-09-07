# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,field_map,model_to_name, request_cache
from helpers.director.model_func.dictfy import model_to_name
from ..models import TbQa
from ..status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc


class HelpPage(TablePage):
    template='jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    
    def get_label(self):
        return '帮助管理'
    
    def get_context(self):
        ctx = TablePage.get_context(self)
        help_form = HelpForm(crt_user=self.crt_user)
        ls = [
            {'name':'help_form',
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
             'heads': help_form.get_heads(),
             'ops': help_form.get_operations()                 
             },
            ]
        ctx['tabs']=ls
        return ctx    
    
    class tableCls(ModelTable):
        model = TbQa
        exclude=[]
        #pop_edit_field='title'
        fields_sort=['title','mtype','status']
        
        def get_operation(self): 
            ops = super().get_operation()
            for op in ops:
                if op['name'] == 'add_new':
                    op['tab_name'] = 'help_form'
            return ops
        
        def dict_head(self, head):
            dc={
                'title':250,
                'mtype':300
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
                
            if head['name'] =='title':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'help_form'
            if head['name'] =='mtype':
                head['options'] = get_mtype_options()
                head['editor']='com-table-array-option-mapper'

            return head
        
        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['extra_table_logic'] = 'help_logic'
            return ctx
        
        #def get_operation(self):
            #operations= ModelTable.get_operation(self)
            #operations.append({'fun':'update_help_file','label':'更新帮助文件','editor':'com-op-btn',})
            #return operations
        
        class filters(RowFilter):
            names=['mtype']
            
            def dict_head(self, head): 
                if head['name'] == 'mtype':
                    head['options'] = get_mtype_options()
                return head
            #def get_options(self,name):
                #if name =='mtype':
                    #return get_mtype_options()
                #else:
                    #return RowFilter.get_options(self,name)
            

class HelpForm(ModelFields):
    field_sort=['title','status','mtype','description']
    class Meta:
        model=TbQa
        exclude=[]
    def clean_dict(self, dc):
        super().clean_dict(dc)
        if not dc.get('pk',None):
            if dc.get('mtype')==0:
                dc['type'] = len(TbQa.objects.values('mtype').distinct())
            else:
                dc['type'] = 0
            
        return dc
            
    def dict_head(self, head):
        if head['name'] =='mtype':
            head['options'] = get_mtype_options()
            head['editor']='sim_select'
        elif head['name']=='description':
            head['editor']='richtext'
            head['config'] = {
                'imageUploadUrl':reverse('ckeditor_img'),
                }            
            #head['style']="height:300px;width:450px"

        return head 

@request_cache
def get_mtype_options():
    ls =[{'value':0,'label':'顶层'}]
    for i in TbQa.objects.filter(mtype=0).order_by('-priority'):
        ls.append({'value':i.type,'label':i.title})
    return ls

director.update({
    'help.table':HelpPage.tableCls,
    'help.table.edit':HelpForm
})

page_dc.update({
    'help':HelpPage,
})