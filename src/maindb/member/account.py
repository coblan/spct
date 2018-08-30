# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter, director
from maindb.money.balancelog import BalancelogPage
from maindb.report.report_account import ReportAccout
from ..models import TbAccount, TbBalancelog, TbLoginlog, TbTicketmaster
from helpers.director.shortcut import model_to_name, model_full_permit, add_permits
from helpers.func.collection.container import evalue_container
from helpers.director.access.permit import can_touch
from helpers.func.random_str import get_str
import hashlib
from decimal import Decimal
from ..matches.ticket_master import TicketMasterPage
from ..member.bankcard import BankCard, BankCardForm
from ..money.recharge import RechargePage
from ..money.withdraw import WithdrawPage
from .loginlog import LoginLogPage


# Register your models here.

class AccountPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '会员管理'

    def get_context(self):
        ctx = TablePage.get_context(self)
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
             'visible': True,
             },
            {'name': 'UserRecharge',
             'label': '充值记录',
             'com': 'com_tab_table',
             'par_field': 'accountid',
             'table_ctx': UserRecharge(crt_user=self.crt_user).get_head_context(),
             'visible': True,
             },
            {'name': 'UserWithdraw',
             'label': '提现记录',
             'com': 'com_tab_table',
             'par_field': 'accountid',
             'table_ctx': UserWithdraw(crt_user=self.crt_user).get_head_context(),
             'visible': True,
             },

            {'name': 'account_ticket',
             'label': _('Ticket'),
             'com': 'com_tab_table',
             'par_field': 'accountid',
             'table_ctx': AccountTicketTable(crt_user=self.crt_user).get_head_context(),
             'visible': can_touch(TbTicketmaster, self.crt_user),
             },
            {'name': 'account_profit',
             'label': '亏盈统计',
             'com': 'com_tab_table',
             'par_field': 'accountid',
             'table_ctx': AccountProfitTable(crt_user=self.crt_user).get_head_context(),
             'visible': True},
            {'name': 'account_login',
             'label': _('Login Log'),
             'com': 'com_tab_table',
             'par_field': 'accountid',
             'table_ctx': AccountLoginTable(crt_user=self.crt_user).get_head_context(),
             'visible': can_touch(TbLoginlog, self.crt_user), }
        ]
        ctx['tabs'] = evalue_container(ls)
        return ctx

    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid', 'account', 'nickname', 'viplv', 'status', 'amount', 'bonusrate', 'agentamount',
                   'isenablewithdraw', 'sumrechargecount','createtime']

        class filters(RowFilter):
            range_fields = ['createtime']

        def dict_row(self, inst):
            tmp = list(inst.account)
            tmp[0:-4] = '*' * (len(tmp) - 4)
            out_str = ''.join(tmp)
            return {
                'amount': str(inst.amount),
                'account': out_str
                # 'accounttype': account_type.get(inst.accounttype)
            }

        def dict_head(self, head):
            dc = {
                'accountid': 80,
                'account': 100,
                'nickname': 100,
                'viplv': 80,
                'amount': 100,
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

        class search(RowSearch):
            names = ['accountid', 'nickname']

        class sort(RowSort):
            names = ['account', 'amount', 'bonusrate', 'agentamount', 'createtime', 'sumrechargecount']

        def get_operation(self):
            modifyer = AccoutModifyAmount(crt_user=self.crt_user)
            return [
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '启用', 'field': 'status',
                 'value': 1, 'confirm_msg': '确认启用？', },
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '禁用', 'field': 'status',
                 'value': 0, 'confirm_msg': '确认禁用？'},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '重置登录密码', 'field': 'password',
                 'value': 1, 'row_match': 'one_row', 'confirm_msg': '确认重置登录密码？'},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '重置资金密码', 'field': 'fundspassword',
                 'value': 1, 'row_match': 'one_row', 'confirm_msg': '确认重置资金密码？'},
                {'fun': 'selected_pop_set_and_save', 'editor': 'com-op-btn', 'label': '加减余额',
                 'fields_ctx': modifyer.get_head_context()},
            ]


