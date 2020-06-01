# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage, ModelTable, model_dc, page_dc, ModelFields, FieldsPage, \
    TabPage, RowSearch, RowSort, RowFilter, field_map, model_to_name, request_cache,Fields
from helpers.director.model_func.dictfy import model_to_name
from ..models import TbQa,TbMerchants
from ..status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from helpers.director.access.permit import has_permit
from .gen_help_file import gen_help_file
from hello.merchant_user import get_user_merchantid,MerchantInstancCheck


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

        ls = [
             {
                 'name':'help_form',
                 'label':'基本信息',
                 'com':'com-tab-fields-v1',
                 'init_express':''' ex.vueAssign(scope.row,scope.vc.par_row)
                    if(!scope.vc.par_row.pk){
                         var par = scope.ps.parents.slice(-1)[0]; 
                         ex.vueAssign(scope.row,{mtype:par.value,})
                     }
                 ''',
                 'fields_ctx':HelpForm().get_head_context(),
             }
            ]
        
        
        return {
            'helpcenter_tabs': ls,
            #'mtype_options':  get_mtype_options(),
        }
    
    class tableCls(ModelTable):
        model = TbQa
        exclude=[]

        #pop_edit_field='title' 
        fields_sort=['merchant','title','status','priority','op']  # 'mtype',
        
        #def get_operation(self):

            #ops = super().get_operation()
            #for op in ops:
                #if op['name'] == 'add_new':
                    #op['tab_name'] = 'help_form'
            #return ops
        
        def getExtraHead(self):
            return [
                {'name':'op','label':'操作',
                 'editor':'com-table-ops-cell',
                 'fields_ctx':HelpForm().get_head_context(),
                  'ops':[
                     {
                         'editor':'com-op-plain-btn',
                         'label':'编辑',
                         'class':'btn btn-primary btn-xs',
                         'action':"""scope.ps.switch_to_tab({ctx_name:'helpcenter_tabs',tab_name:'help_form',par_row:scope.row})"""}
                     #'action':"""var fctx=scope.head.fields_ctx;[fctx.row,fctx.ops_loc]=[scope.row,"bottom"];cfg.pop_vue_com('com-form-one',fctx).then(row=>{ex.vueAssign(scope.row,row)}) """}
                     
                     ],}
            ]
        
        def inn_filter(self, query):
            if has_permit(self.crt_user,'-i_am_merchant'):
                query = query.filter(merchant_id = get_user_merchantid(self.crt_user))
                
            if self.kw.get('_par',0) >0:
                query= query.filter(mtype = self.kw.get('_par')) 
            else:
                query= query.filter(mtype = 0)
            return query
        
        def getParents(self):
            ls =[]
            par_pk = self.kw.get('_par',0)
            if par_pk > 0 :
                parent = TbQa.objects.get(type = par_pk)
                ls.append({'value':parent.type,'label':str(parent)})
                #if parent.type !=0:
                    #parent = parent.parent
                #else:
                    #break
                
            ls.append({'value':0,'label':'根目录'})
            ls.reverse()
            return ls

        def dict_head(self, head):
            dc = {
                'title': 250,
                'mtype': 300,
                'priority':150,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'status':
                head['editor'] = 'com-table-bool-shower'
                
            #if head['name'] == 'title':
                #head['editor'] = 'com-table-switch-to-tab'
                #head['tab_name'] = 'help_form'
                #head['ctx_name'] = 'helpcenter_tabs'
            
            if head['name'] == 'title':
                head['editor'] = 'com-table-click'
                head['width'] = 200
                head['action'] ='if(scope.row.type==0){cfg.toast("没有子目录了,只能有两级帮助!")}else{scope.ps.search_args._par = scope.row.type;scope.ps.search()}'
                
            #if head['name'] == 'mtype':
                #head['options'] = get_mtype_options()
                #head['editor'] = 'com-table-array-option-mapper'

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
                'init_express':'alert("bb")'
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
                  #{'fun': 'director_call', 
                   #'director_name': "gen_help_static_file", 
                   #'label': '更新缓存', 
                   #'editor': 'com-op-btn', 
                   #'visible': has_permit(self.crt_user, 'TbQa.update_cache'),}, 
                  
                  {'action':'cfg.show_load(); ex.director_call("gen_help_static_file",{merchant:%s}).then(()=>{cfg.hide_load()})'%self.crt_user.merchant.id if self.crt_user.merchant else '',
                   'label': '更新缓存', 
                   'editor': 'com-op-btn', 
                   'visible': has_permit(self.crt_user, 'TbQa.update_cache') and self.crt_user.merchant }, 
                   
                   
                  {'action':'cfg.pop_vue_com("com-local-form-one",scope.head.fields_ctx).then(resp=>{cfg.show_load(); return ex.director_call("gen_help_static_file",resp.row)}).then(()=>{cfg.hide_load()})',
                   'fields_ctx':{'title':'选择一个商户', **MerchantSelect().get_head_context()},
                   'label': '更新缓存', 
                   'editor': 'com-op-btn', 
                   'visible': has_permit(self.crt_user, 'TbQa.update_cache') and not self.crt_user.merchant }, 
            ])
            return operations
        
        @staticmethod
        def gen_help_static_file(merchant): 
            gen_help_file(merchant)
            return {'status': 'success',}

        #class filters(RowFilter):
            #names = ['mtype']

            #def dict_head(self, head):
                #if head['name'] == 'mtype':
                    #head['ctx_name'] = 'mtype_options'
                    ##head['ctx_field'] = 'options'
                    #head['options'] = []
                    ##get_mtype_options()
                    ##head[] = get_mtype_options()
                    ##head['director_name'] = 'get_mtype_options'
                    ##head['update_options_on'] = 'row.update_or_insert'
                    
                #return head
            ## def get_options(self,name):
            ## if name =='mtype':
            ## return get_mtype_options()
            ## else:
            ## return RowFilter.get_options(self,name)
        class sort(RowSort):
            names = ['priority']

