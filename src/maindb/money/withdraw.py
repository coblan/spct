# encoding:utf-8
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter, field_map, BaseFieldProc, \
    model_to_name
from helpers.director.model_func.field_procs.datetimeproc import DateTimeProc
from helpers.director.table.table import RowSearch, RowSort
from ..models import TbWithdraw


class WithdrawPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '提现管理'

    class tableCls(ModelTable):
        model = TbWithdraw
        exclude = []
        fields_sort = ['withdrawid', 'accountid', 'amount', 'status', 'createtime', 'amounttype', 'memo',
                       'apollocode', 'apollomsg']

        def dict_head(self, head):
            dc = {
                'accountid': 120,
                'createtime': 150,
                'apollomsg': 200
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        class sort(RowSort):
            names = ['amount','createtime']

        class search(RowSearch):
            def get_context(self):
                return {'search_tip': '昵称',
                        'editor': 'com-search-filter',
                        'name': '_q'
                        }

            def get_query(self, query):
                if self.q:
                    return query.filter(accountid__nickname__icontains=self.q)
                else:
                    return query

        class filters(RowFilter):
            range_fields = ['createtime']
            names = ['status']


director.update({
    'Withdraw': WithdrawPage.tableCls
})

page_dc.update({
    'Withdraw': WithdrawPage,
})
