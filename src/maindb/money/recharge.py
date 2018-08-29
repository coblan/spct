# encoding:utf-8
from django.db.models import Sum, Q
from django.db import connections
from helpers.director.fields.fields import ModelFields
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from helpers.director.table.table import RowSearch, RowSort
from ..models import TbRecharge
from django.utils.timezone import datetime


class RechargePage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值管理'

    class tableCls(ModelTable):
        model = TbRecharge
        sort = ['createtime']
        exclude = ['account']
        fields_sort = ['rechargeid', 'accountid', 'orderid', 'amount', 'status', 'createtime', 'confirmtime',
                       'channelid', 'amounttype', 'isauto', 'memo',
                       'apolloinfo', 'apollomsg']

        def dict_head(self, head):
            dc = {
                'rechargeid': 60,
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
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '手动确认', 'field': 'status',
                 'value': 2,
                 'row_match': 'many_row_match', 'match_field': 'status', 'match_values': [1], 'match_msg': '只能选择未确认的订单',
                 'confirm_msg': '确认这些订单吗?', 'fields_ctx': {
                    'heads': [{'name': 'amount', 'label': '实际金额', 'editor': 'number', 'required': True},
                              {'name': 'memo', 'label': '备注', 'editor': 'blocktext', 'required': True}],
                    'ops': [{'fun': 'save', 'label': '确定', 'editor': 'com-op-btn', }],
                }, },
            ]

        class sort(RowSort):
            names = ['amount', 'createtime', 'confirmtime']

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
            range_fields = ['createtime', 'confirmtime']
            names = ['channelid', 'status']


class ConfirmRechargeForm(ModelFields):
    class Meta:
        model = TbRecharge
        exclude = ['isauto', 'account']

    def save_form(self):
        inst = self.instance
        dc = {
            'OrderID': inst.orderid,
            'AccountID': inst.accountid_id,
            'Amount': inst.amount,
            'ChannelType': '',
            'OrderTime': inst.createtime,
            'Code': '',
            'CallBackInfo': '手动确认'
        }
        sql = "exec [dbo].[SP_RechargeCallBack] '%(OrderID)s','%(AccountID)s',%(Amount)s,1,'%(ChannelType)s','%(OrderTime)s','%(Code)s','%(CallBackInfo)s',0" % dc
        cursor = connections['Sports'].cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.commit()
        if 'ok' not in result:
            result = str(cursor)


director.update({
    'Recharge': RechargePage.tableCls,
    'Recharge.edit': ConfirmRechargeForm
})

page_dc.update({
    'Recharge': RechargePage
})
