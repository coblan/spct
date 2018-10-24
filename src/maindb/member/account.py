# encoding:utf-8
from __future__ import unicode_literals

import re

from django.db.models import Sum, Case, When, F
from django.utils.translation import ugettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter, director
from helpers.director.table.row_search import SelectSearch
from maindb.matches.matches_statistics import MatchesStatisticsPage
from maindb.money.balancelog import BalancelogPage
from ..models import TbAccount, TbBalancelog, TbLoginlog, TbTicketmaster, TbBankcard, TbRecharge, TbWithdraw, TbMatches
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


def account_tab(self):
    baseinfo = AccoutBaseinfo(crt_user=self.crt_user)
    ls = [
        {'name': 'baseinfo',
         'label': _('Basic Info'),
         'com': 'com_tab_fields',
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
         'com': 'com_tab_table',
         'par_field': 'accountid',
         'table_ctx': AccountBalanceTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbBalancelog, self.crt_user),
         },
        {'name': 'backcard',
         'label': '银行卡',
         'com': 'com_tab_table',
         'par_field': 'accountid',
         'table_ctx': UserBankCard(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbBankcard, self.crt_user),
         },
        {'name': 'UserRecharge',
         'label': '充值记录',
         'com': 'com_tab_table',
         'par_field': 'accountid',
         'table_ctx': UserRecharge(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbRecharge, self.crt_user),
         },
        {'name': 'UserWithdraw',
         'label': '提现记录',
         'com': 'com_tab_table',
         'par_field': 'accountid',
         'table_ctx': UserWithdraw(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbWithdraw, self.crt_user),
         },

        {'name': 'account_ticket',
         'label': _('Ticket'),
         'com': 'com_tab_table',
         'par_field': 'accountid',
         'table_ctx': AccountTicketTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbTicketmaster, self.crt_user),
         },
        {'name': 'account_login',
         'label': _('Login Log'),
         'com': 'com_tab_table',
         'par_field': 'accountid',
         'table_ctx': AccountLoginTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbLoginlog, self.crt_user), },
        {'name': 'UserStatistics',
         'label': '会员统计',
         'com': 'com_tab_table',
         'par_field': 'accountid',
         'table_ctx': UserStatisticsTab(crt_user=self.crt_user).get_head_context(),
         'visible': True},
        {'name': 'MatchesStatistics',
         'label': '赛事统计',
         'com': 'com_tab_table',
         'par_field': 'accountid',
         'table_ctx': MatchesStatisticsTab(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbMatches, self.crt_user)},
    ]
    return evalue_container(ls)


class AccountPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '会员管理'

    def get_context(self):
        ctx = super().get_context()
        ctx['tabs'] = account_tab(self)
        ctx['named_tabs'] = MatchesStatisticsPage.get_tabs(self.crt_user)
        
        return ctx

    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid', 'account', 'nickname', 'viplv', 'status', 'amount', 'bonusrate', 'agentamount',
                   'isenablewithdraw', 'sumrechargecount', 'sumwithdrawcount', 'rechargeamount', 'withdrawamount',
                   'createtime', 'source']
        fields_sort = ['accountid', 'account', 'nickname', 'createtime', 'source', 'bonusrate', 'viplv', 'status',
                       'isenablewithdraw', 'amount', 'agentamount',
                       'sumrechargecount', 'sumwithdrawcount', 'rechargeamount', 'withdrawamount']

        @classmethod
        def clean_search_args(cls, search_args):
            if not search_args.get('_sort'):
                search_args['_sort'] = '-withdrawamount'
            return search_args

        class filters(RowFilter):
            range_fields = ['createtime']

        def inn_filter(self, query):
            return query.annotate(
                rechargeamount=Sum(Case(When(tbrecharge__status=2, then=F('tbrecharge__confirmamount')), default=0))) \
                .annotate(withdrawamount=Sum(Case(When(tbwithdraw__status=2, then=F('tbwithdraw__amount')), default=0)))

        def dict_row(self, inst):
            tmp = list(inst.account)
            tmp[0:-4] = '*' * (len(tmp) - 4)
            out_str = ''.join(tmp)
            return {
                'amount': str(inst.amount),
                'account': out_str,
                'rechargeamount': inst.rechargeamount,
                'withdrawamount': inst.withdrawamount
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

        def statistics(self, query):
            dc = query.aggregate(total_amount=Sum('amount'), total_agentamount=Sum('agentamount'))
            mapper = {
                'amount': 'total_amount',
                'agentamount': 'total_agentamount'
            }
            for k in dc:
                dc[k] = str(round(dc.get(k) or 0, 2))
            footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            self.footer = footer
            self.footer = ['合计'] + self.footer
            return query

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            return ctx

        def getExtraHead(self):
            return [{'name': 'rechargeamount', 'label': '充值金额'}, {'name': 'withdrawamount', 'label': '提现金额'}]

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
                 'fields_ctx': modifyer.get_head_context(), 'visible': 'amount' in changeable_fields},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '允许提现', 'field': 'isenablewithdraw',
                 'value': 1, 'confirm_msg': '确认允许这些用户提现？', 'visible': 'isenablewithdraw' in changeable_fields},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '禁止提现', 'field': 'isenablewithdraw',
                 'value': 0, 'confirm_msg': '确认禁止这些用户提现？', 'visible': 'isenablewithdraw' in changeable_fields}
            ]


