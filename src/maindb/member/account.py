# encoding:utf-8
from __future__ import unicode_literals

import re

from django.db.models import Sum, Case, When, F,Count,OuterRef,Subquery
from django.utils.translation import ugettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter, director
from helpers.director.table.row_search import SelectSearch
from maindb.matches.matches_statistics import MatchesStatisticsPage
from maindb.money.balancelog import BalancelogPage
from ..models import TbAccount, TbBalancelog, TbLoginlog, TbTicketmaster, TbBankcard, TbRecharge, TbWithdraw, TbMatches,TbBetfullrecord
from helpers.func.collection.container import evalue_container
from helpers.director.access.permit import can_touch
from helpers.func.random_str import get_str, get_random_number
import hashlib
from decimal import Decimal
from ..matches.ticket_master import TicketMasterPage
from ..member.bankcard import BankCard, BankCardForm
from ..money.recharge import RechargePage
from ..money.withdraw import WithdrawPage
from .loginlog import LoginLogPage
from ..report.user_statistics import UserStatisticsPage
from maindb.send_phone_message import send_message_password, send_message_fundspassword
from django.db.models import DecimalField
from ..models import TbMoneyCategories,TbSetting,TbRisklevellog
import json

def account_tab(self):
    baseinfo = AccoutBaseinfo(crt_user=self.crt_user)
    ls = [
        {'name': 'baseinfo',
         'label': _('Basic Info'),
         'com': 'com-tab-fields',
         'get_data': {
             'fun': 'get_row',
             'kws': {
                 'director_name': AccoutBaseinfo.get_director_name(),
                 'relat_field': 'accountid',
             }
         },
         'after_save': {
             'fun': 'update_or_insert'
         },
         'heads': baseinfo.get_heads(),
         'ops': baseinfo.get_operations()
         },
        {'name': 'balance_log',
         'label': '账目记录',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': AccountBalanceTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbBalancelog, self.crt_user),
         },
        {'name': 'backcard',
         'label': '银行卡',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': UserBankCard(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbBankcard, self.crt_user),
         },
        {'name': 'UserRecharge',
         'label': '充值记录',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': UserRecharge(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbRecharge, self.crt_user),
         },
        {'name': 'UserWithdraw',
         'label': '提现记录',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': UserWithdraw(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbWithdraw, self.crt_user),
         },

        {'name': 'account_ticket',
         'label': _('Ticket'),
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': AccountTicketTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbTicketmaster, self.crt_user),
         },
        {'name': 'account_login',
         'label': _('Login Log'),
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': AccountLoginTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbLoginlog, self.crt_user), },
        {'name': 'UserStatistics',
         'label': '会员统计',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': UserStatisticsTab(crt_user=self.crt_user).get_head_context(),
         'visible': True},
        {'name': 'MatchesStatistics',
         'label': '赛事统计',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': MatchesStatisticsTab(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbMatches, self.crt_user)},
    ]
    dc = {
        'account_tabs':evalue_container(ls)
    }
    dc.update(MatchesStatisticsPage.get_tabs(self.crt_user))
    return dc


class AccountPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '会员管理'

    def get_context(self):
        ctx = super().get_context()
        #ctx['tabs'] = account_tab(self)
        named_ctx =  account_tab(self)
        ctx['named_ctx'] = named_ctx
        
        return ctx

    class tableCls(ModelTable):
        model = TbAccount
        exclude=['password']
        #include = ['accountid', 'account', 'nickname', 'viplv', 'status', 'amount', 'bonusrate', 'agentamount',
                   #'isenablewithdraw', 'sumrechargecount', 'sumwithdrawcount', 'rechargeamount', 'withdrawamount',
                   #'createtime', 'source','accounttype','weight','groupid']
        fields_sort = ['accountid', 'account', 'nickname', 'createtime', 'source','weight','groupid', 'bonusrate', 'viplv', 'status',
                       'isenablewithdraw', 'amount', 'agentamount','betfullrecord',
                       'sumrechargecount', 'sumwithdrawcount', 'rechargeamount', 'withdrawamount','accounttype']

        class filters(RowFilter):
            names=['accounttype','groupid']
            range_fields = ['createtime']

        def inn_filter(self, query):
            """
            """
            #withdraw_query = TbWithdraw.objects.filter(accountid=OuterRef('pk')).values('accountid')
            #withdraw_query=withdraw_query.annotate(amount_sum=Sum('amount')).values('amount_sum')
            #query= query.annotate(
                #bbb=Count('tbrecharge__confirmamount'),
                #rechargeamount=Sum(Case(When(tbrecharge__status=2, then=F('tbrecharge__confirmamount') ),output_field=DecimalField(decimal_places=2, max_digits=8),  default=0)))
            #query=query.annotate(
                #withdrawamount= Subquery(
                    #withdraw_query
                                         #)
                       #)
                ##withdrawamount=Sum(Case(When(tbwithdraw__status=2, then=F('tbwithdraw__amount')), default=0)))
            #return query
            return query.extra(select={'betfullrecord':'SELECT SUM(TB_Betfullrecord.consumeamount) FROM TB_Betfullrecord WHERE TB_Betfullrecord.ConsumeStatus=1 AND TB_Betfullrecord.AccountID=TB_Account.AccountID',
                                       'rechargeamount':'SELECT SUM(TB_Recharge.ConfirmAmount) FROM TB_Recharge WHERE TB_Recharge.status=2 AND TB_Recharge.AccountID=TB_Account.AccountID',
                                       'withdrawamount':'SELECT SUM(TB_Withdraw.Amount) FROM TB_Withdraw WHERE TB_Withdraw.Status=2 AND TB_Withdraw.AccountID =TB_Account.AccountID'})
        #.annotate(rechargeamount_count=Count('tbrecharge__rechargeid',distinct=True),
                                  #withdrawamount_count=Count('tbwithdraw__withdrawid',distinct=True))\
                   #.annotate( rechargeamount_total= Sum(Case(When(tbrecharge__status=2, then=F('tbrecharge__confirmamount')), default=0)),
                              #withdrawamount_total=Sum(Case(When(tbwithdraw__status=2, then=F('tbwithdraw__amount')), default=0)) )\
                   #.annotate( rechargeamount= Case(When(withdrawamount_count=0,then= F('rechargeamount_total') ),output_field=DecimalField(decimal_places=2, max_digits=8) ,default =  F('rechargeamount_total') / F('withdrawamount_count') ),
                              #withdrawamount= Case(When(rechargeamount_count=0,then= F('withdrawamount_total') ),output_field=DecimalField(decimal_places=2, max_digits=8) ,default= F('withdrawamount_total')/ F('rechargeamount_count') ) 
                              #)
        
                   #.annotate(betfullrecord=Sum('tbbetfullrecord__consumeamount'))
        
                #rechargeamount=Sum(Case(When(tbrecharge__status=2, then=F('tbrecharge__confirmamount')), default=0))) \
                #.annotate(withdrawamount=Sum(Case(When(tbwithdraw__status=2, then=F('tbwithdraw__amount')), default=0)))

        def dict_row(self, inst):
            tmp = list(inst.account)
            tmp[0:-4] = '*' * (len(tmp) - 4)
            out_str = ''.join(tmp)
            
            return {
                'amount': str(inst.amount),
                'account': out_str,
                'rechargeamount': round( inst.rechargeamount or 0 ,2),
                'withdrawamount': round( inst.withdrawamount or 0,2),
                'betfullrecord':round( inst.betfullrecord or 0,2) # round( sum( [x.consumeamount for x in  inst.tbbetfullrecord_set.all()] ),2),
            }

        def dict_head(self, head):
            dc = {
                'accountid': 80,
                'account': 100,
                'nickname': 100,
                'viplv': 80,
                'amount': 100,
                'rechargeamount': 100,
                'withdrawamount': 100,
                'agentamount': 100,
                'status': 60,
                'createtime': 150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-switch-to-tab'
                head['ctx_name'] = 'account_tabs'
                head['tab_name'] = 'baseinfo'
            if head['name'] == 'status':
                head['editor'] = 'com-table-bool-shower'
            if head['name'] in ['agentamount', 'amount']:
                head['editor'] = 'com-table-digit-shower'
                head['digit'] = 2
            if head['name'] in ['bonusrate']:
                head['editor'] = 'com-table-digit-shower'
                head['digit'] = 3

            return head

        #def statistics(self, query):
            #dc = query.aggregate(total_amount=Sum('amount'), total_agentamount=Sum('agentamount'))
            #mapper = {
                #'amount': 'total_amount',
                #'agentamount': 'total_agentamount'
            #}
            #for k in dc:
                #dc[k] = str(round(dc.get(k) or 0, 2))
            #footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            #self.footer = footer
            #self.footer = ['合计'] + self.footer
            #return query.order_by('-pk')

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            return ctx

        def getExtraHead(self):
            return [{'name': 'rechargeamount', 'label': '充值金额'}, 
                    {'name': 'withdrawamount', 'label': '提现金额'},
                    {'name': 'betfullrecord', 'label': '提现限额'}]

        class search(SelectSearch):
            names = ['nickname']
            exact_names = ['accountid']

            def get_option(self, name):
                if name == 'accountid':
                    return {'value': name,
                            'label': '账户ID', }
                elif name == 'nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }

            def clean_search(self):
                if self.qf in ['accountid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()

        class sort(RowSort):
            names = ['nickname', 'account', 'amount', 'bonusrate', 'agentamount', 'createtime', 'sumrechargecount',
                     'rechargeamount', 'withdrawamount']

        def get_operation(self):
            modifyer = AccoutModifyAmount(crt_user=self.crt_user)
            betfullmodify = ModifyBetFullRecord(crt_user=self.crt_user)
            changeable_fields = self.permit.changeable_fields()
            return [
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '解冻', 'field': 'status',
                 'value': 1, 'confirm_msg': '确认解冻？', 'visible': 'status' in changeable_fields, },
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '冻结', 'field': 'status',
                 'value': 0, 'confirm_msg': '确认冻结？', 'visible': 'status' in changeable_fields},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '重置登录密码', 'field': 'password',
                 'value': 1, 'row_match': 'one_row', 'confirm_msg': '确认重置登录密码？',
                 'visible': 'password' in changeable_fields},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '重置资金密码', 'field': 'fundspassword',
                 'value': 1, 'row_match': 'one_row', 'confirm_msg': '确认重置资金密码？',
                 'visible': 'fundspassword' in changeable_fields},
                # selected_pop_set_and_save
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '调账',
                 'after_error':'scope.fs.showErrors(scope.errors)',
                 'fields_ctx': modifyer.get_head_context(), 'visible': 'amount' in changeable_fields},
                
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '调整限额',
                 'after_error':'scope.fs.showErrors(scope.errors)',
                 'fields_ctx': betfullmodify.get_head_context(), 'visible': 'amount' in changeable_fields},
                
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '允许提现', 'field': 'isenablewithdraw',
                 'value': 1, 'confirm_msg': '确认允许这些用户提现？', 'visible': 'isenablewithdraw' in changeable_fields},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '禁止提现', 'field': 'isenablewithdraw',
                 'value': 0, 'confirm_msg': '确认禁止这些用户提现？', 'visible': 'isenablewithdraw' in changeable_fields}
            ]


