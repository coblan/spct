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


class FeedBack(TablePage):
    template = 'jb_admin/table.html'
    extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]

    def get_label(self):
        return '用户留言'

    class tableCls(ModelTable):
        model = TbAgentleavemsg
        fields_sort = ['accountid', 'title', 'msg', 'createtime']

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


director.update({
    'feedback.table': FeedBack.tableCls
})

page_dc.update({
    'feedback': FeedBack,
})
