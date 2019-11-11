# encoding:utf-8

from __future__ import unicode_literals
from helpers.director.shortcut import page_dc
from helpers.director.engine import BaseEngine, page, fa, can_list, can_touch
from django.contrib.auth.models import User, Group
from helpers.func.collection.container import evalue_container
from helpers.maintenance.update_static_timestamp import js_stamp
from django.utils.translation import ugettext as _
from django.conf import settings
from helpers.director.access.permit import has_permit
# from .js_translation import get_tr
# from maindb.models import TbBanner, TbAppversion, TbNotice, TbCurrency, TbQa, TbActivity, TbAppresource, TbAccount, TbLoginlog, \
# TbBalancelog, TbChargeflow, TbChannel, TbTicketmaster, TbMatches, TbRcFilter, TbRcLevel, TbRcUser, TbBlackuserlist, TbBlackuserlistLog, \
# Blackiprangelist, Whiteiplist, Whiteuserlist, TbWithdrawlimitlog, TbTeams,
from maindb.models import *
from . import permit
from django.utils import timezone
from maindb.admin_todolist import get_todolist_catlist

class PcMenu(BaseEngine):
    url_name = 'sportcenter'
    title = 'SportsCenter'
    brand = '<img src="/static/images/logo.png" style="height:46px">'
    mini_brand = '<img src="/static/images/logo2.png" style="height:46px">'
    need_staff=True
    access_from_internet=True
    @property
    def menu(self):
        crt_user = self.request.user
        todo_cat_list = get_todolist_catlist()
        menu = [
            {'label': _('DashBoard'), 'url': page('home'), 'icon': fa('fa-home'), 'visible': True},
            {'label': '待办事项', 'url': page('todolist'), 'icon': fa('fa-clock-o'), 'visible': len(todo_cat_list) != 0 },
           
            {'label': _('Member'), 'icon': fa('fa-users'), 'visible': True,
             'submenu': [
                {'label': _('Tb Account'), 'url': page('account'), 'visible': can_touch(TbAccount, crt_user), },
                {'label': _('Tb Balance Log'), 'url': page('balancelog'),
                 'visible': can_touch(TbBalancelog, crt_user), },
                {'label': _('Tb Login Log'), 'url': page('loginlog'),
                 'visible': can_touch(TbLoginlog, crt_user), },
                {'label': _('银行卡管理'), 'url': page('bankcards'), 'visible': can_touch(TbBankcard, crt_user), },
                {'label': '关联用户', 'url': page('ReleventUser'), 'visible': has_permit( crt_user,'member.relevent_user'), },
                #{'label': '流失用户', 'url': page('chum_user'), 'visible': has_permit( crt_user,'member.chum_user'), },
                {'label':'用户日志','url':page('userlog'),'visible':can_touch(TbUserLog,crt_user)},
                {'label': '会员关怀', 'url': page('kefupage'), 'icon': fa('fa-clock-o'),  'visible': has_permit( crt_user,'member.kefu')},
                 
             ]},
            {'label': '市场活动', 'icon': fa('fa-image'), 'visible': True,
             'submenu': [
                 {'label': _('Banner'), 'url': page('banner'), 'visible': can_touch(TbBanner, crt_user)},
                 {'label': _('App Package'), 'url': page('app_package'),
                  'visible': can_touch(TbAppversion, crt_user), },
                 {'label': _('Notice'), 'url': page('notice'), 'visible': can_touch(TbNotice, crt_user), },
                 {'label': '代理公告', 'url': page('agentnotice'), 'visible': can_touch(TbAgentnotice, crt_user), },
                {'label': '代理QA', 'url': page('agent_qa'), 'visible': can_touch(TbAgentqa, crt_user), },
                 
                 {'label': _('Help'), 'url': page('help'), 'visible': can_touch(TbQa, crt_user), },
                 
                {'label': '优惠活动', 'url': page('activity_v2'), 'visible': can_touch(TbActivityV2, crt_user), },
                {'label':'活动记录','url':page('activity_record'),'visible':can_touch(TbActivityRecord,crt_user)},
                #{'label': _('Activity'), 'url': page('activity'), 'visible': can_touch(TbActivity, crt_user), },
                {'label': '用户留言', 'url': page('feedback'), 'visible': can_touch(TbAgentleavemsg, crt_user), },
                {'label': '用户排行', 'visible': lambda liveitem:liveitem['submenu'], 
                 'submenu': [
                     {'label': '虚拟用户', 'url': page('rankuser'), 'visible': can_touch(TbUserConst, crt_user), },
                     {'label': '虚拟排行', 'url': page('rank'), 'visible': can_touch(TbUserRank, crt_user), },                      
                     ],},
                {'label': '红利发放', 'url': page('bonuspage'),'visible': can_touch(TbBonuslog, crt_user), },
                {'label':'启动广告','url':page('advertise'),'visible':can_touch(TbAdvertisement,crt_user)},
               
                
             ]},
            {'label': _('Basic Info'), 'icon': fa('fa-book'), 'visible': True,
             'submenu': [
                 {'label': '运动类型', 'url': page('sportstype'), 'visible': can_touch(TbSporttypes, crt_user), },
                 {'label': '联赛资料', 'url': page('league'), 'visible': can_touch(TbTournament, crt_user)},
                 #{'label': '篮球联赛资料', 'url': page('basketball_league'), 'visible': can_touch(TbTournament, crt_user)},
                 #{'label': '足球队资料', 'url': page('teams'), 'visible': can_touch(TbTeams, crt_user), },
                  #{'label': '篮球队资料', 'url': page('teams_basketball'), 'visible': can_touch(TbTeamsBasketball, crt_user), },
                 
                 #{'label': _('玩法设置'), 'url': page('bet_type'), 'visible': can_touch(TbOddstypegroup, crt_user), },
                 {'label': '玩法设置', 'url': page('usermarket'), 'visible': can_touch(TbMarkets, crt_user), },
                 {'label':'充值渠道组','url':page('TbPaychannelgroup'),'visible':can_touch(TbPaychannelgroup,crt_user)},
                 {'label': '充值渠道', 'url': page('paychannel'), 'visible': can_touch(TbPaychannel, crt_user), },
                  {'label': 'VIP充值渠道', 'url': page('vip_paychannel'),
                  'visible': can_touch(TbPaychanneljoinlevel, crt_user), },
                 {'label': '银行卡类型', 'url': page('banktypes'), 'visible': can_touch(TbBanktypes, crt_user), },
                 {'label': _('AppResource'), 'url': page('app_resource'),
                  'visible': can_touch(TbAppresource, crt_user), },
                {'label': _('Currency'), 'url': page('currency'), 'visible': can_touch(TbCurrency, crt_user)},
               
            
             ]},

            {'label': _('MoneyFlow'), 'icon': fa('fa-dollar'), 'visible': True,
             'submenu': [
                 {'label': '充值记录', 'url': page('recharge'), 'visible': can_touch(TbRecharge, crt_user), },
                 {'label': '提现记录', 'url': page('withdraw'), 'visible': can_touch(TbWithdraw, crt_user), }
             ]},

            {'label': _('Games'), 'icon': fa('fa-globe'), 'visible': True,
             'submenu': [
                 {'label': '赛事列表', 'url': page('matches'), 'visible': can_touch(TbMatch, crt_user), },
                 {'label': '赛事统计', 'url': page('matches_statistics'),
                  'visible': can_touch(TbMatch, crt_user), },
                 {'label': '注单列表', 'url': page('tickets'),
                  'visible': can_touch(TbTicketmaster, crt_user), },
                {'label':'调水模板','url':page('adjusttemplate'),'visible':can_touch(TbAdjusttemplate,crt_user)},
                {'label':'赛事匹配','url':page('web_match_data')},
                {'label':'赛事匹配V2','url':page('web_match_data1')}
                 
             ]},

            {'label': _('RiskControl'), 'icon': fa('fa-lock'), 'visible': True,
             'submenu': [
                #{'label': '足球最大赔付', 'url': page('maxpayout'), 'visible': can_touch(TbMaxpayout, crt_user), },
                #{'label': '篮球最大赔付','url': page('maxpayout_basketball'),'visible': can_touch(TbMaxpayoutBasketball, crt_user)}, 
                {'label': '提现控制', 'url': page('parameterinfo'), 'visible': can_touch(TbParameterinfo, crt_user), },
                {'label':'登录IP黑名单','url':page('blackip_range'), 'visible': can_touch(Blackiprangelist, crt_user),},
                {'label': '登录地区黑名单', 'url': page('area_blacklist'), 'visible': can_touch(TbAreablacklist, crt_user), },
                {'label':'充值用户黑名单','url':page('Paychannelblackaccount'),'visible': can_touch(TbPaychannelblackaccount, crt_user),},
                {'label': '充值IP黑名单', 'url': page('paychannel_blackip'),'visible': can_touch(TbPaychannelblackiprange, crt_user), },
                {'label': '充值地区黑名单', 'url': page('paychannel_area_blacklist'),
                 'visible': can_touch(TbRechargeareablacklist, crt_user), },
                {'label':_('White IP'),'url':page('white_ip_rangelist'), 'visible': can_touch(TbWhiteiprangelist, crt_user),},
                {'label':'用户白名单','url':page('white_users'), 'visible': can_touch(Whiteuserlist, crt_user),},
                #{'label': '联赛组水位', 'url': page('LeagueGroupPage'), 'visible': can_touch(TbLeagueGroup, crt_user), },
                {'label': '参数设置', 'url': page('ParameterPage'),'visible': has_permit(crt_user, 'risk.parameter'),},
                #{'label': '数据源维护', 'url': page('sourececontrol'),'visible': has_permit(crt_user, 'risk.parameter'),},
                {'label': '用户限额分组', 'url': page('limitusergroup'),'visible': can_touch(TbLimitusergroup, crt_user),},
                {'label': '风险控制设置', 'url': page('RiskcontrolSetting'),'visible': has_permit(crt_user, 'risk.RiskcontrolSetting'),},
                {'label':'联赛风控','url':page('newleaguegroup'),'visible':can_touch(TbLeagueGroup,crt_user)},
                
             ]},

            {'label': '报表中心', 'icon': fa('fa-bar-chart'), 'visible': True,
             'submenu': [
                {'label': '会员统计', 'url': page('user_statistics'),
                  'visible': has_permit(crt_user, 'member_statistic'), },
                {'label': '平台亏盈', 'url': page('platform_profit'),
                  'visible': has_permit(crt_user, 'platform_profit'), },
                {'label':'充值安全统计','url':page('recharge_reports'),'visible': has_permit(crt_user, 'report.recharge_reports')},
                {'label': '每日报表', 'url': page('everyday_report'),
                  'visible': can_touch(TbTrendstatistics, crt_user), },
                {'label':'投注分析','url':page('bet_analysis'),'visible':has_permit(crt_user,'report.betAnalysis')},
                {'label':'活动记录','url':page('activityrecord'),},
             ]},
            
            {'label': '代理系统', 'icon': fa('fa-street-view'), 'visible': lambda liveitem:liveitem['submenu'],
             'submenu': [
                 {'label': '代理用户', 'url': page('agent_user'),'visible': has_permit(crt_user, 'agent'), },
                 {'label': '代理佣金', 'url': page('agent_commission'),'visible': can_touch(TbAgentcommission, crt_user), },
             ]},
            
             {'label': 'AG系统', 'icon': fa('fa-street-view'), 'visible': lambda liveitem:liveitem['submenu'] and getattr(settings,'OPEN_SECRET',False) ,
             'submenu': [
                {'label': '用户列表', 'url': page('agaccount'),'visible': can_touch(TbAgaccount, crt_user), },
                {'label':'投注列表','url':page('agprofitloss'),'visible':can_touch(TbAgprofitloss,crt_user)},
                {'label':'资金转入AG','url':page('gamemoneyininfo'),'visible':can_touch(TbGamemoneyininfo,crt_user)},
                {'label':'资金转出AG','url':page('gamemoneyoutinfo'),'visible':can_touch(TbGamemoneyoutinfo,crt_user)},
             ]},
            {'label': '沙巴系统', 'icon': fa('fa-street-view'), 'visible': lambda liveitem:liveitem['submenu'] and getattr(settings,'OPEN_SECRET',False) ,
             'submenu': [
                {'label': '用户列表', 'url': page('sportaccount'),'visible': can_touch(TbSportaccount, crt_user), },
                {'label':'投注列表','url':page('sportprofitloss'),'visible':can_touch(TbSportprofitloss,crt_user)},
                {'label':'资金转入','url':page('sportmoneyinfo'),'visible':can_touch(TbSportmoneyininfo,crt_user)},
                {'label':'资金转出','url':page('sportmoneyout'),'visible':can_touch(TbSportmoneyoutinfo,crt_user)},
             ]},
             
            {'label': '系统管理', 'icon': fa('fa-user'), 'visible': True,
             'submenu': [
                 {'label': _('User'), 'url': page('jb_user'), 'visible': can_touch(User, crt_user)},
                 {'label': _('Role'), 'url': page('jb_group'), 'visible': can_touch(Group, crt_user)},
                 {'label': '操作日志', 'url': page('operation_log'), 'visible': can_touch(TbOperationlog, crt_user)},
                 {'label':'异常地址','url':page('badurl')},
                 {'label':'账号扩展信息','url':page('userex'),'visible':can_touch(TbUserex,crt_user)},
                 {'label':'后台登录IP白名单','url':page('admin_ip'),'visible':can_touch(TbBackendwhiteip,crt_user)},
                 {'label':'后台登录日志','url':page('bacnend_loginlog'),'visible':can_touch(TbBackendloginlog,crt_user)}
                 # {'label':'权限分组','url':page('group_human'),'visible':can_touch(Group)},
             ]},

        ]

        return menu

    def custome_ctx(self, ctx):
        ctx['js_stamp'] = js_stamp
        ctx['fast_config_panel'] = True
        if 'extra_js' not in ctx:
            ctx['extra_js'] = []
        if 'maindb' not in ctx['extra_js']:
            ctx['extra_js'].append('maindb')
        if 'notify' not in ctx['extra_js']:
            ctx['extra_js'].append('notify')
        if 'init_express' not in ctx:
            #ws://localhost:15674/ws   v1_user  v1_user   /exchange/mytest/test
            ctx['init_express'] = '''(function(){
            window.alert_audio = new Audio("/static/mp3/alert.mp3")
            window.alert_audio.loop=true
            
            ex.stompInit({url:"%(url)s",user:"%(user)s",pswd:"%(pswd)s"});
            ex.stompListen("/exchange/center.topic/backend.timely.message",function(data){
                console.log(data.body)
                var msg_dc = JSON.parse(data.body)
                if(msg_dc.EventType==1){
                    rootStore.$emit("todolist_updated")
                }
            })
            })()
            '''%{'url':settings.WEBSOCKET.get('url'),'user':settings.WEBSOCKET.get('user'),'pswd':settings.WEBSOCKET.get('pswd')}
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
    
    def get_head_bar_data(self, request):
        dc = super().get_head_bar_data(request)
        header_bar_widgets = dc.get('header_bar_widgets')
        cat_list = get_todolist_catlist()
        if cat_list:
            count = TbTodolist.objects.filter(status=0,category__in = cat_list).count()
            header_bar_widgets = [
                {'editor': 'com-head-bell-msg', 'link':'/pc/todolist','count':count,'lasttime':timezone.now().strftime('%Y-%m-%d %H:%M:%S'),'init_express':'''(function(){
                rootStore.$on('todolist_updated',()=>{
                    ex.director_call("todolist.hasnew_todolist",{lasttime:scope.head.lasttime}).then((resp)=>{
                        scope.head.count = resp.count
                        if(resp.hasnew){
                           scope.head.lasttime=resp.lasttime
                           window.alert_audio.play()
                           
                            cfg.notify(resp.title,
                            {
                            requireInteraction:true,
                            tag:'jb_todolist',
                            data: {
                                url: '%(self_url)s/pc/todolist'
                            },
                            onclose:function(){
                                window.alert_audio.pause();
                            }
                            })
                        }
                    })
                })
                
                rootStore.$on('todolist_count_updated',()=>{
                    ex.director_call('todolist.get_counter').then(count=>{
                        scope.head.count = count
                    })
                })
                
                })()
                '''%{'self_url':settings.SELF_URL}
                   },
            ] + header_bar_widgets
            dc['header_bar_widgets'] = header_bar_widgets
        return dc


