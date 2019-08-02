# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage, ModelTable, model_dc, page_dc, ModelFields, FieldsPage, \
    TabPage, RowSearch, RowSort, RowFilter, director
from .models import TbAccount, TbBalancelog, TbLoginlog, TbTicketmaster
from .status_code import *

from .member.account import AccountPage
from .member import bankcard
from .member import loginlog
from .member import operation_log
from .member import relevent_user
from .member import chum_user

from .matches import admin, matches, ticket_master,matches_statistics
from .matches import basketball_matches
from .matches import basketball_matches_statistics
from .matches import ajusttemplate
from .matches import event_match

from .marketing import admin
from .marketing import feedback
from .marketing import agent_qa
from .marketing import advertisement

from .report import user_statistics
from .report import report_channel
from .report import platform_profit
from .report import recharge_report
from .report import every_day
from .report import bet_analysis
from .report import active_record

from .basic_data import bet_type, league, teams, app_resource, currency
from .basic_data import banktypes
from .basic_data import paychannel
#from .basic_data import basketball_league
from .basic_data import sporttype
from .basic_data import teams_basketball


from .riskcontrol import admin
#from .riskcontrol import max_payout
from . import update_cache
from .riskcontrol import withdraw_limit
from .riskcontrol import paychannel_blackiprange
from .riskcontrol import area_blacklist
from .riskcontrol import paychannel_area_blacklist
from .riskcontrol import white_ip_rangelist

from .money import vip_paychannel
from .money import recharge
from .money import withdraw
from .money import balancelog

from .admin_agent import agentuser
from .admin_agent import agent_commission
from .riskcontrol import new_withdraw_limit

from . import admin_todolist
from . import permit

from . import js_cfg

from .yunwei import domain
from .yunwei import badurl

from .programer import admin
from helpers.director.base_data import site_cfg,field_map

site_cfg['inspect_dict']['field_map'] = field_map
