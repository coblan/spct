# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,model_to_name,director
from .models import TbAccount,TbBalancelog,TbLoginlog,TbTrans,TbTicketmaster,TbWithdrawlimitlog
from .status_code import *
from helpers.director.shortcut import model_to_name, model_full_permit, add_permits
import json
from helpers.func.collection.container import evalue_container
from helpers.director.access.permit import can_touch
# Register your models here.

class AccountPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return '会员管理'
    
    def get_context(self):
        ctx = TablePage.get_context(self)
        baseinfo = AccoutBaseinfo(crt_user=self.crt_user)
        ls = [
            {'name':'baseinfo',
             'label':_('Basic Info'),
             'com':'com_tab_fields',
             'get_data':{
                 'fun':'get_row',
                 'kws':{
                    'director_name':AccoutBaseinfo.get_director_name(),
                    'relat_field':'accountid',              
                 }
             },
             'after_save':{
                 'fun':'update_or_insert'
             },
             'heads': baseinfo.get_heads(),
             'ops': baseinfo.get_operations()                 
             },
            {'name':'balance_log',
             'label':_('Balance Log'),
             'com':'com_tab_table',
             'get_data':{
                 'fun':'get_rows',
                 'kws':{
                    'director_name':AccountBalanceTable.get_director_name() ,# model_to_name(TbBalancelog),
                    'relat_field':'accountid',
                 }
                 
             },
             'table_ctx':AccountBalanceTable(crt_user=self.crt_user).get_head_context(), 
             'visible': can_touch(TbBalancelog, self.crt_user),
             },
            #{'name':'account_trans',
             #'label':_('Transaction Log'),
             #'com':'com_tab_table',
             #'get_data':{
                 #'fun':'get_rows',
                 #'kws':{
                     #'director_name':AccountTransTable.get_director_name(),# model_to_name(TbTrans),
                     #'relat_field':'account',                     
                 #}
             #},
             #'table_ctx':AccountTransTable(crt_user=self.crt_user).get_head_context()
             #},
            {'name':'account_ticket',
             'label':_('Ticket'),
             'com':'com_tab_table',
             'get_data':{
                 'fun':'get_rows',
                 'kws':{
                     'director_name': AccountTicketTable.get_director_name(), #model_to_name(TbTicketmaster),
                     'relat_field':'accountid',
                 }
             },
             'table_ctx':AccountTicketTable(crt_user=self.crt_user).get_head_context(), 
              'visible': can_touch(TbTicketmaster, self.crt_user),
             },
            {'name':'account_login',
            'label':_('Login Log'),
            'com':'com_tab_table',
            'get_data':{
                'fun':'get_rows',
                'kws':{
                    'director_name':AccountLoginTable.get_director_name(), #model_to_name(TbLoginlog),
                    'relat_field':'accountid',                    
                }
            },
            'table_ctx':AccountLoginTable(crt_user=self.crt_user).get_head_context(), 
            'visible': can_touch(TbLoginlog, self.crt_user),},
            
            #{'name':'account_withdrawlimitlog',
            #'label':_('Withdraw Log'),
            #'com':'com_tab_table',
            #'get_data':{
                #'fun':'get_rows',
                #'kws':{
                    #'director_name': AccoutWithdrawLimitLogTable.get_director_name(),#model_to_name(TbWithdrawlimitlog),
                    #'relat_field':'accountid',                    
                #}
            #},
            #'table_ctx':AccoutWithdrawLimitLogTable(crt_user=self.crt_user).get_head_context()}, 
                       
            ]
        ctx['tabs']= evalue_container( ls )
        return ctx
    
    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid','account','accounttype','username','viplv','createtime']
        #fields_sort=['accountid','account','accounttype','username']

        def dict_row(self, inst):
            account_type = dict(ACCOUNT_TYPE)
            return {
                'amount':str(inst.amount),
                'accounttype': account_type.get(inst.accounttype)
            }
        
        def dict_head(self, head):
            dc={
                'accountid':80,
                'account':150,
                'accounttype':80,
                'username':120,
                'viplv':100,
                'createtime':150
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name']='baseinfo'
            return head
    
        class search(RowSearch):
            names=['account']

        class sort(RowSort):
            names=['account']

class AccoutBaseinfo(ModelFields):
        field_sort=['accounttype','account','username','status','agent','verify','viplv','createtime']
        readonly=['createtime']
        class Meta:
            model=TbAccount
            exclude =['password', 'account', 'amount']

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
    
class WithAccoutInnFilter(ModelTable):
    def inn_filter(self, query):
        query = ModelTable.inn_filter(self,query)
        if self.kw.get('accountid'):
            return query.filter(accountid=self.kw.get('accountid'))   
        else:
            return query    

class AccountBalanceTable(WithAccoutInnFilter):
    model = TbBalancelog
    exclude = []
    
    def dict_head(self, head): 
        dc={
            'beforeamount':110,
            'afteramount': 110,
            'createtime': 110,
      
           }
        if dc.get(head['name']):
            head['width'] =dc.get(head['name'])        
        return head
    
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


class AccountTransTable(WithAccoutInnFilter):
    model=TbTrans
    exclude=[]  
   
    
class AccountTicketTable(WithAccoutInnFilter):
    """投注记录"""
    model=TbTicketmaster
    exclude=[]  
    def dict_head(self, head): 
        dc={
            'betoutcome':110,
            'stakecount': 110,
            'parlaycount': 110,
            'reststakecount': 110,
            'possibleturnover': 160,
      
           }
        if dc.get(head['name']):
            head['width'] =dc.get(head['name'])         
        return head
  

class AccountLoginTable(WithAccoutInnFilter):
    model=TbLoginlog
    exclude=[]
    
    def dict_head(self, head): 
        dc={
            'deviceversion':120,
            'devicename':120,
        }
        if dc.get(head['name']):
            head['width'] =dc.get(head['name'])
        return head
  

class AccoutWithdrawLimitLogTable(WithAccoutInnFilter):
    model=TbWithdrawlimitlog
    exclude=[]
   

#class AccountTokenCodeTable(AccountTabBase):
    ## 去掉了。
    #model=TbTokencode
    #exclude=[]
    #class sort(RowSort):
        #names=['tokentypeid']
    #class filters(RowFilter):
        #names=['tokentypeid']

class LoginLogPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return _('Tb Login Log')
    
    class tableCls(ModelTable):
        model=TbLoginlog
        exclude=[]
        fields_sort=['accountid__username','devicecode','deviceip','appversion','devicename','deviceversion',
                     'logintype','createtime']
        
        def dict_head(self, head): 
            dc={
                'accountid':100,
                'devicecode':120,
                'deviceip':120,
                'appversion':100,
                'devicename':120,
                'deviceversion':120,
                'createtime':150
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head
        
        def get_heads(self):
            heads=[{
                'name':'accountid__username',
                'label':'用户'
            }]
            heads2 = ModelTable.get_heads(self)
            heads.extend(heads2)
            return heads
        
        def permited_fields(self):
            fields = ModelTable.permited_fields(self)
            fields.append('accountid__username')
            return fields
        
        def inn_filter(self, query):
            return query.values(*self.fields_sort).order_by('-createtime')
        
        class search(RowSearch):
            names=['account','deviceip']
        
        class filters(RowFilter):
            range_fields=['createtime']

director.update({
    'account':AccountPage.tableCls,
    'account.base.edit':AccoutBaseinfo,
    'account.log':AccountLoginTable,
    'account.ticketmaster':AccountTicketTable,
    'account.trans':AccountTransTable,
    'account.balancelog':AccountBalanceTable,
    'account.withdrawlimitlog':AccoutWithdrawLimitLogTable,
    
    'account.loginpage':LoginLogPage.tableCls,
})
#model_dc[TbAccount]={'fields':AccoutBaseinfo,'table':AccountPage.tableCls}
#model_dc[TbTicketmaster]={'table':AccountTicketTable}
#model_dc[TbLoginlog]={'table':AccountLoginTable}
#model_dc[TbTrans]={'table':AccountTransTable}
#model_dc[TbBalancelog]={'table':AccountBalanceTable}
#model_dc[TbWithdrawlimitlog]={'table':AccoutWithdrawLimitLogTable}

page_dc.update({
    'maindb.loginlog':LoginLogPage
})




permits = [('TbAccount', model_full_permit(TbAccount), model_to_name(TbAccount), 'model' ), 
           ('TbLoginlog', model_full_permit(TbLoginlog), model_to_name(TbLoginlog),'model' ), 
           ('TbBalancelog', model_full_permit(TbBalancelog), model_to_name(TbBalancelog), 'model'), 
           #('TbTicketmaster', model_full_permit(TbTicketmaster), model_to_name(TbTicketmaster), 'model'), 
           ('TbAccount.all', 'TbAccount;TbLoginlog;TbBalancelog;TbTicketmaster', '', 'set'), 
           ]

add_permits(permits)

    