class AccoutBaseinfo(ModelFields):
    #'agentamount', 
    field_sort = ['account', 'nickname', 'amount', 'status', 'agent', 'verify', 'viplv', 'bonusrate',
                  'isenablewithdraw','accounttype', 'groupid','weight','risklevel','cashchannel','createtime']
    readonly = ['createtime', 'account', 'nickname', 'amount', 'agentamount']

    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw):
        if kw.get('accountid'):
            pk = kw.get('accountid')
        super().__init__(dc, pk, crt_user, nolimit, *args, **kw)
        self.orgin_risklevel= self.instance.risklevel

    def dict_head(self, head):
        if head['name'] == 'bonusrate':
            head['step'] = 0.001
        if head['name']=='weight':
            head['fv_rule']='range(0.001~500)'
        if head['name']=='risklevel':
            head['editor']='com-field-select'
            inst = TbSetting.objects.get(settingname='RiskControlLevel')
            head['options']=[{'value':x['Level'],'label':x['Memo']} for x in json.loads(inst.settingvalue)]
        if head['name']=='cashchannel':
            head['editor']='com-field-select'
            inst = TbSetting.objects.get(settingname='CashChannel')
            head['options']=[{'value':x['Channel'],'label':x['Memo']} for x in json.loads(inst.settingvalue)]            
        return head

    def dict_row(self, inst):
        tmp = list(inst.account)
        tmp[0:-4] = '*' * (len(tmp) - 4)
        out_str = ''.join(tmp)
        return {
            'account': out_str,
        }

    def clean_save(self):
        if self.kw.get('password') == 1:
            text_pswd, self.instance.password = gen_pwsd()
            send_message_password(self.instance.phone, text_pswd)
            return {'memo': '重置密码', }
        elif self.kw.get('fundspassword') == 1:
            text_pswd, self.instance.fundspassword = gen_money_pswd()
            send_message_fundspassword(self.instance.phone, text_pswd)
            return {'memo': '重置资金密码', }
        if 'risklevel' in self.changed_data:
            # 用户风险控制。
            risklevel = self.cleaned_data.get('risklevel')
            if risklevel > self.orgin_risklevel:
                # 升
                self.instance.isriskleveldown = 0
                TbRisklevellog.objects.create(upordown=1,createuser=self.crt_user.username,accountid=self.instance.accountid,oldrisklevel=self.orgin_risklevel,newrisklevel=risklevel,)
            else:
                # 降
                self.instance.isriskleveldown = 1
                TbRisklevellog.objects.create(upordown=2,createuser=self.crt_user.username,accountid=self.instance.accountid,oldrisklevel=self.orgin_risklevel,newrisklevel=risklevel,)
                

    class Meta:
        model = TbAccount
        exclude = ['actimestamp', 'agent', 'phone', 'gender', 'points', 'codeid', 'parentid',
                   'sumrechargecount', 'password']