class MerchantSelect(Fields):
    def get_heads(self):
        return [
            {'label':'商户','name':'merchant','editor':'com-field-select','required':True,
             'options':[
                {'value':x.pk ,'label':str(x)} for x in TbMerchants.objects.all()
            ]}
        ]

class HelpForm(MerchantInstancCheck,ModelFields):
    @property
    def field_sort(self):
        if has_permit(self.crt_user,'-i_am_merchant'):
            return ['title', 'status','priority',  'description']
        else:
            return ['merchant','title', 'status','priority',  'description'] # 'mtype',
    
    class Meta:
        model = TbQa
        exclude = []

    def clean_dict(self, dc):
        super().clean_dict(dc)
        if has_permit(self.crt_user,'-i_am_merchant'):
            dc['merchant'] = get_user_merchantid(self.crt_user)
        
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
            #head['ctx_name'] = 'mtype_options'
            #head['editor'] = 'com-field-select'
            #head['director_name'] = 'get_mtype_options'
            #head['update_options_on'] = 'row.update_or_insert'
            
        elif head['name'] == 'description':
            head['editor'] = 'richtext'
            
            #head['config'] = {
                #'imageUploadUrl': reverse('ckeditor_img'),
            #}
            # head['style']="height:300px;width:450px"

        return head


#@request_cache
#def get_mtype_options(row = None, **kws):
    #ls = [{'value': 0, 'label': '顶层'}]
    #for i in TbQa.objects.filter(mtype=0).order_by('-priority'):
        #ls.append({'value': i.type, 'label': i.title})
    #return ls


director.update({
    'help.table': HelpPage.tableCls,
    'help.table.edit': HelpForm, 
    #'get_mtype_options': get_mtype_options,
    'gen_help_static_file': HelpPage.tableCls.gen_help_static_file,
    
})

page_dc.update({
    'help': HelpPage,
})
