# encoding:utf-8
import re

from django.db.models import Sum, Q
from django.db import connections
from helpers.director.fields.fields import ModelFields
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from helpers.director.table.row_search import SelectSearch
from helpers.director.table.table import RowSearch, RowSort
from ..models import TbRecharge


class RechargePage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值管理'

    class tableCls(ModelTable):
        model = TbRecharge
        sort = ['createtime']
        exclude = ['account', 'apolloinfo', 'apollomsg']
        fields_sort = ['rechargeid', 'accountid', 'orderid', 'amount', 'confirmamount', 'status', 'createtime',
                       'confirmtime',
                       'channelid', 'amounttype', 'isauto', 'memo',
                       'apolloinfo', 'apollomsg']

        def dict_head(self, head):
            dc = {
                'rechargeid': 60,
                'amount': 100,
                'confirmamount': 100,
                'accountid': 120,
                'channelid': 120,
                'createtime': 150,
                'confirmtime': 150,
                'apollomsg': 200
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def statistics(self, query):
            dc = query.aggregate(total_amount=Sum('amount'), total_confirmamount=Sum('confirmamount'))
            mapper = {
                'amount': 'total_amount',
                'confirmamount': 'total_confirmamount'
            }
            for k in dc:
                dc[k] = str(dc[k])
            footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            self.footer = footer
            self.footer = ['合计'] + self.footer
            return query

        def inn_filter(self, query):
            return query.order_by('-createtime')

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            return ctx

        def get_operation(self):
            return [
                {'fun': 'selected_pop_set_and_save',
                 'editor': 'com-op-btn',
                 'label': '手动确认',
                 'row_match': 'one_row_match',
                 'match_field': 'status',
                 'match_values': [1],
                 'match_msg': '只能选择状态为未充值的',
                 'fields_ctx': ConfirmRechargeForm(crt_user=self.crt_user).get_head_context()},
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o'}
            ]

        class sort(RowSort):
            names = ['amount', 'confirmamount', 'createtime', 'confirmtime']

        class search(SelectSearch):
            names = ['accountid__nickname']
            exact_names = ['orderid']

            def get_option(self, name):
                if name == 'orderid':
                    return {'value': name,
                            'label': '订单编号', }
                elif name == 'accountid__nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }

            def clean_search(self):
                if self.qf in ['orderid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()

        class filters(RowFilter):
            range_fields = ['createtime', 'confirmtime']
            names = ['channelid', 'status']


class ConfirmRechargeForm(ModelFields):
    hide_fields = ['status']

    class Meta:
        model = TbRecharge
        fields = ['amount', 'memo', 'status']

    def dict_head(self, head):
        if head['name'] == 'memo':
            head['editor'] = 'blocktext'
        return head

    def save_form(self):
        inst = self.instance
        dc = {
            'OrderID': inst.orderid,
            'AccountID': inst.accountid_id,
            'Amount': inst.amount,
            'ChannelType': '',
            'OrderTime': inst.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            'Code': '',
            'CallBackInfo': inst.memo
        }
        sql = "exec [dbo].[SP_RechargeCallBack] '%(OrderID)s','%(AccountID)s',%(Amount)s,1,'%(ChannelType)s','%(OrderTime)s','%(Code)s','%(CallBackInfo)s',0" % dc
        cursor = connections['Sports'].cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.commit()
        if '@ok' not in str(result):
            raise UserWarning(str(result))
        self.instance = self.instance.__class__.objects.get(pk=self.instance.pk)


director.update({
    'Recharge': RechargePage.tableCls,
    'Recharge.edit': ConfirmRechargeForm
})

page_dc.update({
    'recharge': RechargePage
})
