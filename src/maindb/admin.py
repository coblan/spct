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

from .matches import admin, matches, ticket_master,matches_statistics
from .matches import basketball_matches
from .matches import basketball_matches_statistics

from .marketing import admin
from .marketing import feedback
from .marketing import agent_qa

from .report import user_statistics
from .report import report_channel
from .report import platform_profit

from .basic_data import bet_type, league, teams, app_resource, currency
from .basic_data import banktypes
from .basic_data import paychannel
from .basic_data import basketball_league

from .riskcontrol import admin
from .riskcontrol import max_payout
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

from . import permit

from . import js_cfg
