# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, \
    RowSearch, RowFilter, director
from helpers.director.table.row_search import SelectSearch
from ..models import TbLoginlog
import re
from django.db.models import Q



class LoginLogPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return _('Tb Login Log')

    class tableCls(ModelTable):
        model = TbLoginlog
        exclude = []
        fields_sort = ['accountid_id', 'accountid__nickname', 'devicecode', 'deviceip', 'appversion', 'devicename',
                       'deviceversion',
                       'logintype', 'createtime']

        def dict_head(self, head):
            dc = {
                'accountid_id': 80,
                'devicecode': 120,
                'deviceip': 120,
                'appversion': 100,
                'devicename': 120,
                'deviceversion': 120,
                'createtime': 150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def getExtraHead(self):
            return [
                {'name': 'accountid__nickname', 'label': '用户昵称'},
                {'name': 'accountid_id', 'label': '用户ID'}
            ]

        def inn_filter(self, query):
            return query.values(*self.fields_sort).order_by('-createtime')

        class search(SelectSearch):
            names = ['accountid__nickname']
            exact_names = ['accountid']

            def get_option(self, name):
                if name == 'accountid':
                    return {'value': name,
                            'label': '用户ID', }
                elif name == 'accountid__nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }

            def clean_search(self):
                if self.qf in ['accountid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()

        class filters(RowFilter):
            range_fields = ['createtime']


director.update({
    'account.loginpage': LoginLogPage.tableCls,
})

page_dc.update({
    'loginlog': LoginLogPage
})