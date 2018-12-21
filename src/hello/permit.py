from helpers.director.base_data import site_cfg
from django.utils.translation import ugettext as _

def get_permit(): 
    permit = [
        { 'label': _('Marketing'),
         'children': [
             { 'label': _('Banner'), 'children': [
                 {'label': '查看', 'value': 'TbBanner'}, 
                 { 'label': '编辑', 'value': 'TbBanner.edit', 'depend': ['TbBanner'],}, 
                 ]}, 
             { 'label': _('App Package'), 'children': [
                 {'label': '查看', 'value': 'TbAppversion'}, 
                 {'label': '编辑', 'value': 'TbAppversion.edit', 'depend': ['TbAppversion'],}, 
                 ],},
             { 'label': _('Notice'), 'children': [
                 {'label': '查看','value': 'TbNotice',}, 
                 {'label': '编辑','value': 'TbNotice.edit', 'depend': ['TbNotice'],}, 
                 {'label': '更新缓存','value': 'TbNotice.update_cache', 'depend': [ 'TbNotice', 'TbNotice.edit'],}, 
                 ],},
             #{ 'label': _('Notice'), 'value': 'TbNotice',}, 
             { 'label': _('Help'), 'children':[
                 {'label': '查看', 'value': 'TbQa',}, 
                 {'label': '编辑', 'value': 'TbQa.edit','depend': ['TbQa']}, 
                 {'label': '更新缓存', 'value': 'TbQa.update_cache', 'depend': ['TbQa' , 'TbQa.edit',],}
                 ]}, 
             { 'label': _('Activity'), 'children': [
                 {'label': '查看', 'value': 'TbActivity',}, 
                 {'label': '编辑', 'value': 'TbActivity.edit', 'depend': ['TbActivity'],}, 
                 {'label': '更新缓存', 'value': 'TbActivity.update_cache', 'depend': ['TbActivity', 'TbActivity.edit', ],}
                 ]}, 
            { 'label': '代理用户留言', 'value': 'TbAgentleavemsg',}, 
            #{ 'label': _('AppResource'), 'value': 'TbAppresource',}, 
             ]
         }, 
        { 'label': '基本信息',
         'children': [
             {'label': '运动类型', 'children': [
                 {'label': '查看', 'value': 'TbSporttypes',}, 
                 {'label': '编辑', 'value': 'TbSporttypes.edit', 'depend': ['TbSporttypes'],}
                                 ],}, 
             {'label': '足球联赛资料', 'children': [
                 {'label': '查看', 'value': 'TbTournament',}, 
                 {'label': '编辑', 'value': 'TbTournament.edit', 'depend': ['TbTournament'],}
                    ],}, 
             {'label': '篮球联赛资料', 'children': [
                 {'label': '查看', 'value': 'TbTournamentBasketball',}, 
                 {'label': '编辑', 'value': 'TbTournamentBasketball.edit', 'depend': ['TbTournamentBasketball'],}
                            ],}, 
             
             {'label': '足球队资料', 'children': [
                 {'label': '查看', 'value': 'TbTeams',}, 
                 {'label': '编辑', 'value': 'TbTeams.edit', 'depend': ['TbTeams'],}
                    ],}, 
             {'label': '篮球队资料', 'children': [
                 {'label': '查看', 'value': 'TbTeamsBasketball',}, 
                 {'label': '编辑', 'value': 'TbTeamsBasketball.edit', 'depend': ['TbTeamsBasketball'],}
                           ],}, 

             {'label': '充值渠道', 'children': [
                 {'label': '查看', 'value': 'TbPaychannel',}, 
                 {'label': '编辑', 'value': 'TbPaychannel.edit', 'depend': ['TbPaychannel'],}
                ],}, 
             
             {'label': 'VIP充值渠道', 'children': [
                 {'label': '查看', 'value': 'TbPaychanneljoinlevel',}, 
                 {'label': '编辑', 'value': 'TbPaychanneljoinlevel.edit', 'depend': ['TbPaychanneljoinlevel'],}
                ],},  
             {'label': '银行卡类型', 'children': [
                 {'label': '查看', 'value': 'TbBanktypes',}, 
                 {'label': '编辑', 'value': 'TbBanktypes.edit', 'depend': ['TbBanktypes'],}
                       ],},              
             {'label': '玩法设置', 'value': 'TbOddstypegroup',}, 
             {'label': 'APP资源', 'children': [
                 {'label': '查看', 'value': 'TbAppresource',}, 
                 {'label': '编辑', 'value': 'TbAppresource.edit', 'depend': ['TbAppresource'],}
                ],},              
             {'label': '金币', 'children': [
                 {'label': '查看', 'value': 'TbCurrency',}, 
                 {'label': '编辑', 'value': 'TbCurrency.edit', 'depend': ['TbCurrency'],}
                              ],}, 
             
             #{'label': _('Tb Balance Log'), 'value': 'TbBalancelog', }, 
          
             ],
         }, 
        
        { 'label': _('Member'),
         'children': [
             {'label': _('Tb Account'), 'children': [
                {'label': '查看', 'value': 'TbAccount',}, 
                {'label': '编辑', 'value': 'TbAccount.edit', 'depend': ['TbAccount'],}, 
                
                {'label': '所有标签(全功能)', 'value': 'TbAccount.all_tab', 'depend': ['TbAccount.edit', 
                                'TbBalancelog', 'TbLoginlog', 'TbBankcard', 'TbBankcard.edit', 'TbRecharge.edit',
                                'TbWithdraw.edit'],}, 
               
                ],}, 
             
             {'label': _('Tb Balance Log'), 'value': 'TbBalancelog', }, 
             {'label': _('Tb Login Log'), 'value': 'TbLoginlog',}, 
             {'label': '银行卡', 'children': [
                {'label': '查看', 'value': 'TbBankcard',}, 
                {'label': '编辑', 'value': 'TbBankcard.edit', 'depend': ['TbBankcard'],}, 
                ],}, 
             ],
         }, 
        {'label': _('MoneyFlow'),
         'children': [
             {'label': '充值记录', 'children': [
                 {'label': '查看', 'value': 'TbRecharge', 'depend': ['TbAccount']}, 
                 {'label': '编辑', 'value': 'TbRecharge.edit', 'depend': ['TbRecharge', 'TbAccount'],}
                 ],}, 
             {'label': '提现记录', 'children': [
                 {'label': '查看', 'value': 'TbWithdraw',}, 
                 {'label': '编辑', 'value': 'TbWithdraw.edit', 'depend': ['TbWithdraw'],}
                          ],}
             #{'label': '账目记录', 'value': 'TbBalancelog', }, 
             #{'label': '金流渠道', 'value': 'TbChannel',}, 
             #{'label': '金流日志', 'value': 'TbChargeflow',}
             ],
        }, 
        {'label': '比赛列表',#_('Tb Match'), 
         'children': [
             {'label': '足球比赛列表', 'children': [
                 {'label': '查看', 'value': 'TbMatches',}, 
                 {'label': '编辑', 'value': 'TbMatches.edit', 'depend': ['TbMatches'],}
                 ]}, 
             {'label':'篮球比赛列表', 'children': [
                 {'label': '查看', 'value': 'TbMatchesBasketball',}, 
                 {'label': '编辑', 'value': 'TbMatchesBasketball.edit', 'depend': ['TbMatchesBasketball'],}
                 ]}, 
             
             {'label': _('Tb TicketMaster'), 'children': [
                 {'label': '查看', 'value': 'TbTicketmaster_all_tab_read',}, 
                 {'label': '编辑', 'value': 'TbTicketmaster.edit', 'depend': ['TbTicketmaster_all_tab_read', 'TbMatches'],}
                 ]},              
             ],
        }, 
       
        {'label': _('RiskControl'),
         'children': [
             {'label': '最大赔付', 'children': [
                 {'label': '查看', 'value': 'TbMaxpayout',}, 
                 {'label': '编辑', 'value': 'TbMaxpayout.edit', 'depend': ['TbMaxpayout', 'TbMatches', 'TbTournament', 'TbAccount'],}, 
                 ],}, 
             {'label': '提现控制', 'children': [
                 {'label': '查看', 'value': 'TbParameterinfo',}, 
                 {'label': '编辑', 'value': 'TbParameterinfo.edit', 'depend': ['TbParameterinfo'],}, 
                        ],}, 
             {'label': '黑名单范围', 'children': [
                 {'label': '查看', 'value': 'Blackiprangelist',}, 
                 {'label': '编辑', 'value': 'Blackiprangelist.edit', 'depend': ['Blackiprangelist'],}, 
                        ],}, 
             {'label': '充值黑名单IP', 'children': [
                 {'label': '查看', 'value': 'TbPaychannelblackiprange',}, 
                 {'label': '编辑', 'value': 'TbPaychannelblackiprange.edit', 'depend': ['TbPaychannelblackiprange'],}, 
                          ],}, 
             {'label': 'IP白名单', 'children': [
                 {'label': '查看', 'value': 'TbWhiteiprangelist',}, 
                 {'label': '编辑', 'value': 'TbWhiteiprangelist.edit', 'depend': ['TbWhiteiprangelist', ],}, 
                          ],}, 
             {'label': '用户白名单', 'children': [
                 {'label': '查看', 'value': 'Whiteuserlist',}, 
                 {'label': '编辑', 'value': 'Whiteuserlist.edit', 'depend': ['Whiteuserlist', 'TbAccount'],}, 
                      ],}, 
             {'label': '联赛组水位', 'value': 'TbLeagueGroup.edit',}, 
             {'label': '参数设置', 'value': 'risk.parameter',}
             
            
            #{'label': _('Tb RC Filter'), 'value': 'TbRcFilter',}, 
            #{'label': _('Tb RC Level'), 'value': 'TbRcLevel',}, 
            #{'label': _('Tb RC User'), 'value': 'TbRcUser',}, 
            #{'label': _('Tb Withdraw Limit Log'), 'value': 'TbWithdrawlimitlog',}, 
                 
                 
             #{'label': _('Tb Blankuserlist'), 'value': 'TbBlackuserlist',}, 
             #{'label': _('Tb BlackuserlistLog'), 'value': 'TbBlackuserlistLog',}, 
             #{'label': _('Blackiplist'), 'value': 'Blackiplist',}, 
             #{'label': _('Black IP Range'), 'value': 'Blackiprangelist',}, 
             #{'label': _('White IP'), 'value': 'Whiteiplist',}, 
             #{'label': _('White User'), 'value': 'Whiteuserlist',}
             ],},
        {'label': '报表中心', 
         'children': [
             {'label': '会员统计', 'value': 'member_statistic', 'depend': ['TbAccount'],}, 
             {'label': '平台亏盈', 'value': 'platform_profit',},     
                     ],
        }, 
        {'label': '代理平台', 'children': [
            {'label': '代理用户', 'children': [
                {'label': '查看', 'value': 'agent', 'depend': ['TbAccount'],}, 
                {'label': '编辑', 'value': 'agent.edit', 'depend': ['TbAccount.edit'],},     
               ],}, 
            {'label': '代理佣金', 'children': [
                {'label': '查看', 'value': 'TbAgentcommission',}, 
                {'label': '编辑', 'value': 'TbAgentcommission.edit',},
                         ],}
            ],
         
         
         
        
        }, 
        
        {'label': _('User'),
         'children': [
            #{'label': _('查看用户'), 'value': 'User.read',}, 
             {'label': _('User'), 'value': 'User.write',}, 
             {'label': _('Role'), 'value': 'Group',}
             ],
         }
    ]
    return permit

site_cfg['permit.options'] = get_permit
#permit_dc['__root__'] = permit