PcMenu.add_pages(page_dc)


class ProgramerAdmin(BaseEngine):
    url_name = 'ProgramerAdmin'
    brand = 'ProgramerAdmin'
    mini_brand = 'PA'
    need_staff = True
    access_from_internet=True
    @property
    def menu(self):
        menu = [
            {'label': '玩法组', 'url': page('marketgroup'), 'icon': fa('fa-superpowers')},
            {'label': '玩法', 'url': page('marketpage'), 'icon': fa('fa-superpowers')},
            {'label': '投注项', 'url': page('outcome'), 'icon': fa('fa-superpowers')},
            {'label':'列表玩法','url':page('marketsport'),'icon':fa('fa-superpowers')},
        ]
        return menu

    def custome_ctx(self, ctx):
        ctx['js_stamp'] = js_stamp
        ctx['fast_config_panel'] = True
        return ctx

ProgramerAdmin.add_pages(page_dc)

class YunweiEngin(BaseEngine):
    url_name = 'yunwei'
    brand = 'yunwei'
    mini_brand = 'YW'
    need_staff=False
    access_from_internet=True
    @property
    def menu(self):
        crt_user = self.request.user
        menu = [
            {'label': '域名管理', 'url': page('domain'), 'icon': fa('fa-superpowers'),'visible':can_touch(TbDomain,crt_user)}
            
        ]
        return menu

    def custome_ctx(self, ctx):
        ctx['js_stamp'] = js_stamp
        ctx['fast_config_panel'] = True
        return ctx

YunweiEngin.add_pages(page_dc)