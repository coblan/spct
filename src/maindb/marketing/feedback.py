# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage, ModelTable, model_dc, page_dc, ModelFields, FieldsPage, \
    TabPage, RowSearch, RowSort, RowFilter, field_map, model_to_name
from helpers.director.model_func.dictfy import model_to_name
from ..models import TbNotice, TbAgentleavemsg
from ..status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from ..redisInstance import redisInst


class Feedback(TablePage):
    template = 'jb_admin/table.html'


    def get_label(self):
        return '用户留言'

    class tableCls(ModelTable):
        model = TbAgentleavemsg
        fields_sort = ['accountid', 'title', 'msg', 'createtime']
        pop_edit_field = 'title'


        def get_operation(self):
            return []

        def dict_head(self, head):
            dc = {
                'accountid': 120,
                'title': 200,
                'msg': 400,
                'createtime': 140
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head


class FeedbackForm(ModelFields):
    readonly = ['title', 'msg','accountid','createtime']
    field_sort = ['accountid','title', 'msg','createtime']

    def get_operations(self): 
        return []

    class Meta:
        model = TbAgentleavemsg
        exclude = ['answer','isanswer']



director.update({
    'feedback.table': Feedback.tableCls,
    'feedback.table.edit': FeedbackForm
})

page_dc.update({
    'feedback': Feedback,
})
