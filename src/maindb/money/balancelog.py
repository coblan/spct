# encoding:utf-8
from __future__ import unicode_literals
from django.db.models import Sum
from helpers.director.shortcut import RowSort,SelectSearch,has_permit
from ..models import TbBalancelog
from .chargeflow import *
from ..status_code import ACCOUNT_TYPE
from hello.merchant_user import get_user_merchantid

class BalancelogPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '账目记录'

    class tableCls(ModelTable):
        model = TbBalancelog
        include = ['merchant','accountid', 'categoryid', 'beforeamount', 'amount', 'afteramount',  'createtime','memo'] # creater

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

        def getExtraHead(self):
            return [
                {'name':'accountid__accounttype','label':'账号类型','editor':'com-table-label-shower',}
            ]
        
        def dict_row(self, inst):
            dc= dict(ACCOUNT_TYPE)
            return {
                
                '_accountid__accounttype_label': dc.get( inst.accountid.accounttype ,'')
            }
        
        def get_operation(self):
            return [
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]

        def statistics(self, query):
            dc = query.aggregate(total_amount=Sum('amount'))
            mapper = {
                'amount': 'total_amount'
            }
            for k in dc:
                dc[k] = str(round(dc.get(k) or 0, 2))
            self.footer = {'amount':dc.get('total_amount'),'_label':'合计'}
            #footer = [dc.get(mapper.get(name), '') for name in self.include]
            #self.footer = footer
            #self.footer = ['合计'] + self.footer
            return query

        #def get_context(self):
            #ctx = ModelTable.get_context(self)
            #ctx['footer'] = self.footer
            #return ctx

        def inn_filter(self, query):
            if self.crt_user.merchant:
                query = query.filter(merchant_id = self.crt_user.merchant.id)
            return query.order_by('-createtime')

        class filters(RowFilter):
            #names = ['categoryid','accountid__accounttype']
            range_fields = ['createtime']
            
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['categoryid','accountid__accounttype']
                else:
                    return ['merchant','categoryid','accountid__accounttype']
            
            def dict_head(self, head):
                if head['name']=='createtime':
                    head['editor']='com-filter-datetime-range'
                return head
            
            def getExtraHead(self):
                return [
                    {'name':'accountid__accounttype','label':'账号类型','editor':'com-filter-select','options':[{'value':x[0],'label':x[1]} for x in ACCOUNT_TYPE]}
                ]

        class search(SelectSearch):
            names = ['accountid__nickname']

            def get_option(self, name):
                if name == 'accountid__nickname':
                    return {'value': 'accountid__nickname', 'label': '用户昵称', }
                else:
                    return super().get_option(name)

        class sort(RowSort):
            names = ['createtime']


director.update({
    'money.balancelog': BalancelogPage.tableCls
})

page_dc.update({
    'balancelog': BalancelogPage
})
