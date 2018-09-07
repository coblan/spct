# encoding:utf-8
import re

from django.utils.timezone import datetime

from django.db.models import Sum, Q
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter, ModelFields
from helpers.director.table.row_search import SelectSearch
from helpers.director.table.table import RowSort
from ..models import TbWithdraw, TbBalancelog
from maindb.rabbitmq_instance import notifyWithdraw


class WithdrawPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '提现管理'

    class tableCls(ModelTable):
        model = TbWithdraw
        exclude = []
        fields_sort = ['accountid', 'orderid', 'amount', 'status', 'createtime', 'confirmtime',
                       'amounttype', 'memo',
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
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '审核异常单',
                    'field': 'status',
                    'value': 1,
                    'row_match': 'one_row_match',
                    'match_field': 'status',
                    'match_values': [4],
                    'match_msg': '只能选择状态为异常的订单！',
                    'fields_ctx': WithDrawForm(crt_user=self.crt_user).get_head_context()},
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '确认成功',
                    'field': 'status',
                    'value': 2,
                    'row_match': 'one_row_match',
                    'match_field': 'status',
                    'match_values': [1],
                    'match_msg': '只能选择状态为处理中的订单！',
                    'confirm_msg': '确认修改订单状态为成功吗？',
                    'fields_ctx': WithDrawForm(crt_user=self.crt_user).get_head_context()},
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '退款',
                    'field': 'status',
                    'value': 5,
                    'row_match': 'one_row_match',
                    'match_field': 'status',
                    'match_values': [4],
                    'confirm_msg': '确认退款到用户余额吗？',
                    'match_msg': '只能选择状态为异常的订单',
                    'fields_ctx': WithDrawForm(crt_user=self.crt_user).get_head_context()},
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o'}
            ]

        def inn_filter(self, query):
            return query.order_by('-createtime')

        class sort(RowSort):
            names = ['amount', 'createtime', 'confirmtime']

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
            names = ['status']


class WithDrawForm(ModelFields):
    hide_fields = ['status', 'orderid', 'account']

    class Meta:
        model = TbWithdraw
        fields = ['orderid', 'account', 'memo', 'status', 'confirmtime']

    def dict_head(self, head):
        if head['name'] == 'memo':
            head['editor'] = 'blocktext'
            head['required'] = True
        else:
            head['readonly'] = True
        return head

    def save_form(self):
        super().save_form()
        if 'status' in self.changed_data and 'memo' in self.changed_data and self.instance.status == 1:
            notifyWithdraw(self.instance.accountid_id, self.instance.orderid)
        elif 'status' in self.changed_data and 'memo' in self.changed_data and self.instance.status == 2:
            self.instance.confirmtime = datetime.now()
            self.save()
        elif 'status' in self.changed_data and 'memo' in self.changed_data and self.instance.status == 5:  # 退款
            beforamount = self.instance.accountid.amount
            afteramount = self.instance.accountid.amount + self.instance.amount
            self.instance.accountid.amount += self.instance.amount
            self.save()
            TbBalancelog.objects.create(account=self.instance.account, beforeamount=beforamount,
                                        amount=self.instance.amount, afteramount=afteramount, creater='system',
                                        memo='提现退款', accountid=self.instance.accountid, categoryid_id=35,
                                        cashflow=1)


director.update({
    'Withdraw': WithdrawPage.tableCls,
    'Withdraw.edit': WithDrawForm,
})

page_dc.update({
    'withdraw': WithdrawPage,
})
