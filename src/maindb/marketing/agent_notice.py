# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage, ModelTable, model_dc, page_dc, ModelFields, FieldsPage, \
    TabPage, RowSearch, RowSort, RowFilter, field_map, model_to_name
from helpers.director.model_func.dictfy import model_to_name
from ..models import TbAgentnotice
from ..status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from ..redisInstance import redisInst
from helpers.director.access.permit import has_permit


class AgentNoticePage(TablePage):
    template = 'jb_admin/table.html'
    extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]

    def get_label(self):
        return '代理通知'

    def get_context(self):
        ctx = TablePage.get_context(self)
        notice_form = NoticeForm(crt_user=self.crt_user)
        ctx['named_ctx'] = self.get_tabs()
        return ctx
    
    def get_tabs(self): 
        notice_form = NoticeForm(crt_user=self.crt_user)
        ls = [
            {'name': 'notice_form',
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
             'heads': notice_form.get_heads(),
             'ops': notice_form.get_operations()
             },
        ]
        return {
            'agent_notice_tabs': ls,
        }

    class tableCls(ModelTable):
        model = TbAgentnotice
        exclude = ['id', 'url']
        hide_fields = ['content']

        class search(RowSearch):
            names = ['title']

        class filters(RowFilter):
            names = ['status', ]

        def dict_head(self, head):
            dc = {
                'title': 180,
                'createtime': 150,
                'createuser': 100,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])

            if head['name'] == 'status':
                head['editor'] = 'com-table-bool-shower'
            elif head['name'] == 'title':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'notice_form'
                head['ctx_name'] = 'agent_notice_tabs'
            return head

        def get_operation(self):
            operations = ModelTable.get_operation(self)[0:1]
            add_new =  operations[0]
            add_new.update({
                'tab_name': 'notice_form',
                'ctx_name': 'agent_notice_tabs',
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
                }
            ])
            return operations

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['extra_table_logic'] = 'notice_logic'
            return ctx


class NoticeForm(ModelFields):
    class Meta:
        model = TbAgentnotice
        exclude = []

    hide_fields = ['createuser']

    def dict_head(self, head):
        # if head['name'] == 'createuser':
        # head['editor'] = 'com-field-label-shower'
        if head['name'] == 'title':
            head['fv_rule'] = 'length(~200)'
        if head['name'] == 'content':
            head['editor'] = 'richtext'
            head['config'] = {
                'imageUploadUrl': reverse('ckeditor_img'),
            }
        return head

    def dict_row(self, row):
        return {
            'createtime': row.createtime.strftime('%Y-%m-%d %H:%M:%S') if row.createtime else None,

        }


director.update({
    'agentnotice': AgentNoticePage.tableCls,
    'agentnotice.edit': NoticeForm
})

page_dc.update({
    'agentnotice': AgentNoticePage,
})
