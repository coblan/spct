# encoding:utf-8
from django.db.models import Sum, Q
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter, ModelFields
from helpers.director.table.table import RowSearch, RowSort
from ..models import TbWithdraw, TbBalancelog
from maindb.rabbitmq_instance import notifyWithdraw


class WithdrawPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '提现管理'

    class tableCls(ModelTable):
        model = TbWithdraw
        exclude = []
        fields_sort = ['withdrawid', 'accountid', 'orderid', 'amount', 'status', 'createtime', 'confirmtime',
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
                    'label': '审核',
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
            names = ['status']


class WithDrawForm(ModelFields):
    hide_fields = ['status', 'orderid', 'account']

    class Meta:
        model = TbWithdraw
        fields = ['orderid', 'account', 'memo', 'status']

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
        if 'status' in self.changed_data and 'memo' in self.changed_data and self.instance.status == 5:  # 退款
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
    'Withdraw': WithdrawPage,
})
