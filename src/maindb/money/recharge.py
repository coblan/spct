# encoding:utf-8
import re

from django.db.models import Sum, Q
from django.db import connections
from helpers.director.fields.fields import ModelFields
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from helpers.director.table.row_search import SelectSearch
from helpers.director.table.table import RowSort
from ..models import TbRecharge
from maindb.google_validate import valide_google_code

class RechargePage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值管理'

    class tableCls(ModelTable):
        model = TbRecharge
        sort = ['createtime']
        exclude = ['account', 'apolloinfo', 'apollomsg']
        fields_sort = ['rechargeid', 'accountid', 'orderid','bankcardno','accountip', 'amount', 'confirmamount', 'status', 'createtime',
                       'confirmtime', 'channelid', 'amounttype', 'isauto','apolloinfo', 'apollomsg', 'memo']

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
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-switch-to-tab'
                head['inn_editor'] = 'com-table-label-shower'
                head['tab_name'] = 'baseinfo'
                head['ctx_name'] = 'account_tabs'
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
                dc[k] = str(round(dc.get(k) or 0, 2))
            self.footer={
                '_label':'合计',
                'amount':dc.get('total_amount'),
                'confirmamount':dc.get('total_confirmamount')
            }
            #footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            #self.footer = footer
            #self.footer = ['合计'] + self.footer
            return query

        def inn_filter(self, query):
            return query.order_by('-createtime')

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            # 由于交叉引入的问题，所以只能在这里
            from maindb.member.account import account_tab
            #ctx['tabs'] = account_tab(self)
            ctx['named_ctx'] = account_tab(self)
            return ctx

        def get_operation(self):
            return [
                #{'fun': 'selected_pop_set_and_save',
                 #'editor': 'com-op-btn',
                 #'label': '手动确认',
                 #'row_match': 'one_row_match',
                 #'match_field': 'status',
                 #'match_values': [1],
                 #'match_msg': '只能选择状态为未充值的',
                 #'fields_ctx': ConfirmRechargeForm(crt_user=self.crt_user).get_head_context(),
                 #'visible': 'status' in self.permit.changeable_fields(), },
                  {'fun': 'selected_set_and_save',
                 'editor': 'com-op-btn',
                 'label': '手动确认',
                 'row_match': 'one_row',
                'match_express':'scope.row.status == 1',
                'match_msg':'只能选择状态为未充值的',
                 'fields_ctx': ConfirmRechargeForm(crt_user=self.crt_user).get_head_context(),
                 'visible': 'status' in self.permit.changeable_fields(), },
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

            #def clean_search(self):
                #if self.qf in ['orderid']:
                    #return self.q
                    ##if not re.search('^\d*$', self.q):
                        ##return None
                    ##else:
                        ##return self.q
                #else:
                    #return super().clean_search()

        class filters(RowFilter):
            range_fields = ['createtime', 'confirmtime']
            names = ['channelid', 'status', 'amounttype']


class ConfirmRechargeForm(ModelFields):
    hide_fields = ['status', 'confirmtime', 'isauto']

    class Meta:
        model = TbRecharge
        fields = ['amount', 'memo', 'status', 'confirmtime', 'isauto']

    def dict_head(self, head):
        if head['name'] == 'memo':
            head['editor'] = 'blocktext'
        return head
    
    def getExtraHeads(self):
        return [
            {'name':'google_code','label':'身份验证码','editor':'com-field-linetext','required':True,'help_text':'关键操作，需要身份验证码，请联系管理员!'}
        ]
    
    def clean(self):
        super().clean()
        if not valide_google_code(self.kw.get('google_code')):
            raise UserWarning('身份验证码错误，请联系管理员!')
    
    def save_form(self):
        inst = self.instance
        memo = '[%s]'%self.crt_user.username + inst.memo 
        dc = {
            'OrderID': inst.orderid,
            'AccountID': inst.accountid_id,
            'Amount': inst.amount,
            'ChannelType': '',
            'OrderTime': inst.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            'Code': '',
            #'CallBackInfo': inst.memo
        }
        sql = "exec [dbo].[SP_RechargeCallBack] '%(OrderID)s','%(AccountID)s',%(Amount)s,1,'%(ChannelType)s','%(OrderTime)s','%(Code)s',%%s,0,'',''" % dc
        cursor = connections['Sports'].cursor()
        cursor.execute(sql,[memo])
        result = cursor.fetchone()
        cursor.commit()
        if '@ok' not in str(result):
            raise UserWarning(str(result))
        # 从数据库刷新
        self.instance = self.instance.__class__.objects.get(pk=self.instance.pk)
        self.save_log({'content': '手动确认orderid=%(orderid)s的订单' % {'orderid': inst.orderid, },
                       'memo': '手动确认订单',
                       'model': 'TbRecharge', })


director.update({
    'Recharge': RechargePage.tableCls,
    'Recharge.edit': ConfirmRechargeForm
})

page_dc.update({
    'recharge': RechargePage
})
