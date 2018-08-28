# encoding:utf-8

from __future__ import unicode_literals
from helpers.director.shortcut import page_dc
from helpers.director.engine import BaseEngine, page, fa, can_list, can_touch
from django.contrib.auth.models import User, Group
from helpers.func.collection.container import evalue_container
from helpers.maintenance.update_static_timestamp import js_stamp
from django.utils.translation import ugettext as _
from django.conf import settings
# from .js_translation import get_tr
# from maindb.models import TbBanner, TbAppversion, TbNotice, TbCurrency, TbQa, TbActivity, TbAppresource, TbAccount, TbLoginlog, \
# TbBalancelog, TbChargeflow, TbChannel, TbTicketmaster, TbMatches, TbRcFilter, TbRcLevel, TbRcUser, TbBlackuserlist, TbBlackuserlistLog, \
# Blackiprangelist, Whiteiplist, Whiteuserlist, TbWithdrawlimitlog, TbTeams,
from maindb.models import *
from . import permit


class PcMenu(BaseEngine):
    url_name = 'sportcenter'
    title = 'SportsCenter'
    brand = '<img src="/static/images/logo.png" style="height:46px">'
    mini_brand = '<img src="/static/images/logo2.png" style="height:46px">'

    @property
    def menu(self):
        crt_user = self.request.user
        menu = [
            {'label': _('DashBoard'), 'url': page('home'), 'icon': fa('fa-home'), 'visible': True},

            {'label': _('Marketing'), 'icon': fa('fa-image'), 'visible': True,
             'submenu': [
                 {'label': _('Banner'), 'url': page('TbBanner'), 'visible': can_touch(TbBanner, crt_user)},
                 {'label': _('App Package'), 'url': page('maindb.TbAppversion'),
                  'visible': can_touch(TbAppversion, crt_user), },
                 {'label': _('Notice'), 'url': page('maindb.TbNotice'), 'visible': can_touch(TbNotice, crt_user), },
                 {'label': _('Help'), 'url': page('maindb.TbQa'), 'visible': can_touch(TbQa, crt_user), },
                 {'label': _('Activity'), 'url': page('maindb.TBActive'), 'visible': can_touch(TbActivity, crt_user), },

             ]},

            {'label': _('Basic Info'), 'icon': fa('fa-book'), 'visible': True,
             'submenu': [
                 {'label': _('玩法设置'), 'url': page('maindb.TbOddstypeGroupPage'),
                  'visible': can_touch(TbOddstypegroup, crt_user), },
                 {'label': _('Currency'), 'url': page('maindb.TbCurrency'), 'visible': can_touch(TbCurrency, crt_user)},
                 {'label': _('league '), 'url': page('match.league'), 'visible': can_touch(TbTournament, crt_user)},
                 {'label': _('Teams'), 'url': page('maindb.teams'), 'visible': can_touch(TbTeams, crt_user), },
                 {'label': '银行卡类型', 'url': page('banktypes'), 'visible': can_touch(TbBanktypes, crt_user), },
                 {'label': '充值渠道', 'url': page('paychannel'), 'visible': can_touch(TbPaychannel, crt_user), },
                 {'label': _('AppResource'), 'url': page('AppResource'),
                  'visible': can_touch(TbAppresource, crt_user), },

             ]},

            {'label': _('Member'), 'icon': fa('fa-users'), 'visible': True,
             'submenu': [
                 {'label': _('Tb Account'), 'url': page('maindb.account'), 'visible': can_touch(TbAccount, crt_user), },
                 {'label': _('Tb Balance Log'), 'url': page('maindb.balancelog'),
                  'visible': can_touch(TbBalancelog, crt_user), },
                 {'label': _('Tb Login Log'), 'url': page('maindb.loginlog'),
                  'visible': can_touch(TbLoginlog, crt_user), },
                 {'label': _('银行卡管理'), 'url': page('BankCards'), 'visible': can_touch(TbAccount, crt_user), },
             ]},

            {'label': _('MoneyFlow'), 'icon': fa('fa-dollar'), 'visible': True,
             'submenu': [
                 # {'label': _('Charge Flow'), 'url': page('ChargeFlow'), 'visible': can_touch(TbChargeflow, crt_user), },
                 {'label': 'VIP充值渠道', 'url': page('ChargeType'), 'visible': can_touch(TbPaychanneljoinlevel, crt_user), },
                 {'label': '充值记录', 'url': page('Recharge'), 'visible': can_touch(TbRecharge, crt_user), },
                 {'label': '提现记录', 'url': page('Withdraw'), 'visible': can_touch(TbWithdraw, crt_user), },
                 # {'label':_('Tb Trans'),'url':page('maindb.trans'),'icon':fa('fa-home')},
                 # {'label': _('Tb Channel'), 'url': page('maindb.channel'), 'visible': can_touch(TbChannel, crt_user), },
             ]},

            {'label': _('Games'), 'icon': fa('fa-globe'), 'visible': True,
             'submenu': [
                 {'label': _('Tb TicketMaster'), 'url': page('maindb.ticketmaster'),
                  'visible': can_touch(TbTicketmaster, crt_user), },
                 {'label': _('Tb Match'), 'url': page('maindb.Matches'), 'visible': can_touch(TbMatches, crt_user), },
                 {'label': _('View TicketSingleByMatch'), 'url': page('maindb.MatchesSummary'),
                  'visible': can_touch(TbMatches, crt_user), },
                 # {'label':_('Odds'),'url':page('maindb.TbOdds'), 'visible': True,},

             ]},

            {'label': _('RiskControl'), 'icon': fa('fa-lock'), 'visible': True,
             'submenu': [
                 {'label': _('最大赔付'), 'url': page('sports.maxpayout'), 'visible': can_touch(TbLimit, crt_user), },
                 # {'label':_('Tb RC Filter'),'url':page('maindb.TbRcFilter'), 'visible': can_touch(TbRcFilter, crt_user),},
                 # {'label':_('Tb RC Level'),'url':page('maindb.TbRcLevel'), 'visible': can_touch(TbRcLevel, crt_user),},
                 # {'label':_('Tb RC User'),'url':page('maindb.TbRcUser'), 'visible': can_touch(TbRcUser, crt_user),},
                 {'label': _('Tb Blankuserlist'), 'url': page('maindb.TbBlackuserlist'),
                  'visible': can_touch(TbBlackuserlist, crt_user), },
                 {'label': '提现控制', 'url': page('Parameter'), 'visible': can_touch(TbTeams, crt_user), },
                 # {'label':_('Tb BlackuserlistLog'),'url':page('maindb.TbBlackuserlistLog'), 'visible': can_touch(TbBlackuserlistLog, crt_user),},

                 # {'label':_('Black IP Range'),'url':page('maindb.BlankipRangeList'), 'visible': can_touch(Blackiprangelist, crt_user),},
                 # {'label':_('White IP'),'url':page('maindb.WhiteIpList'), 'visible': can_touch(Whiteiplist, crt_user),},
                 # {'label':_('White User'),'url':page('maindb.Whiteuserlist'), 'visible': can_touch(Whiteuserlist, crt_user),},

                 # {'label':_('Tb Withdraw Limit Log'),'url':page('maindb.TbWithdrawlimitlog'), 'visible': can_touch(TbWithdrawlimitlog, crt_user)}
             ]},

            {'label': _('Report'), 'icon': fa('fa-bar-chart'), 'visible': True,
             'submenu': [
                 # {'label': _('Channel'), 'url': page('maindb.report.channel'),
                 # 'visible': can_touch(TbChannel, crt_user), },
                 {'label': _('Account'), 'url': page('maindb.report.account'),
                  'visible': can_touch(TbAccount, crt_user), },
             ]},

            {'label': _('User'), 'icon': fa('fa-user'), 'visible': True,
             'submenu': [
                 {'label': _('User'), 'url': page('jb_user'), 'visible': can_touch(User, crt_user)},
                 {'label': _('Role'), 'url': page('jb_group'), 'visible': can_touch(Group, crt_user)},
                 # {'label':'权限分组','url':page('group_human'),'visible':can_touch(Group)},
             ]},

        ]

        return menu

    def custome_ctx(self, ctx):
        ctx['js_stamp'] = js_stamp
        ctx['fast_config_panel'] = True
        # ctx['table_fun_config'] ={
        # 'detail_link': '详情', #'<i class="fa fa-info-circle" aria-hidden="true" title="查看详情"></i>'#,
        # }
        # lans = []
        # for k,v in settings.LANGUAGES:
        # lans.append({'value':k,'label':v})

        # ctx['site_settings']={
        # 'lans':lans,
        # 'tr':get_tr()
        # }

        return ctx


PcMenu.add_pages(page_dc)


class ProgramerAdmin(BaseEngine):
    url_name = 'ProgramerAdmin'
    brand = 'ProgramerAdmin'
    mini_brand = 'PA'

    @property
    def menu(self):
        menu = [
            {'label': _('DashBoard'), 'url': page('home'), 'icon': fa('fa-home')},
            {'label': '账号', 'url': page('user'), 'icon': fa('fa-users'), 'visible': can_list((User, Group)),
             'submenu': [
                 {'label': '账号管理', 'url': page('jb_user'), 'visible': can_touch(User)},
                 {'label': '角色管理', 'url': page('jb_group'), 'visible': can_touch(Group)},
                 {'label': '权限分组', 'url': page('group_human'), 'visible': can_touch(Group)},
             ]},
        ]
        return menu

    def custome_ctx(self, ctx):
        ctx['js_stamp'] = js_stamp
        ctx['fast_config_panel'] = True
        return ctx


ProgramerAdmin.add_pages(page_dc)
