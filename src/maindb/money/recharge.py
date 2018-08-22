# encoding:utf-8
from django.db.models import Sum

from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from helpers.director.table.table import RowSearch, RowSort
from ..models import TbRecharge


class RechargePage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值管理'

    class tableCls(ModelTable):
        model = TbRecharge
        sort = ['createtime']
        exclude = ['account']
        fields_sort = ['rechargeid', 'accountid', 'amount', 'status', 'createtime', 'channelid', 'amounttype', 'memo',
                       'apolloinfo', 'apollomsg']

        def dict_head(self, head):
            dc = {
                'accountid': 120,
                'channelid': 120,
                'createtime': 150,
                'apollomsg': 200
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


        class sort(RowSort):
            names = ['amount', 'createtime']

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
    'Recharge': RechargePage.tableCls
})

page_dc.update({
    'Recharge': RechargePage,
})
