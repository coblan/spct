# encoding:utf-8
from django.db.models import Sum, Q

from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from helpers.director.table.table import RowSearch, RowSort
from ..models import TbAgentcommission


class AgentCommissionPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '代理佣金'

    class tableCls(ModelTable):
        model = TbAgentcommission
        sort = ['Amount']
        exclude = ['creater','updater','updatetime','description','agent']
        # fields_sort = ['rechargeid', 'accountid','orderid', 'amount', 'status', 'createtime','confirmtime', 'channelid', 'amounttype','isauto', 'memo',
        #                'apolloinfo', 'apollomsg']

        def dict_head(self, head):
            dc = {
                'accountid':100,
                'amount':120,
                'daus': 100,
                'lostamount': 120,
                'balancelostamount': 120,
                'createtime': 140,
                'applytime': 140,
                'settledate':120
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
            names = ['amount', 'daus','lostamount','balancelostamount']

        class search(RowSearch):
            def get_context(self):
                return {'search_tip': '昵称',
                        'editor': 'com-search-filter',
                        'name': '_q'
                        }

            def get_query(self, query):
                if self.q:
                    return query.filter(Q(accountid__nickname__icontains=self.q) | Q(orderid=self.q))
                else:
                    return query

        class filters(RowFilter):
            range_fields = ['createtime']
            names = ['status']


director.update({
    'AgentCommission': AgentCommissionPage.tableCls
})

page_dc.update({
    'AgentCommission': AgentCommissionPage,
})
