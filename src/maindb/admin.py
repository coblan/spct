# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from django.conf import settings
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
from .member import userlog
from .member import vipbonus

from .matches import admin, matches, ticket_master,matches_statistics
from .matches import basketball_matches
from .matches import basketball_matches_statistics
from .matches import ajusttemplate
from .matches import event_match
from .matches import event_match1
from .matches import mapping_setting

from .marketing import admin
from .marketing import feedback
from .marketing import agent_qa
from .marketing import advertisement
from .marketing import activity_record
from .marketing import vip_gift

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
from .basic_data import admin_paychanel_group


from .riskcontrol import admin
#from .riskcontrol import max_payout
from . import update_cache
from .riskcontrol import withdraw_limit
from .riskcontrol import paychannel_blackiprange
from .riskcontrol import area_blacklist
from .riskcontrol import paychannel_area_blacklist
from .riskcontrol import white_ip_rangelist
from .riskcontrol import new_withdraw_limit

from .money import vip_paychannel
from .money import recharge

if getattr(settings,'OPEN_SECRET',False):
    from .money import withdraw
    
from .money import balancelog

from .admin_agent import agentuser
from .admin_agent import agent_commission


from . import admin_todolist
from . import permit
from . import admin_administrator_ip
from . admin_backend import login_log
from . admin_backend import admin_google_code

from . import js_cfg
from . import login

from .yunwei import domain
from .yunwei import badurl
from . import kefu
from . import userex

from .programer import admin
from helpers.director.base_data import inspect_dict,field_map

inspect_dict['field_map'] = field_map

if getattr(settings,'OPEN_SECRET',False):
    from . ag import ag_account
    from . ag import profitloss
    from . ag import gamemoneyinfo
    from . ag import gamemoneyoutinfo
    
    from . sport import sport_account
    from . sport import sport_profitloss
    from . sport import sport_money_in_info
    from . sport import sport_money_out
    
    from . city import city_account
    from . city import city_profitloss
    from . city import city_money_in
    from . city import city_money_out
    
    from . im import im_account
    from . im import im_esb_account
    from . im import im_money_in
    from . im import im_money_out
    from . im import im_profitloss
    
    from . rg import rg_account
    from . rg import rg_profitloss
    from . rg import rg_money_in
    from . rg import rg_money_out
    
    from . pt import pt_account
    from . pt import pt_money_in
    from . pt import pt_money_out
    from . pt import pt_profitloss
    
    from .sg import sg_account
    from .sg import sg_money_in
    from .sg import sg_money_out
    from .sg import sg_profitloss
    
    from . part3.ebet import ebet_account,ebet_money_in,ebet_money_out,ebet_profitloss
    from . part3.pp import pp_account,pp_money_in,pp_money_out,pp_profitloss
    from . part3.imchess import imchess_account,imchess_money_in,imchess_money_out,imchess_profitloss
    from . part3.vr import vr_account,vr_money_in,vr_money_out,vr_profitloss