class AccoutBaseinfo(ModelFields):
    field_sort = ['account', 'nickname', 'amount', 'status', 'agent', 'verify', 'viplv', 'createtime']
    readonly = ['createtime', 'account', 'nickname', 'amount']

    def clean_dict(self, dc):
        if dc.get('password') == 1:
            dc['password'] = gen_pwsd()
        if dc.get('fundspassword') == 1:
            dc['fundspassword'] = gen_pwsd()
        super().clean_dict(dc)
        return dc

    class Meta:
        model = TbAccount
        exclude = ['actimestamp', 'agent', 'phone', 'gender', 'points', 'codeid', 'parentid',
                   'sumrechargecount']


class AccoutModifyAmount(ModelFields):
    field_sort = ['accountid', 'nickname', 'amount', 'add_amount']
    readonly = ['accountid', 'nickname', 'amount']

    class Meta:
        model = TbAccount
        fields = ['amount', 'nickname', 'accountid', 'amount', 'agentamount']

    def getExtraHeads(self):
        return [
            {'name': 'add_amount', 'label': '调整金额', 'editor': 'number', 'fv_rule': 'range(-50000~50000)', }
        ]

    def clean_dict(self, dc):
        if dc.get('add_amount'):
            add_amount = Decimal(dc.get('add_amount', 0))
            self.before_amount = Decimal(dc['amount'])
            self.changed_amount = add_amount
            dc['amount'] = Decimal(dc['amount']) + add_amount
        return dc

    def save_form(self):
        super().save_form()
        if 'amount' in self.changed_data:
            cashflow = 1 if self.changed_amount > 0 else 0
            TbBalancelog.objects.create(account=self.instance.account, beforeamount=self.before_amount,
                                        amount=self.changed_amount, afteramount=self.instance.amount, creater='system',
                                        memo='调账', accountid=self.instance.accountid, categoryid=4, cashflow=cashflow)

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
    class search(RowSearch):
        names = []


class UserBankCard(WithAccoutInnFilter, BankCard.tableCls):
    class search(RowSearch):
        names = []


class UserRecharge(WithAccoutInnFilter, RechargePage.tableCls):
    class search(RowSearch):
        names = []


class UserWithdraw(WithAccoutInnFilter, WithdrawPage.tableCls):
    class search(RowSearch):
        names = []


class AccountTicketTable(WithAccoutInnFilter, TicketMasterPage.tableCls):
    def dict_head(self, head):
        head = super().dict_head(head)

        if head['name'] == 'ticketid':
            head['editor'] = ''
        return head


class AccountLoginTable(WithAccoutInnFilter, LoginLogPage.tableCls):
    class search(RowSearch):
        names = []


class AccountProfitTable(WithAccoutInnFilter, ReportAccout.tableCls):
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
    'account.profit': AccountProfitTable
})

permits = [('TbAccount', model_full_permit(TbAccount), model_to_name(TbAccount), 'model'),
           ('TbLoginlog', model_full_permit(TbLoginlog), model_to_name(TbLoginlog), 'model'),
           ('TbBalancelog', model_full_permit(TbBalancelog), model_to_name(TbBalancelog), 'model'),
           ('TbAccount.all', 'TbAccount;TbLoginlog;TbBalancelog;TbTicketmaster', '', 'set'),
           ]

add_permits(permits)

page_dc.update({
    'maindb.account': AccountPage
})


def gen_pwsd():
    pswd = get_str(length=6)
    print(pswd)
    m1 = hashlib.md5()
    m1.update(pswd.encode("utf-8"))
    pswd = m1.hexdigest()
    salt = ':69257765ACB34A08A6D0D978E9CF39ED'
    pswd_str = pswd + salt
    m2 = hashlib.md5()
    m2.update(pswd_str.encode("utf-8"))  # 参数必须是byte类型，否则报Unicode-objects must be encoded before
    pswd_db_str = m2.hexdigest().upper()
    return pswd_db_str
