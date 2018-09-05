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

from .matches import admin, matches, ticket_master,matches_statistics

from .marketing import admin
from .report import user_statistics
from .report import report_channel
from .report import platform_profit

from .basic_data import odds_typegroup, league, teams, app_resource, currency
from .basic_data import admin_parameter
from .basic_data import banktypes
from .basic_data import paychannel

from .riskcontrol import admin
from . import update_cache

from .money import chargetype
from .money import recharge
from .money import withdraw
from .money import balancelog
from .money import agent_commission

from .admin_agent import agentuser
from .admin_agent import AgentCommission