class AccoutModifyAmount(ModelFields):
    field_sort = ['accountid', 'nickname', 'amount', 'add_amount','moenycategory']
    readonly = ['accountid', 'nickname', 'amount']

    class Meta:
        model = TbAccount
        fields = ['amount', 'nickname', 'accountid', 'amount', 'agentamount']

    def getExtraHeads(self):
        desp_options = [{'value':x.pk,'label':x.categoryname} for x in  TbMoneyCategories.objects.all()]
        return [
            {'name': 'add_amount', 'label': '调整金额', 'editor': 'number', 'required': True,'fv_rule': 'range(-50000~50000)', },
            {'name':'moenycategory','label':'类型','editor':'com-field-select','required':True,'options':desp_options},
        ]

    def clean_dict(self, dc):
        if dc.get('add_amount'):
            add_amount = Decimal(dc.get('add_amount', 0))
            self.before_amount = Decimal(dc['amount'])
            self.changed_amount = add_amount
            dc['amount'] = Decimal(dc['amount']) + add_amount
        return dc


    def extra_valid(self):
        dc = {}
        if self.cleaned_data.get('amount') + Decimal( self.kw.get('add_amount',0) )< 0:
            dc['add_amount'] = '叠加值使得余额小于0'
        return dc

    # def clean(self):

    # raise ValidationError('余额不能小于0')
    # return self.cleaned_data.get('amount')

    def clean_save(self):
        if 'add_amount' in self.kw:
            moenycategory_pk = self.kw.get('moenycategory')
            moenycategory_inst = TbMoneyCategories.objects.get(categoryid =moenycategory_pk)
            #cashflow, moenycategory = (1, 4) if self.changed_amount > 0 else (0, 34)
            cashflow, moenycategory =moenycategory_inst.cashflow,moenycategory_pk
            before_amount = self.instance.amount
            self.instance.amount = before_amount + Decimal(self.kw.get('add_amount', 0))
            TbBalancelog.objects.create(account=self.instance.account, beforeamount=self.before_amount,
                                        amount=abs( self.changed_amount), afteramount=self.instance.amount, creater='system',
                                        memo='调账', accountid=self.instance, categoryid_id=moenycategory,
                                        cashflow=cashflow)
            return {'memo': '调账', 'ex_before': {'amount': before_amount},
                    'ex_after': {'amount': self.instance.amount, }}


