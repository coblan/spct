# encoding:utf-8

from __future__ import unicode_literals
from helpers.director.shortcut import page_dc
from helpers.director.engine import BaseEngine,page,fa,can_list,can_touch
from django.contrib.auth.models import User,Group
from helpers.maintenance.update_static_timestamp import js_stamp


class PcMenu(BaseEngine):
    url_name='sportcenter'
    brand = 'SportsCenter'
    mini_brand='SC'
    menu=[
        {'label':'控制面板','url':page('home'),'icon':fa('fa-home')},
        {'label':'Banner','url':page('TbBanner'),'icon':fa('fa-image')},
        {'label':'会员管理','icon':fa('fa-users'),'visible':can_list((User,Group)),
        'submenu':[
            {'label':'会员列表','url':page('maindb.account'),'icon':fa('fa-home')},
            {'label':'Players','url':page('betradar.Players'),'icon':fa('fa-home')},
            ]},   
        
        {'label':'金流管理','icon':fa('fa-users'),'visible':can_list((User,Group)),
        'submenu':[
            {'label':'账目记录','url':page('maindb.balancelog'),'icon':fa('fa-home')},
            {'label':'存款记录','url':page('maindb.trans'),'icon':fa('fa-home')},
            {'label':'金流渠道','url':page('maindb.channel'),'icon':fa('fa-home')},
                         ]}, 
        
        {'label':'赛事及赔率','icon':fa('fa-users'),'visible':can_list((User,Group)),
        'submenu':[
            {'label':'注单列表','url':page('maindb.ticketmaster'),'icon':fa('fa-home')},
            {'label':'Players','url':page('betradar.Players'),'icon':fa('fa-home')},
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
                  {'label':'账号管理','url':page('user'),'visible':can_touch(User)},
                  {'label':'权限分组','url':page('group_human'),'visible':can_touch(Group)},
            ]},        
        
    ]
    
    def custome_ctx(self, ctx):
        ctx['js_stamp']=js_stamp
        #ctx['table_fun_config'] ={
            #'detail_link': '详情', #'<i class="fa fa-info-circle" aria-hidden="true" title="查看详情"></i>'#,
        #}
        return ctx      

PcMenu.add_pages(page_dc)