class AccoutBaseinfo(ModelFields):
    field_sort = ['account', 'nickname', 'amount', 'agentamount', 'status', 'agent', 'verify', 'viplv', 'bonusrate',
                  'isenablewithdraw', 'createtime']
    readonly = ['createtime', 'account', 'nickname', 'amount', 'agentamount']

    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw):
        if kw.get('accountid'):
            pk = kw.get('accountid')
        super().__init__(dc, pk, crt_user, nolimit, *args, **kw)

    def dict_head(self, head):
        if head['name'] == 'bonusrate':
            head['step'] = 0.001
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

    class Meta:
        model = TbAccount
        exclude = ['actimestamp', 'agent', 'phone', 'gender', 'points', 'codeid', 'parentid',
                   'sumrechargecount', 'password']


class AccoutModifyAmount(ModelFields):
    field_sort = ['accountid', 'nickname', 'amount', 'add_amount']
    readonly = ['accountid', 'nickname', 'amount']

    class Meta:
        model = TbAccount
        fields = ['amount', 'nickname', 'accountid', 'amount', 'agentamount']

    def getExtraHeads(self):
        return [
            {'name': 'add_amount', 'label': '调整金额', 'editor': 'number', 'required': True,'fv_rule': 'range(-50000~50000)', }
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
        if self.cleaned_data.get('amount') + Decimal( self.kw.get('add_amount') )< 0:
            dc['add_amount'] = '叠加值使得余额小于0'
        return dc

    # def clean(self):

    # raise ValidationError('余额不能小于0')
    # return self.cleaned_data.get('amount')

    def clean_save(self):
        if 'add_amount' in self.kw:
            cashflow, moenycategory = (1, 4) if self.changed_amount > 0 else (0, 34)
            before_amount = self.instance.amount
            self.instance.amount = before_amount + Decimal(self.kw.get('add_amount', 0))
            TbBalancelog.objects.create(account=self.instance.account, beforeamount=self.before_amount,
                                        amount=self.changed_amount, afteramount=self.instance.amount, creater='system',
                                        memo='调账', accountid=self.instance, categoryid_id=moenycategory,
                                        cashflow=cashflow)
            return {'memo': '调账', 'ex_before': {'amount': before_amount},
                    'ex_after': {'amount': self.instance.amount, }}


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

    def dict_head(self, head):
        head = super().dict_head(head)

        if head['name'] == 'ticketid':
            head['editor'] = ''
        return head
    
    class search(SelectSearch):
            #names = ['accountid__nickname']
            exact_names = ['orderid', 'tbticketstake__match_id']

            def get_option(self, name):

                if name == 'orderid':
                    return {'value': name,
                            'label': '订单编号', }
                #elif name == 'accountid__nickname':
                    #return {
                        #'value': name,
                        #'label': '昵称',
                    #}
                elif name == 'tbticketstake__match_id':
                    return {
                        'value': name,
                        'label': '比赛ID',
                    }

            def clean_search(self):
                if self.qf in ['ticketid', 'tbticketstake__match_id']:
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