class ModifyBetFullRecord(ModelFields):
    field_sort = ['accountid', 'nickname', 'betfullrecord', 'add_amount']
    readonly = ['accountid', 'nickname',]
    
    class Meta:
        model = TbAccount
        fields = ['nickname', 'accountid']
    
    def clean_dict(self, dc):
        return dc
        #if dc.get('add_amount'):
            #self.add_amount = Decimal(dc.get('add_amount', 0))
            #dc.pop('betfullrecord',None)
           
            #self.changed_amount = add_amount
            #dc['amount'] = Decimal(dc['amount']) + add_amount
        #return dc    
    
    def dict_row(self, inst):
        return {
            'betfullrecord':round( sum( [x.consumeamount for x in  inst.tbbetfullrecord_set.all()] ),2),
        }
    
    def getExtraHeads(self):
        return [
            {'name': 'betfullrecord', 'label': '当前限额', 'editor': 'number', 'readonly':True },
            {'name': 'add_amount', 'label': '调整金额', 'editor': 'number', 'required': True,'fv_rule': 'range(-50000~50000)', }
        ]    
    
    def clean(self):
        add_amount = self.kw.get('add_amount')
        if not add_amount :
            self._errors['add_amount']= '调整值不能为0或者空'
        else:
            self. betfullrecord_list = TbBetfullrecord.objects.filter(accountid_id=self.kw.get('accountid'),consumestatus=1).order_by('tid')
            total =sum([x.consumeamount for x in  self. betfullrecord_list ] )
            if Decimal( add_amount ) + total < 0 :
                self._errors['add_amount']= '不能使限额小于0'
    
    def clean_save(self):
        if 'add_amount' in self.kw:
            add_amount = Decimal( self.kw.get('add_amount') )
            if add_amount < 0:
                for item in self.betfullrecord_list:
                    if item.consumeamount + add_amount <=0:
                        
                        item.content = item.content or '' + ';调整数-%s'%  item.consumeamount 
                        item.consumeamount = 0
                        item.consumestatus = 2
                        
                        item.save()
                        add_amount += item.consumeamount
                    else:
                        item.content =  item.content or '' + ';调整数%s'%  add_amount 
                        item.consumeamount += add_amount
                        item.save()
                        break
            else:
                TbBetfullrecord.objects.create(accountid_id=self.kw.get('accountid') ,consumeamount = add_amount,consumestatus=1,rftype=3,rfid=0,content='后台管理员限额调整')
                
            #cashflow, moenycategory = (1, 4) if self.changed_amount > 0 else (0, 34)
            #before_amount = self.instance.amount
            #self.instance.amount = before_amount + Decimal(self.kw.get('add_amount', 0))
            #TbBalancelog.objects.create(account=self.instance.account, beforeamount=self.before_amount,
                                        #amount=abs( self.changed_amount), afteramount=self.instance.amount, creater='system',
                                        #memo='调账', accountid=self.instance, categoryid_id=moenycategory,
                                        #cashflow=cashflow)
            after_amount = Decimal(self.kw.get('betfullrecord')) + add_amount
            return {'memo': '提现限额调整', 'ex_before': {'betfullrecord': self.kw.get('betfullrecord')},
                    'ex_after': {'betfullrecord': str(after_amount) , }}

