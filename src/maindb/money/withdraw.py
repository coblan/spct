# encoding:utf-8
from django.db.models import Sum, Q
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from helpers.director.table.table import RowSearch, RowSort
from ..models import TbWithdraw


class WithdrawPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '提现管理'

    class tableCls(ModelTable):
        model = TbWithdraw
        exclude = []
        fields_sort = ['withdrawid', 'accountid', 'orderid','amount', 'status', 'createtime','confirmtime', 'amounttype', 'memo',
                       'apollocode', 'apollomsg']

        def dict_head(self, head):
            dc = {
                'accountid': 120,
                'createtime': 150,
                'confirmtime': 150,
                'apollomsg': 200,
                'memo': 120,
                'apollocode': 150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def statistics(self, query):
            dc = query.aggregate(total_amount=Sum('amount'))
            mapper = {
                'amount': 'total_amount'
            }
            for k in dc:
                dc[k] = str(dc[k])
            footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            self.footer = footer
            self.footer = ['合计'] + self.footer
            return query

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            return ctx
        
        def get_operation(self): 
            return [
                 {'fun': 'export_excel','editor': 'com-op-btn','label': '导出Excel','icon': 'fa-file-excel-o'}
            ]
        
        class sort(RowSort):
            names = ['amount', 'createtime','confirmtime']

        class search(RowSearch):
            def get_context(self):
                return {'search_tip': '昵称,订单号',
                        'editor': 'com-search-filter',
                        'name': '_q'
                        }

            def get_query(self, query):
                if self.q:
                    return query.filter(Q(accountid__nickname__icontains=self.q) | Q(orderid=self.q))
                else:
                    return query

        class filters(RowFilter):
            range_fields = ['createtime','confirmtime']
            names = ['status']


director.update({
    'Withdraw': WithdrawPage.tableCls
})

page_dc.update({
    'Withdraw': WithdrawPage,
})
