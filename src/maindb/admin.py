# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage, ModelTable, model_dc, page_dc, ModelFields, FieldsPage, \
    TabPage, RowSearch, RowSort, RowFilter, director
from .models import TbAccount, TbBalancelog, TbLoginlog, TbTrans, TbTicketmaster
from .status_code import *
from .account_admin import AccountPage
from .member import admin_bankcard

from .admin_games import admin
# from .ticket_admin import TicketMasterPage
# from .money_admin import BalancelogPage,TransPage,ChannelPage

from .marketing import admin
from .report import admin
from .admin_basic_data import admin_oddtypegroup

# from .banner_admin import BannerPage
# from .admin_games import ViewTicketSingleByMatch,matchs

from .admin_riskcontrol import admin
from . import update_cache

from .money import chargetype
from .money import admin
from .money import recharge
from .money import withdraw


# Register your models here.
# class AccountPage(TablePage):
# class tableCls(ModelTable):
# model = TbAccount
# exclude = []
# fields_sort=['accountid','account','accounttype','username']

# def dict_row(self, inst):
# account_type = dict(ACCOUNT_TYPE)
# return {
# 'amount':unicode(inst.amount),
# 'accounttype': account_type.get(inst.accounttype)
# }

# class search(RowSearch):
# names=['account']

# class sort(RowSort):
# names=['account']


class AccountEditGroup(TabPage):
    def __init__(self, request):
        pk = request.GET.get('pk')
        if pk:
            self.account = TbAccount.objects.get(pk=pk)
        else:
            self.account = None
        TabPage.__init__(self, request)

    def get_tabs(self):
        tabs = [{'name': 'baseinfo', 'label': '基本信息', 'page_cls': AccountBaseInfoPage},
                {'name': 'balance_log', 'label': '账目记录', 'page_cls': AccountBalancePage},
                {'name': 'login_log', 'label': '登录记录', 'page_cls': AccountLoginPage},
                {'name': 'trans', 'label': '交易记录', 'page_cls': AccountTransPage},
                {'name': 'tickmaster', 'label': '投注记录', 'page_cls': AccountTicketPage}]
        # if self.jianfanginfo:
        # count = self.jianfanginfo.yinjizhenggai_set.count()
        # tabs =[{'name':'blockgroup_normal','label':'基本信息','page_cls':JianFangInfoFormPage},
        # {'name':'blockgroup_map','label':'应急整改(%s)'%count,'page_cls':YinJiTablePage}
        # ]
        # else:
        # tabs=[{'name':'blockgroup_normal','label':'基本信息','page_cls':JianFangInfoFormPage},]
        return tabs

    def get_label(self):
        return str(self.account)


class AccountBaseInfoPage(FieldsPage):
    class fieldsCls(ModelFields):
        class Meta:
            model = TbAccount
            exclude = []

        def dict_row(self, inst):
            return {
                'amount': str(inst.amount)
            }


class AccountLoginPage(TablePage):
    template = 'director/table_tab.html'

    class tableCls(ModelTable):
        model = TbLoginlog
        exclude = []

        def __init__(self, *args, **kws):
            ModelTable.__init__(self, *args, **kws)
            account_pk = self.kw.get('pk')
            account = TbAccount.objects.get(pk=account_pk)
            self.sn = account.accountsn

        def inn_filter(self, query):
            return query.filter(accountsn=self.sn)

        class filters(RowFilter):
            range_fields = [{'name': 'createtime', 'type': 'date'}]


page_dc.update({
    'maindb.account': AccountPage,
    'maindb.account.edit': AccountEditGroup,
    # 'maindb.ticketmaster':TicketMasterPage,
    # 'maindb.balancelog':BalancelogPage,
    # 'maindb.trans':TransPage,
    # 'maindb.channel':ChannelPage,
    # 'TbBanner':BannerPage
})

# admin.site.register(TbAccount)
