
from helpers.director.shortcut import director_element
from django.conf import settings
from django.utils.translation import ugettext as _
from helpers.func.nav_data import walk_dict
from helpers.func.collection.container import evalue_container

@director_element('permit.options')
def get_permit(ui=None): 
    
    permit1 =[
        {'label': '商户分组','value': '-i_am_merchant','help_text':'标识用户是否为商户;如果是商户用户分组，必须勾选!'},
        {'label':'首页统计','value':'home-statistic'},
        {'label': '待办事项',
         'children': [
             {'label': '结算相关', 'value': 'todolist_1',}, 
             {'label': '结算提醒', 'value': 'todolist_2',}, 
             {'label':'资金流','value':'todolist_100'},
             ],
         },
        { 'label': '市场活动',
         'children': [
             { 'label': _('Banner'), 'children': [
                 {'label': '查看', 'value': 'TbBanner',}, 
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
             {'label':'代理公告','value':'TbAgentnotice.edit'},
             { 'label': _('Help'), 'children':[
                 {'label': '查看', 'value': 'TbQa',}, 
                 {'label': '编辑', 'value': 'TbQa.edit','depend': ['TbQa']}, 
                 {'label': '更新缓存', 'value': 'TbQa.update_cache', 'depend': ['TbQa' , 'TbQa.edit',],}
                 ]}, 
             { 'label': '优惠活动', 'children': [
                 {'label': '查看', 'value': 'TbActivityV2',}, 
                 {'label': '编辑', 'value': 'TbActivityV2.edit', 'depend': ['TbActivityV2'],}, 
                 {'label': '更新缓存', 'value': 'TbActivityV2.update_cache', 'depend': ['TbActivityV2', 'TbActivityV2.edit', ],},
                 {'label':'活动设置','value':'TbActivitySettings.edit','depend':['TbActivityV2']}
                 ]}, 
            {'label':'活动记录','value':'TbActivityRecord'},
            { 'label': '代理用户留言', 'value': 'TbAgentleavemsg',}, 
            
            { 'label': '用户排行', 'children':[
                {'label':'虚拟用户','value':'TbUserConst.edit'},
                {'label':'用户排行','value':'TbUserRank.edit'}
                ],}, 
           
            { 'label': '红利发放', 'children': [
                {'label': '查看', 'value': 'Bonuse-dispatch',}, 
                {'label': '编辑', 'value': 'Bonuse-dispatch.edit', 'depend': ['Bonuse-dispatch','TbAccount'],}, 
                         ]}, 
            
             { 'label': '启动广告', 'children': [
                {'label': '查看', 'value': 'TbAdvertisement',}, 
                {'label': '编辑', 'value': 'TbAdvertisement.edit', 'depend': ['TbAdvertisement'],}, 
                         ]}, 
              { 'label': '推送消息', 'children': [
                {'label': '查看', 'value': 'TbMessage',}, 
                {'label': '编辑', 'value': 'TbMessage.edit', 'depend': ['TbMessage'],}, 
                         ]}, 
               { 'label': 'VIP豪礼', 'children': [
                {'label': '查看', 'value': 'TbVipgift',}, 
                {'label': '编辑', 'value': 'TbVipgift.edit', 'depend': ['TbVipgift'],}, 
                         ]}, 
             ]
         }, 
         { 'label': '基本信息',
         'children': [
             {'label': '运动类型', 'children': [
                 {'label': '查看', 'value': 'TbSporttypes',}, 
                 {'label': '编辑', 'value': 'TbSporttypes.edit', 'depend': ['TbSporttypes'],}
                                 ],}, 
             {'label': '联赛资料', 'children': [
                 {'label': '查看', 'value': 'TbTournament',}, 
                 {'label':'订阅','value':'TbTournament.issubscribe','depend': ['TbTournament']},
                 {'label':'走地','value':'TbTournament.closelivebet','depend': ['TbTournament']},
                 {'label':'推荐','value':'TbTournament.isrecommend','depend': ['TbTournament']},
                 {'label': '编辑(除订阅、走地、推荐)', 'value': 'TbTournament.edit', 'depend': ['TbTournament'],}
                    ],}, 
             {'label':'充值渠道组','value':'TbPaychannelgroup.edit'},
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
             {'label': '玩法设置', 'children':[
                 {'label':'查看','value':'TbMarkets'},
                 {'label':'修改','value': 'TbMarkets.edit','depend':['TbMarkets']}
             ]} ,
             {'label': 'APP资源', 'children': [
                 {'label': '查看', 'value': 'TbAppresource',}, 
                 {'label': '编辑', 'value': 'TbAppresource.edit', 'depend': ['TbAppresource'],}
                ],},              
             {'label': '金币', 'children': [
                 {'label': '查看', 'value': 'TbCurrency',}, 
                 {'label': '编辑', 'value': 'TbCurrency.edit', 'depend': ['TbCurrency'],}
                              ],}, 
             ],
         }, 
        { 'label': _('Member'),
         'children': [
             {'label': _('Tb Account'), 'children': [
                {'label':'基本信息','children':[
                      {'label': '查看', 'value': 'TbAccount',}, 
                      {'label': '编辑', 'value': 'TbAccount.edit', 'depend': ['TbAccount'],}, 
                    ]},
                #{'label':'账目记录','value':'TbBalancelog'},
                #{'label':'银行卡','children':[
                      #{'label': '查看', 'value': 'TbBankcard',}, 
                      #{'label': '编辑', 'value': 'TbBankcard.edit', 'depend': ['TbBankcard'],}, 
                #]},
                #{'label':'充值记录','value':'TbRecharge'},
                #{'label':'提现记录','value':'TbWithdraw'},
                #{'label':'注单','value':'TbTicketmaster_all_tab_read'},
                #{'label':'登录日志','value':'TbLoginlog'},
                #{'label':'会员统计','value':'member_statistic'},
                #{'label':'赛事统计','value':'TbMatch'},
              
            
                #{'label': '所有标签(全功能)', 'value': 'TbAccount.all_tab', 'depend': ['TbAccount.edit', 
                                #'TbBalancelog', 'TbLoginlog', 'TbBankcard', 'TbBankcard.edit', 'TbRecharge.edit',
                                #'TbWithdraw.edit',],}, 
                ],}, 
             
             {'label': _('Tb Balance Log'), 'value': 'TbBalancelog', }, 
             {'label': _('Tb Login Log'), 'value': 'TbLoginlog',}, 
             {'label': '银行卡', 'children': [
                {'label': '查看', 'value': 'TbBankcard',}, 
                {'label': '编辑', 'value': 'TbBankcard.edit', 'depend': ['TbBankcard'],}, 
                ],}, 
            #{'label': '限额记录', 'children': [
                #{'label': '查看', 'value': 'TbBetfullrecord',}, 
                #{'label': '编辑', 'value': 'TbBetfullrecord.edit', 'depend': ['TbBetfullrecord'],}, 
                #],}, 
             {'label':'关联用户','value':'member.relevent_user'},
             #{'label': '流失用户', 'value': 'member.chum_user','depend':['TbAccount'] }, 
             {'label':'用户日志','value':'TbUserLog'},
            {'label':'限额记录','children':[
                    {'label': '查看', 'value': 'TbBetfullrecord',}, 
                    {'label': '编辑', 'value': 'TbBetfullrecord.edit', 'depend': ['TbBetfullrecord'],}, 
                ]},
            {'label':'会员关怀','children':[
                {'label':'查看页面','value':'member.kefu','depend':['TbAccount']},
                {'label':'查看所有会员','value':'kefu.watch_all_account'},
                ],},
            {'label':'VIP红利','children':[
                {'label':'查看页面','value':'TbVipbonus'},
                {'label':'收货地址','value':'vipbonus.account_real_address','depend':['TbVipbonus']}
            ]},
            {'label':'指定客服','value':'TbAccount.csuserid','depend':['TbAccount','User.read']}
            
            ]
         }, 
        {'label': _('MoneyFlow'),
         'children': [
             {'label': '充值记录', 'children': [
                 {'label': '查看', 'value': 'TbRecharge', 'depend': ['TbAccount']}, 
                 {'label': '编辑', 'value': 'TbRecharge.edit', 'depend': ['TbRecharge', 'TbAccount'],}
                 ],}, 
             {'label': '提现记录', 'children': [
                 {'label': '查看', 'value': 'TbWithdraw','depend':['TbTicketmaster.edit']}, 
                 {'label': '编辑', 'value': 'TbWithdraw.edit', 'depend': ['TbWithdraw',],}
                          ],}
             #{'label': '账目记录', 'value': 'TbBalancelog', }, 
             #{'label': '金流渠道', 'value': 'TbChannel',}, 
             #{'label': '金流日志', 'value': 'TbChargeflow',}
             ],
        }, 
        {'label': '比赛列表',#_('Tb Match'), 
         'children': [
             {'label': '比赛列表', 'children': [
                 {'label': '查看', 'value': 'TbMatches',}, 
                 {'label':'推荐','value':'TbMatch.isrecommend'},
                 {'label':'走地','value':'TbMatch.hasliveodds'},
                 {'label':'显示/隐藏','value':'TbMatch.ishidden'},
                 {'label':'退单','value':'TbMatch.quit_ticket'},
                 {'label': '编辑(除推荐、走地、显示)', 'value': 'TbMatches.edit', 'depend': ['TbMatches',],},
                 {'label':'比分','value':'TbPeriodscore'},
                 {'label':'危险球','value':'TbLivefeed.edit'},
                 {'label':'盘口','value':'manual_specialbetvalue'},
                 {'label':'手动结算','children':[
                      {'label':'进入结算页面','value':'manual_outcome','depend':['TbMarkets']},
                      {'label':'提交手动结算','value':'save_manual_outcome'},
                      {'label':'审批手动结算','value':'audit_manual_outcome'},
                 ]}
                
                 ]}, 
    

             {'label': _('Tb TicketMaster'), 'children': [
                 {'label': '查看', 'value': 'TbTicketmaster_all_tab_read','depend':['TbMatches']}, 
                 {'label': '编辑', 'value': 'TbTicketmaster.edit', 'depend': ['TbTicketmaster_all_tab_read', ],}
                 ]},   
             {'label': '调水模板', 'value':'TbAdjusttemplate.edit'}, 
             {'label':'比赛匹配','value':'web_match_data1','depend':['TbMatches']},
            {'label':'跟水设置','value':'mapping_setting.water_switch',},
             ],
        }, 
        
       
        {'label': _('RiskControl'),
         'children': [
             #{'label': '足球最大赔付', 'children': [
                 #{'label': '查看', 'value': 'TbMaxpayout','depend': ['TbMatches', 'TbTournament', 'TbAccount']}, 
                 #{'label': '编辑', 'value': 'TbMaxpayout.edit', 'depend': ['TbMaxpayout', ],}, 
                 #],}, 
             #{'label': '篮球最大赔付', 'children': [
                 #{'label': '查看', 'value': 'TbMaxpayoutBasketball','depend': ['TbMatchesBasketball', 'TbTournamentBasketball', 'TbAccount']}, 
                 #{'label': '编辑', 'value': 'TbMaxpayoutBasketball.edit', 'depend': ['TbMaxpayoutBasketball',],}, 
                             #],}, 
             
             {'label': '提现控制', 'children': [
                 {'label': '查看', 'value': 'TbParameterinfo',}, 
                 {'label': '编辑', 'value': 'TbParameterinfo.edit', 'depend': ['TbParameterinfo'],}, 
                        ],}, 
             {'label': '登录IP黑名单', 'children': [
                 {'label': '查看', 'value': 'Blackiprangelist',}, 
                 {'label': '编辑', 'value': 'Blackiprangelist.edit', 'depend': ['Blackiprangelist'],}, 
                        ],}, 
             {'label': '登录地区黑名单', 'children': [
                 {'label': '查看', 'value': 'TbAreablacklist',}, 
                 {'label': '编辑', 'value': 'TbAreablacklist.edit', 'depend': ['TbAreablacklist'],}, 
                        ],}, 
             {'label': '充值用户黑名单', 'children': [
                 {'label': '查看', 'value': 'TbPaychannelblackaccount','depend':['TbAccount']}, 
                 {'label': '编辑', 'value': 'TbPaychannelblackaccount.edit', 'depend': ['TbPaychannelblackaccount'],}, 
                        ],}, 
             
             {'label': '充值IP黑名单', 'children': [
                 {'label': '查看', 'value': 'TbPaychannelblackiprange',}, 
                 {'label': '编辑', 'value': 'TbPaychannelblackiprange.edit', 'depend': ['TbPaychannelblackiprange'],}, 
                          ],}, 
             {'label': '充值地区黑名单', 'children': [
                 {'label': '查看', 'value': 'TbRechargeareablacklist',}, 
                 {'label': '编辑', 'value': 'TbRechargeareablacklist.edit', 'depend': ['TbRechargeareablacklist'],}, 
                          ],}, 
             
             {'label': 'IP白名单', 'children': [
                 {'label': '查看', 'value': 'TbWhiteiprangelist',}, 
                 {'label': '编辑', 'value': 'TbWhiteiprangelist.edit', 'depend': ['TbWhiteiprangelist', ],}, 
                          ],}, 
             {'label': '用户白名单', 'children': [
                 {'label': '查看', 'value': 'Whiteuserlist',}, 
                 {'label': '编辑', 'value': 'Whiteuserlist.edit', 'depend': ['Whiteuserlist', 'TbAccount'],}, 
                      ],}, 
             #{'label': '联赛组水位', 'value': 'TbLeagueGroup.edit',}, 
             {'label': '参数设置', 'value': 'risk.parameter',},
             {'label':'用户限额分组','children':[
                 {'label':'查看','value':'TbLimitusergroup'},
                 {'label':'编辑','value':'TbLimitusergroup.edit','depend':['TbLimitusergroup']}
             ]},
             {'label':'风险控制设置','value':'risk.RiskcontrolSetting'},
             {'label':'联赛风控','children':[
                 {'label':'基本信息','value':'TbLeagueGroup.edit'},
                 {'label':'玩法权重','value':'TbLeaguegroupMarketweight.edit'},
                 {'label':'包含联赛','value':'virtual_include_league','depend':['TbTournament']}
                 ] },
             
             
            
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
             {'label':'充值安全统计','value':'report.recharge_reports','depend':['TbRecharge']},
             {'label':'投注分析','value':'report.betAnalysis',}
                     ],
        }, 
        {'label': '代理平台', 'children': [
            {'label': '代理用户',  'value': 'agent', 'depend': ['TbAccount'] }, 
            {"label":'修改上级','value':'agent.parent.edit','depend': ['agent']},
            {'label': '代理佣金', 'children': [
                {'label': '查看', 'value': 'TbAgentcommission',}, 
                {'label': '编辑', 'value': 'TbAgentcommission.edit',},
                         ],},
            {'label':'指定客服','value':'agent.csuserid-btn','depend':['TbAccount.csuserid']}
            ],
        
        }, 
        {'label':'AG系统','visible':getattr(settings,'OPEN_SECRET',False) ,'children':[
            {'label':'AG账号','children':[
                {'label':'查看','value':'TbAgaccount'},
                {'label':'编辑','value':'TbAgaccount.edit','depend':['TbAgaccount']},
                ]},
            {'label':'投注列表','value':'TbAgprofitloss.edit'},
            {'label':'资金流入','value':'TbGamemoneyininfo.edit'},
            {'label':'资金流出','value':'TbGamemoneyoutinfo.edit'}
        ]},
        
         {'label':'沙巴系统','visible':getattr(settings,'OPEN_SECRET',False) ,'children':[
            {'label':'账号','children':[
                {'label':'查看','value':'TbSportaccount'},
                {'label':'编辑','value':'TbSportaccount.edit','depend':['TbSportaccount']},
                ]},
            {'label':'投注列表','value':'TbSportprofitloss.edit'},
            {'label':'资金流入','value':'TbSportmoneyininfo.edit'},
            {'label':'资金流出','value':'TbSportmoneyoutinfo.edit'}
        ]},
        {'label':'龙城系统','visible':getattr(settings,'OPEN_SECRET',False) ,'children':[
            {'label':'账号','children':[
                {'label':'查看','value':'TbLcityaccount'},
                {'label':'编辑','value':'TbLcityaccount.edit','depend':['TbLcityaccount']},
                ]},
            {'label':'投注列表','value':'TbLcityprofitloss.edit'},
            {'label':'资金流入','value':'TbLcitymoneyininfo.edit'},
            {'label':'资金流出','value':'TbLcitymoneyoutinfo.edit'}
        ]},
        {'label':'IM体育/电竞','visible':getattr(settings,'OPEN_SECRET',False) ,'children':[
            {'label':'体育账号','children':[
                {'label':'查看','value':'TbImaccount'},
                {'label':'编辑','value':'TbImaccount.edit','depend':['TbImaccount']},
                ]},
            {'label':'电竞账号','children':[
                {'label':'查看','value':'TbImeaccount'},
                {'label':'编辑','value':'TbImeaccount.edit','depend':['TbImeaccount']},
                ]},
            {'label':'投注列表','value':'TbImprofitloss.edit'},
            {'label':'资金流入','value':'TbImmoneyininfo.edit'},
            {'label':'资金流出','value':'TbImmoneyoutinfo.edit'}
        ]},
        {'label':'RG系统','visible':getattr(settings,'OPEN_SECRET',False) ,'children':[
            {'label':'账号','children':[
                {'label':'查看','value':'TbRgaccount'},
                {'label':'编辑','value':'TbRgaccount.edit','depend':['TbRgaccount']},
                ]},
            {'label':'投注列表','value':'TbRgprofitloss.edit'},
            {'label':'资金流入','value':'TbRgmoneyininfo.edit'},
            {'label':'资金流出','value':'TbRgmoneyoutinfo.edit'}
        ]},
        {'label':'PT系统','visible':getattr(settings,'OPEN_SECRET',False) ,'children':[
            {'label':'账号','children':[
                {'label':'查看','value':'TbPtaccount'},
                {'label':'编辑','value':'TbPtaccount.edit','depend':['TbPtaccount']},
                ]},
            {'label':'投注列表','value':'TbPtprofitloss.edit'},
            {'label':'资金流入','value':'TbPtmoneyininfo.edit'},
            {'label':'资金流出','value':'TbPtmoneyoutinfo.edit'}
        ]},
        {'label':'SG系统','visible':getattr(settings,'OPEN_SECRET',False) ,'children':[
            {'label':'账号','children':[
                {'label':'查看','value':'TbSgaccount'},
                {'label':'编辑','value':'TbSgaccount.edit','depend':['TbSgaccount']},
                ]},
            {'label':'投注列表','value':'TbSgprofitloss.edit'},
            {'label':'资金流入','value':'TbSgmoneyininfo.edit'},
            {'label':'资金流出','value':'TbSgmoneyoutinfo.edit'}
        ]},
        {'label':'eBet真人','visible':getattr(settings,'OPEN_SECRET',False) ,'children':[
            {'label':'账号','children':[
                {'label':'查看','value':'TbEbaccount'},
                {'label':'编辑','value':'TbEbaccount.edit','depend':['TbEbaccount']},
                ]},
            {'label':'投注列表','value':'TbEbprofitloss.edit'},
            {'label':'资金流入','value':'TbEbmoneyininfo.edit'},
            {'label':'资金流出','value':'TbEbmoneyoutinfo.edit'}
        ]},
        
        {'label': '系统管理',
         'children': [
             {'label': '用户查看', 'value': 'User.read',}, 
             {'label': '用户编辑', 'value': 'User.write',}, 
             {'label': _('Role'), 'value': 'Group',},
             {'label':'用户扩展','children':[
                 {'label':'查看','value':'TbUserex'},
                 {'label':'编辑','value':'TbUserex.edit','depend':['TbUserex']},
             ]}
             ],
         },
        
         {'label': '运维管理',
         'children': [
             {'label': '域名管理', 'value': 'TbDomain.edit',}, 
             ],
         },
         
      
         
    ]
    permit_member =  [ 
        {'label':'会员列表(标签页)','children':[
                {'label':'基本信息','children':[
                      {'label': '查看', 'value': 'TbAccount',}, 
                      {'label': '编辑', 'value': 'TbAccount.edit', 'depend': ['TbAccount'],}, 
                    ]},
                {'label':'账目记录','value':'TbBalancelog'},
                {'label':'银行卡','children':[
                      {'label': '查看', 'value': 'TbBankcard',}, 
                      {'label': '编辑', 'value': 'TbBankcard.edit', 'depend': ['TbBankcard'],}, 
                ]},
                {'label':'充值记录','value':'TbRecharge'},
                {'label':'提现记录','value':'TbWithdraw'},
                {'label':'注单','value':'TbTicketmaster_all_tab_read'},
                {'label':'登录日志','value':'TbLoginlog'},
                {'label':'会员统计','value':'member_statistic'},
                {'label':'赛事统计','value':'TbMatch'},
                
                {'label':'限额记录','children':[
                    {'label': '查看', 'value': 'TbBetfullrecord',}, 
                    {'label': '编辑', 'value': 'TbBetfullrecord.edit', 'depend': ['TbBetfullrecord'],}, 
                ]},
            ]},
       { 'label': '会员管理',
         'children': [
            {'label':'关联用户','value':'member.relevent_user'},
            #{'label': '流失用户', 'value': 'member.chum_user','depend':['TbAccount'] }, 
            {'label':'用户日志','value':'TbUserLog'},
             ],
         }
        ]
    permit_match =[
        {'label': '比赛列表(按钮)',#_('Tb Match'), 
         'children': [
            {'label':'推荐','value':'TbMatch.isrecommend'},
            {'label':'走地','value':'TbMatch.hasliveodds'},
            {'label':'显示/隐藏','value':'TbMatch.ishidden'},
            {'label':'退单','value':'TbMatch.quit_ticket'},
            {'label': '编辑(除推荐、走地、显示)', 'value': 'TbMatches.edit', 'depend': ['TbMatches',],},
             ],
        }, 
        {'label':'比赛列表(标签页)','children':[
            {'label': '查看', 'value': 'TbMatches',}, 
            {'label':'比分','value':'TbPeriodscore'},
            {'label':'危险球','value':'TbLivefeed.edit'},
            {'label':'盘口','value':'manual_specialbetvalue'},
            {'label':'手动结算','children':[
                    {'label':'进入结算页面','value':'manual_outcome','depend':['TbMarkets']},
                    {'label':'提交手动结算','value':'save_manual_outcome'},
                    {'label':'审批手动结算','value':'audit_manual_outcome'},
               ]}
            ]},
        {'label': '玩法设置', 'children':[
                 {'label':'查看','value':'TbMarkets'},
                 {'label':'修改','value': 'TbMarkets.edit','depend':['TbMarkets']}
             ]} ,
        {'label': _('Tb TicketMaster'), 'children': [
                 {'label': '查看', 'value': 'TbTicketmaster_all_tab_read','depend':['TbMatches']}, 
                 {'label': '编辑', 'value': 'TbTicketmaster.edit', 'depend': ['TbTicketmaster_all_tab_read', ],}
                 ]},   
        {'label': '调水模板', 'value':'TbAdjusttemplate.edit'},  
    ]
    out_permit = []
    if ui is None:
        out_permit = permit1
    elif ui =='member':
        out_permit = permit_member
    elif ui=='match':
        out_permit = permit_match
    
    #out_list =[]
    #for ns in walk_dict(out_permit):
        #if ns.get('value'):
            #if ns.get('value') in out_list:
                #raise UserWarning('%s发生了重复'%ns.get('value'))
            #out_list.append(out_list)
    return  evalue_container(out_permit)

@director_element('permit.ui_options')
def permit_ui_options():
    return [
        #{'value':'admin_menu','label':'管理后台菜单'},
        {'value':'member','label':'会员管理'},
        {'value':'match','label':'比赛列表'}
     ]


#permit_dc['__root__'] = permit