class AccountTabBase(ModelTable):
    def __init__(self, *args, **kws):
        ModelTable.__init__(self, *args, **kws)
        accountid = self.kw.get('accountid')
        self.accountid = accountid

    def inn_filter(self, query):
        return query.filter(accountid=self.accountid)


class WithAccoutInnFilter(ModelTable):
    def inn_filter(self, query):
        query = super().inn_filter(query)
        if self.kw.get('accountid'):
            return query.filter(accountid=self.kw.get('accountid'))
        else:
            return query


class AccountBalanceTable(WithAccoutInnFilter, BalancelogPage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return BalancelogPage.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []


class UserBankCard(WithAccoutInnFilter, BankCard.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return BankCard.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []


class UserRecharge(WithAccoutInnFilter, RechargePage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return RechargePage.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []


class UserWithdraw(WithAccoutInnFilter, WithdrawPage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return WithdrawPage.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []


class AccountTicketTable(WithAccoutInnFilter, TicketMasterPage.tableCls):

    @classmethod
    def get_edit_director_name(cls):
        return TicketMasterPage.tableCls.get_edit_director_name()

    #def dict_head(self, head):
        #head = super().dict_head(head)

        #if head['name'] == 'ticketid':
            #head['editor'] = ''
        #return head
    
    class search(SelectSearch):
            #names = ['accountid__nickname']
            exact_names = ['orderid', 'tbticketstake__matchid']

            def get_option(self, name):

                if name == 'orderid':
                    return {'value': name,
                            'label': '订单编号', }
                #elif name == 'accountid__nickname':
                    #return {
                        #'value': name,
                        #'label': '昵称',
                    #}
                elif name == 'tbticketstake__matchid':
                    return {
                        'value': name,
                        'label': '比赛ID',
                    }

            def clean_search(self):
                if self.qf in ['ticketid', 'tbticketstake__matchid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()


class AccountLoginTable(WithAccoutInnFilter, LoginLogPage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return LoginLogPage.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []


class UserStatisticsTab(UserStatisticsPage.tableCls):
    class search(RowSearch):
        names = []


class MatchesStatisticsTab(MatchesStatisticsPage.tableCls):
    class search(RowSearch):
        names = []


director.update({
    'account': AccountPage.tableCls,
    'account.edit': AccoutBaseinfo,
    'account.base.edit': AccoutBaseinfo,
    'account.amount.edit': AccoutModifyAmount,
    'account.betfullmodify':ModifyBetFullRecord,
    
    'account.bankcard': UserBankCard,
    'account.bankcard.edit': BankCardForm,
    'account.UserRecharge': UserRecharge,
    'account.UserWithdraw': UserWithdraw,
    'account.log': AccountLoginTable,
    'account.ticketmaster': AccountTicketTable,
    'account.balancelog': AccountBalanceTable,
    'account.statistc': UserStatisticsTab,
    'account.matches_statistics': MatchesStatisticsTab
})

# permits = [('TbAccount', model_full_permit(TbAccount), model_to_name(TbAccount), 'model'),
# ('TbLoginlog', model_full_permit(TbLoginlog), model_to_name(TbLoginlog), 'model'),
# ('TbBalancelog', model_full_permit(TbBalancelog), model_to_name(TbBalancelog), 'model'),
# ('TbAccount.all', 'TbAccount;TbLoginlog;TbBalancelog;TbTicketmaster', '', 'set'),
# ]

# add_permits(permits)

page_dc.update({
    'account': AccountPage
})


def gen_pwsd():
    while True:
        pswd = get_str(length=6)
        # 不能全是字母，或者全是数字
        if not (re.search('^\d+$', pswd) or re.search('^\[a-zA-Z]+$', pswd)):
            break
    text_pswd = pswd
    m1 = hashlib.md5()
    m1.update(pswd.encode("utf-8"))
    pswd = m1.hexdigest()
    salt = ':69257765ACB34A08A6D0D978E9CF39ED'
    pswd_str = pswd + salt
    m2 = hashlib.md5()
    m2.update(pswd_str.encode("utf-8"))  # 参数必须是byte类型，否则报Unicode-objects must be encoded before
    pswd_db_str = m2.hexdigest().upper()
    return text_pswd, pswd_db_str

def gen_money_pswd(): 
    pswd = get_random_number(6)
    text_pswd = pswd
    m1 = hashlib.md5()
    m1.update(pswd.encode("utf-8"))
    pswd = m1.hexdigest()
    salt = ':69257765ACB34A08A6D0D978E9CF39ED'
    pswd_str = pswd + salt
    m2 = hashlib.md5()
    m2.update(pswd_str.encode("utf-8"))  # 参数必须是byte类型，否则报Unicode-objects must be encoded before
    pswd_db_str = m2.hexdigest().upper()
    return text_pswd, pswd_db_str

