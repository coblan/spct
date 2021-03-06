# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage, ModelTable, model_dc, page_dc, ModelFields, FieldsPage, \
    TabPage, RowSearch, RowSort, RowFilter, field_map, model_to_name, request_cache
from helpers.director.model_func.dictfy import model_to_name
from ..models import TbQa
from ..status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from helpers.director.access.permit import has_permit
from .gen_help_file import gen_help_file

class HelpPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '帮助管理'

    def get_context(self):
        ctx = TablePage.get_context(self)
        ctx['named_ctx'] = self.get_named_ctx()
        #ctx['childStore_event_slot'] = [
            #{'event': 'row.update_or_insert', 'fun': 'update_ctx', 
             #'kws': "rt={director_name:'get_mtype_options',ctx_name:'mtype_options'}",}
            ##{'event': 'row.update_or_insert', 'fun': 'update_ctx', 'ctx_name': 'mtype_options', 'director_name': 'get_mtype_options',}
        #]
            
        
        return ctx
    
    def get_named_ctx(self): 
        help_form = HelpForm(crt_user=self.crt_user)
        ls = [
            {'name': 'help_form',
             'label': '基本信息',
             'com': 'com-tab-fields',
             'get_data': {
                 'fun': 'table_row',
                 # 'kws':{
                 # 'director_name':help_form.get_director_name(),
                 # 'relat_field':'pk',
                 # }
             },
             'after_save': {
                 'fun': 'update_or_insert'
             },
             'heads': help_form.get_heads(),
             'ops': help_form.get_operations()
             },
               ]
        
        
        return {
            'helpcenter_tabs': ls,
            'mtype_options':  get_mtype_options(),
        }
    
    class tableCls(ModelTable):
        model = TbQa
        exclude=[]

        #pop_edit_field='title'
        fields_sort=['title','mtype','status','priority']
        
        #def get_operation(self):

            #ops = super().get_operation()
            #for op in ops:
                #if op['name'] == 'add_new':
                    #op['tab_name'] = 'help_form'
            #return ops

        def dict_head(self, head):
            dc = {
                'title': 250,
                'mtype': 300
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'status':
                head['editor'] = 'com-table-bool-shower'
            if head['name'] == 'title':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'help_form'
                head['ctx_name'] = 'helpcenter_tabs'
                
            if head['name'] == 'mtype':
                head['options'] = get_mtype_options()
                head['editor'] = 'com-table-array-option-mapper'

            return head

        def get_context(self):
            ctx = ModelTable.get_context(self)
            #ctx['extra_table_logic'] = 'help_logic'
            return ctx

        def get_operation(self):
            operations = ModelTable.get_operation(self)[0:1]
            add_new = operations[0]
            add_new.update({
                'tab_name': 'help_form',
                'ctx_name': 'helpcenter_tabs',
            })
            operations.extend([
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '在线',
                    'field': 'status',
                    'value': 1,
                    'row_match': 'many_row',
                    'confirm_msg': '确认修改为在线吗?', 
                    'visible': 'status' in self.permit.changeable_fields(),
                },
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '离线',
                    'field': 'status',
                    'value': 0,
                    'row_match': 'many_row',
                    'confirm_msg': '确认修改为离线吗?', 
                    'visible': 'status' in self.permit.changeable_fields(),
                },
                #{'fun': 'update_help_file', 'label': '更新缓存', 'editor': 'com-op-btn', 
                 #'visible': has_permit(self.crt_user, 'TbQa.update_cache'),}, 
                  {'fun': 'director_call', 
                   'director_name': "gen_help_static_file", 
                   'label': '更新缓存', 
                   'editor': 'com-op-btn', 
                   'visible': has_permit(self.crt_user, 'TbQa.update_cache'),}, 
            ])
            return operations
        
        @staticmethod
        def gen_help_static_file(**kws): 
            gen_help_file()
            return {'status': 'success',}

        class filters(RowFilter):
            names = ['mtype']

            def dict_head(self, head):
                if head['name'] == 'mtype':
                    head['ctx_name'] = 'mtype_options'
                    #head['ctx_field'] = 'options'
                    head['options'] = []
                    #get_mtype_options()
                    #head[] = get_mtype_options()
                    #head['director_name'] = 'get_mtype_options'
                    #head['update_options_on'] = 'row.update_or_insert'
                    
                return head
            # def get_options(self,name):
            # if name =='mtype':
            # return get_mtype_options()
            # else:
            # return RowFilter.get_options(self,name)
        class sort(RowSort):
            names = ['priority']


class HelpForm(ModelFields):
    field_sort = ['title', 'status','priority', 'mtype', 'description']

    class Meta:
        model = TbQa
        exclude = []

    def clean_dict(self, dc):
        super().clean_dict(dc)
        #if not dc.get('pk', None):
        if dc.get('mtype') == 0 :
            if dc.get('type') == 0:
                dc['type'] = len(TbQa.objects.values('type').distinct())
        else:
            dc['type'] = 0
        #else:
            #dc['type'] = 0

        return dc

    def dict_head(self, head):
        if head['name'] == 'mtype':
            head['options'] = []
            head['ctx_name'] = 'mtype_options'
            #head['options'] = get_mtype_options()
            #head['remote_options'] = 'get_mtype_options'
            head['editor'] = 'com-field-select'
            head['director_name'] = 'get_mtype_options'
            head['update_options_on'] = 'row.update_or_insert'
            
        elif head['name'] == 'description':
            head['editor'] = 'richtext'
            #head['config'] = {
                #'imageUploadUrl': reverse('ckeditor_img'),
            #}
            # head['style']="height:300px;width:450px"

        return head


@request_cache
def get_mtype_options(row = None, **kws):
    ls = [{'value': 0, 'label': '顶层'}]
    for i in TbQa.objects.filter(mtype=0).order_by('-priority'):
        ls.append({'value': i.type, 'label': i.title})
    return ls


director.update({
    'help.table': HelpPage.tableCls,
    'help.table.edit': HelpForm, 
    'get_mtype_options': get_mtype_options,
    'gen_help_static_file': HelpPage.tableCls.gen_help_static_file,
    
})

page_dc.update({
    'help': HelpPage,
})
