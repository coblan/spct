# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,model_to_name
from .models import TbAccount,TbBalancelog,TbLoginlog,TbTrans,TbTicketmaster,TbWithdrawlimitlog,TbTokencode
from .status_code import *
# Register your models here.

class AccountPage(TablePage):
    template='maindb/table_ajax_tab.html'
    def get_label(self):
        return '会员管理'
    
    def get_context(self):
        ctx = TablePage.get_context(self)
        ls = [
            {'name':'baseinfo',
             'label':'基本信息','com':'com_ajax_fields',
             'model_name':'maindb.TbAccount',
             'relat_field':'accountid',
             'kw': AccoutBaseinfo(crt_user=self.crt_user).get_heads()},
            {'name':'balance_log',
             'label':'帐目记录',
             'com':'com_ajax_table',
             'model':model_to_name(TbBalancelog),
             'relat_field':'accountid',
             'kw':AccountBalanceTable(crt_user=self.crt_user).get_head_context()},
            {'name':'account_trans',
             'label':'交易记录',
             'com':'com_ajax_table',
             'model':model_to_name(TbTrans),
             'relat_field':'accountid',
             'kw':AccountTransTable(crt_user=self.crt_user).get_head_context()},
            {'name':'account_ticket',
             'label':'投注记录',
             'com':'com_ajax_table',
             'model':model_to_name(TbTicketmaster),
             'relat_field':'accountid',
             'kw':AccountTicketTable(crt_user=self.crt_user).get_head_context()},
            {'name':'account_login',
            'label':'登录日志',
            'com':'com_ajax_table',
            'model':model_to_name(TbLoginlog),
            'relat_field':'accountid',
            'kw':AccountLoginTable(crt_user=self.crt_user).get_head_context()},
            {'name':'account_withdrawlimitlog',
            'label':'提款限额记录',
            'com':'com_ajax_table',
            'model':model_to_name(TbWithdrawlimitlog),
            'relat_field':'accountid',
            'kw':AccoutWithdrawLimitLogTable(crt_user=self.crt_user).get_head_context()}, 
            #{'name':'account_tokencode',
             #'label':'验证码查询',
             #'com':'com_ajax_table',
             #'kw':AccountTokenCodeTable(crt_user=self.crt_user).get_head_context()},                 
            ]
        ctx['tabs']=ls
        return ctx
    
    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid','account','accounttype','username','viplv','createtime']
        #fields_sort=['accountid','account','accounttype','username']

        def dict_row(self, inst):
            account_type = dict(ACCOUNT_TYPE)
            return {
                'amount':unicode(inst.amount),
                'accounttype': account_type.get(inst.accounttype)
            }
        
        def dict_head(self, head):
            dc={
                'accountid':40,
                'account':120,
                'accounttype':60,
                'username':80,
                'viplv':40,
                'createtime':100
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head
    
        class search(RowSearch):
            names=['account']

        class sort(RowSort):
            names=['account']

class AccoutBaseinfo(ModelFields):
    field_sort=['accounttype','account','username','status','agent','verify','viplv','createtime']
    readonly=['account','createtime']
    class Meta:
        model=TbAccount
        exclude =[]

class AccountTabBase(ModelTable):
    def __init__(self, *args,**kws):
        ModelTable.__init__(self,*args,**kws)
        accountid = self.kw.get('accountid')
        self.accountid = accountid
        #if accountid:
            #account = TbAccount.objects.get(accountid=accountid)
            #self.accountid = account.accountid
    
    def inn_filter(self, query):
        return query.filter(accountid=self.accountid) 
    

class AccountBalanceTable(AccountTabBase):
    model = TbBalancelog
    exclude = []
       
    def dict_row(self, inst):
        ba_cat = dict(BALANCE_CAT)
        return {
            'categoryid':ba_cat.get(inst.categoryid)
        }
    
    class sort(RowSort):
        names=['createtime']
    
    class filters(RowFilter):
        names=['categoryid']
        range_fields = [{'name':'createtime','type':'date'}]


class AccountTransTable(AccountTabBase):
    model=TbTrans
    exclude=[]  
   
    

class AccountTicketTable(AccountTabBase):
    """投注记录"""
    model=TbTicketmaster
    exclude=[]  
  

class AccountLoginTable(AccountTabBase):
    model=TbLoginlog
    exclude=[]
  

class AccoutWithdrawLimitLogTable(AccountTabBase):
    model=TbWithdrawlimitlog
    exclude=[]
   

class AccountTokenCodeTable(AccountTabBase):
    # 去掉了。
    model=TbTokencode
    exclude=[]
    class sort(RowSort):
        names=['tokentypeid']
    class filters(RowFilter):
        names=['tokentypeid']

model_dc[TbAccount]={'fields':AccoutBaseinfo}
model_dc[TbTicketmaster]={'table':AccountTicketTable}
model_dc[TbLoginlog]={'table':AccountLoginTable}
model_dc[TbTrans]={'table':AccountTransTable}
model_dc[TbBalancelog]={'table':AccountBalanceTable}

    
