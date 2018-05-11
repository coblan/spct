# encoding:utf-8

from __future__ import unicode_literals
from helpers.director.shortcut import page_dc
from helpers.director.engine import BaseEngine,page,fa,can_list,can_touch
from django.contrib.auth.models import User,Group
from helpers.maintenance.update_static_timestamp import js_stamp
from django.utils.translation import ugettext as _
from django.conf import settings
from js_translation import get_tr

class PcMenu(BaseEngine):
    url_name='sportcenter'
    brand = 'SportsCenter'
    mini_brand='SC'
    
    @property
    def menu(self):
        menu=[
            {'label':_('DashBoard'),'url':page('home'),'icon':fa('fa-home')},
            
            {'label':_('Marketing'),'icon':fa('fa-image'),'visible':can_list((User,Group)),
            'submenu':[
                {'label':_('Banner'),'url':page('TbBanner')},
                {'label':_('App Package'),'url':page('maindb.TbAppversion')},
                {'label':_('Notice'),'url':page('maindb.TbNotice')},
                {'label':_('Currency'),'url':page('maindb.TbCurrency')},
                {'label':_('Help'),'url':page('maindb.TbQa')},
                {'label':_('Activity'),'url':page('maindb.TBActive')},
                   
                 
                
                ]},  
            
            
            {'label':_('Member'),'icon':fa('fa-users'),'visible':can_list((User,Group)),
            'submenu':[
                {'label':_('Tb Account'),'url':page('maindb.account'),'icon':fa('fa-home')},
                {'label':_('Tb Login Log'),'url':page('maindb.loginlog'),'icon':fa('fa-home')},
                
                ]},   
            
            {'label':_('MoneyFlow'),'icon':fa('fa-dollar'),'visible':can_list((User,Group)),
            'submenu':[
                {'label':_('Tb Balance Log'),'url':page('maindb.balancelog'),'icon':fa('fa-home')},
                {'label':_('Tb Trans'),'url':page('maindb.trans'),'icon':fa('fa-home')},
                {'label':_('Tb Channel'),'url':page('maindb.channel'),'icon':fa('fa-home')},
                             ]}, 
            
            {'label':_('Games'),'icon':fa('fa-globe'),'visible':can_list((User,Group)),
            'submenu':[
                {'label':_('Tb TicketMaster'),'url':page('maindb.ticketmaster'),'icon':fa('fa-home')},
                {'label':_('Tb Match'),'url':page('maindb.Matches')},
                {'label':_('View TicketSingleByMatch'),'url':page('maindb.TicketSingleByMatch')},
                {'label':'Players','url':page('betradar.Players'),'icon':fa('fa-home')},
                        ]}, 
            
            {'label':_('RiskControl'),'icon':fa('fa-globe'),'visible':can_list((User,Group)),
            'submenu':[
                {'label':_('Tb RC Filter'),'url':page('maindb.TbRcFilter'),'icon':fa('fa-home')},
                {'label':_('Tb RC Level'),'url':page('maindb.TbRcLevel')},
                {'label':_('Tb RC User'),'url':page('maindb.TbRcUser')},
                {'label':_('Tb Blankuserlist'),'url':page('maindb.TbBlackuserlist')},
                {'label':_('Tb BlackuserlistLog'),'url':page('maindb.TbBlackuserlistLog')},
                
                {'label':_('Black IP Range'),'url':page('maindb.BlankipRangeList')},
                {'label':_('White IP'),'url':page('maindb.WhiteIpList')},
                {'label':_('White User'),'url':page('maindb.Whiteuserlist')},
                
                {'label':_('Tb Withdraw Limit Log'),'url':page('maindb.TbWithdrawlimitlog')}
                        ]},             
            
            
            {'label':'Betradar','icon':fa('fa-users'),'visible':can_list((User,Group)),
            'submenu':[
                {'label':'Alltournamentsidcn','url':page('betradar.Alltournamentsidcn'),'icon':fa('fa-home')},
                {'label':'Players','url':page('betradar.Players'),'icon':fa('fa-home')},
                ]},
                
           
            
            #{'label':_('学校管理'),'icon':fa('fa-users'),'visible':can_list((User,Group)),
            #'submenu':[
                #{'label':'学校管理','url':page('school.school'),'visible':can_touch(User)},
                #{'label':'学生管理','url':page('school.student'),'visible':can_touch(Group)},
                #]},
        
            #{'label':'首页','url':page('home'),'icon':fa('fa-home')},
            # {'label':'政策','icon':fa('fa-sitemap'),'submenu':[
                # {'label':'政策协议','url':page('liantang.policy')},
                # {'label':'申请表格','url':page('liantang.applytable')}
                # ]},
            
            #{'label':'政策协议','url':page('liantang.policy'),'icon':fa('fa-sitemap')},
            #{'label':'申请表格','url':page('liantang.applytable'),'icon':fa('fa-life-ring')},
            #{'label':'建房信息','url':page('liantang.jianfanginfo'),'icon':fa('fa-building')},
            ## {'label':'GIS区域','url':page('geoinfo.blockpolygon'),'icon':fa('fa-map-o')},
            ## {'label':'区域组','url':page('geoinfo.blockgroup'),'icon':fa('fa-map-o')}
            #{'label':'村委信息','url':page('liantang.cunwei'),'icon':fa('fa-life-ring')},
            
            ##{'label':'账号管理','url':page('user'),'icon':fa('fa-users')},
             {'label':'账号','url':page('user'),'icon':fa('fa-users'),'visible':can_list((User,Group)),
                  'submenu':[
                      {'label':'账号管理','url':page('jb_user'),'visible':can_touch(User)},
                      {'label':'角色管理','url':page('jb_group'),'visible':can_touch(Group)},
                      #{'label':'权限分组','url':page('group_human'),'visible':can_touch(Group)},
                ]},        
            
        ]
        return menu
    
    def custome_ctx(self, ctx):
        ctx['js_stamp']=js_stamp
        ctx['fast_config_panel']=True
        #ctx['table_fun_config'] ={
            #'detail_link': '详情', #'<i class="fa fa-info-circle" aria-hidden="true" title="查看详情"></i>'#,
        #}
        #lans = []
        #for k,v in settings.LANGUAGES:
            #lans.append({'value':k,'label':v})
            
        #ctx['site_settings']={
            #'lans':lans,
            #'tr':get_tr()
        #}
        
        return ctx      

PcMenu.add_pages(page_dc)