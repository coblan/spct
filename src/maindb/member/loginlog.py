# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, \
    RowSearch, RowFilter, director
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

        class search(RowSearch):
            names = ['accountid', 'deviceip', 'accountid__nickname']

            def get_context(self):
                """
                """
                dc = {
                    'search_tip': '设备ip,用户昵称,用户ID',
                    'editor': 'com-search-filter',
                    'name': '_q'
                }
                return dc

            def get_query(self, query):
                names = ['deviceip', 'accountid__nickname']
                if self.q:
                    exp = None
                    for name in names:
                        kw = {}
                        kw['%s__icontains' % name] = self.q
                        if exp is None:
                            exp = Q(**kw)
                        else:
                            exp = exp | Q(**kw)
                    if re.search('^\d+$', self.q):
                        exp = exp | Q(accountid_id=self.q)
                    return query.filter(exp)
                else:
                    return query

        class filters(RowFilter):
            range_fields = ['createtime']


director.update({
    'account.loginpage': LoginLogPage.tableCls,
})

page_dc.update({
    'maindb.loginlog': LoginLogPage
})