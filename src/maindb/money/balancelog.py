# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import RowSearch, RowSort, RowFilter, director
from ..models import TbBalancelog
from .chargeflow import *


class BalancelogPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '账目记录'

    class tableCls(ModelTable):
        model = TbBalancelog
        include = ['accountid', 'categoryid', 'beforeamount', 'amount', 'afteramount', 'memo', 'createtime', 'creater']

        def dict_head(self, head):
            dc = {
                'account': 120,
                'categoryid': 100,
                'beforeamount': 120,
                'amount': 120,
                'afteramount': 120,
                'memo': 250,
                'createtime': 150,
                'creater': 120
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def get_operation(self):
            return [
                {'fun': 'export_excel','editor': 'com-op-btn','label': '导出excel','icon': 'fa-file-excel-o',}
            ]

        class filters(RowFilter):
            names = ['categoryid']
            range_fields = ['createtime']

        class search(RowSearch):
            def get_context(self):
                return {'search_tip': '用户昵称',
                        'editor': 'com-search-filter',
                        'name': '_q'
                        }

            def get_query(self, query):
                if self.q:
                    return query.filter(accountid__nickname__icontains=self.q)
                else:
                    return query

        class sort(RowSort):
            names = ['createtime']


director.update({
    'money.balancelog': BalancelogPage.tableCls
})

page_dc.update({
    'maindb.balancelog': BalancelogPage
})
