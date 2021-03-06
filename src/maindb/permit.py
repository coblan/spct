from helpers.director.access.permit import ModelPermit
#from helpers.director.base_data import permit_dc
from .models import TbBanner, TbAppversion, TbNotice, TbAccount, TbNotice, TbQa, TbActivity, TbAgentleavemsg, \
     TbOddstypegroup, TbCurrency, TbTournament, TbTeams, TbBanktypes, TbAppresource, TbPaychannel, TbPaychanneljoinlevel, \
     TbAccount
from .models import * 

from helpers.director.shortcut import model_to_name, model_full_permit, add_permits, model_read_permit

import json



permits = [('TbBanner', model_read_permit(TbBanner), model_to_name(TbBanner), 'model' ),
           ('TbBanner.edit', model_full_permit(TbBanner), model_to_name(TbBanner) , 'model'), 
           ('TbAppversion', model_read_permit(TbAppversion), model_to_name(TbAppversion) , 'model'), 
           ('TbAppversion.edit', model_full_permit(TbAppversion), model_to_name(TbAppversion) , 'model'), 
           
           ('TbNotice', model_read_permit(TbNotice), model_to_name(TbNotice) , 'model'), 
           ('TbNotice.edit', model_full_permit(TbNotice), model_to_name(TbNotice) , 'model'), 
           ('TbNotice.updateCache', '', '', 'single'), 
           
           ('TbQa', model_read_permit(TbQa), model_to_name(TbQa), 'model'), 
           ('TbQa.edit', model_full_permit(TbQa), model_to_name(TbQa), 'model'), 
           ('TbQa.update_cache', '', '', 'single'), 
           
           ('TbMessage',model_read_permit(TbMessage),model_to_name(TbMessage),'model'),
           ('TbMessage.edit',model_full_permit(TbMessage),model_to_name(TbMessage),'model'),
           ('TbVipgift',model_read_permit(TbVipgift),model_to_name(TbVipgift),'model'),
           ('TbVipgift.edit',model_full_permit(TbVipgift),model_to_name(TbVipgift),'model'),
           ('TbVipbonus',model_read_permit(TbVipbonus),model_to_name(TbVipbonus),'model'),
           #('TbVipbonus.edit',model_read_permit(TbVipbonus),model_to_name(TbVipbonus),'model'),
           
           #------活动2--------
           ('TbActivityV2', model_read_permit(TbActivityV2), model_to_name(TbActivityV2), 'model'), 
           ('TbActivityV2.edit', model_full_permit(TbActivityV2), model_to_name(TbActivityV2), 'model'), 
           ('TbActivityV2.update_cache', '', '', 'single'), 
           ('TbActivitySettings.edit', model_full_permit(TbActivitySettings), model_to_name(TbActivitySettings), 'model'),
           ('TbActivityRecord',model_read_permit(TbActivityRecord),model_to_name(TbActivityRecord),'model'),
           
           # 代理公告
           ('TbAgentnotice.edit',model_full_permit(TbAgentnotice),model_to_name(TbAgentnotice),'model'),
           # 代理留言
           ('TbAgentleavemsg', model_read_permit(TbAgentleavemsg), model_to_name(TbAgentleavemsg), 'model'), 
           
           #------------------------------------------------
           ('TbOddstypegroup', model_full_permit(TbOddstypegroup), model_to_name(TbOddstypegroup), 'model'), 
           ('TbCurrency', model_read_permit(TbCurrency), model_to_name(TbCurrency), 'model'), 
           ('TbCurrency.edit', model_full_permit(TbCurrency), model_to_name(TbCurrency), 'model'), 
           
           # 运动类型
           ('TbSporttypes', model_read_permit(TbSporttypes), model_to_name(TbSporttypes), 'model'), 
           ('TbSporttypes.edit', model_full_permit(TbSporttypes), model_to_name(TbSporttypes), 'model'),            
           
           # 联赛
           ('TbTournament', model_read_permit(TbTournament), model_to_name(TbTournament), 'model'), 
           ('TbTournament.issubscribe',json.dumps({'write':['issubscribe']}),model_to_name(TbTournament),'model'),
           ('TbTournament.closelivebet',json.dumps({'write':['closelivebet']}),model_to_name(TbTournament),'model'),
           ('TbTournament.isrecommend',json.dumps({'write':['isrecommend']}),model_to_name(TbTournament),'model'),
           ('TbTournament.edit', model_full_permit(TbTournament,exclude=['issubscribe','closelivebet','isrecommend']), model_to_name(TbTournament), 'model'), 
           
           #('TbTournamentBasketball', model_read_permit(TbTournamentBasketball), model_to_name(TbTournamentBasketball), 'model'), 
           #('TbTournamentBasketball.edit', model_full_permit(TbTournamentBasketball), model_to_name(TbTournamentBasketball), 'model'),            
           
           ('TbTeams', model_read_permit(TbTeams), model_to_name(TbTeams), 'model'), 
           ('TbTeams.edit', model_full_permit(TbTeams), model_to_name(TbTeams), 'model'), 
           
           ('TbTeamsBasketball', model_read_permit(TbTeamsBasketball), model_to_name(TbTeamsBasketball), 'model'), 
           ('TbTeamsBasketball.edit', model_full_permit(TbTeamsBasketball), model_to_name(TbTeamsBasketball), 'model'),            
           
           ('TbBanktypes', model_read_permit(TbBanktypes), model_to_name(TbBanktypes), 'model'), 
           ('TbBanktypes.edit', model_full_permit(TbBanktypes), model_to_name(TbBanktypes), 'model'), 
           
           ('TbAppresource', model_read_permit(TbAppresource), model_to_name(TbAppresource), 'model'), 
           ('TbAppresource.edit', model_full_permit(TbAppresource), model_to_name(TbAppresource), 'model'), 
           
           ('TbPaychannelgroup.edit',model_full_permit(TbPaychannelgroup),model_to_name(TbPaychannelgroup),'model'),
           ('TbPaychannel', model_read_permit(TbPaychannel), model_to_name(TbPaychannel), 'model'), 
           ('TbPaychannel.edit', model_full_permit(TbPaychannel), model_to_name(TbPaychannel), 'model'), 
           
           ('TbPaychanneljoinlevel', model_read_permit(TbPaychanneljoinlevel), model_to_name(TbPaychanneljoinlevel), 'model'), 
           ('TbPaychanneljoinlevel.edit', model_full_permit(TbPaychanneljoinlevel), model_to_name(TbPaychanneljoinlevel), 'model'), 
           #----------------------------------------------------------------
           
           ('TbAccount', model_read_permit(TbAccount), model_to_name(TbAccount), 'model'), 
           ('TbAccount.edit', model_full_permit(TbAccount,write_exclude=['csuserid']), model_to_name(TbAccount), 'model'), 
           ('TbAccount.csuserid',json.dumps({"write":['csuserid']}),model_to_name(TbAccount),'model'),
           ('TbBalancelog', model_read_permit(TbBalancelog), model_to_name(TbBalancelog), 'model'), 
           
           ('TbBankcard', model_read_permit(TbBankcard), model_to_name(TbBankcard), 'model'), 
           ('TbBankcard.edit', model_full_permit(TbBankcard), model_to_name(TbBankcard), 'model'), 
           
           ('TbRecharge', model_read_permit(TbRecharge), model_to_name(TbRecharge), 'model'), 
           ('TbRecharge.edit', model_full_permit(TbRecharge), model_to_name(TbRecharge), 'model'), 
           
           ('TbWithdraw', model_read_permit(TbWithdraw), model_to_name(TbWithdraw), 'model'), 
           ('TbWithdraw.edit', model_full_permit(TbWithdraw), model_to_name(TbWithdraw), 'model'), 
           
           # 关联用户
           ('member.relevent_user','','','single'),
           # 流失用户
           ('member.chum_user','','','single'), 
           
           ('TbUserLog',model_read_permit(TbUserLog),model_to_name(TbUserLog),'model'),
           
           ('TbLoginlog', model_read_permit(TbLoginlog), model_to_name(TbLoginlog), 'model'), 
           
           #------比赛----------------------------------------------
           
           # 老的比赛表名，但是现在对应的新表，为了兼容老的权限
           ('TbMatches', model_read_permit(TbMatch), model_to_name(TbMatch), 'model'), 
           
           ('TbMatch', model_read_permit(TbMatch), model_to_name(TbMatch), 'model'), 
           ('TbMatch.isrecommend',json.dumps({'write':['isrecommend']}),model_to_name(TbMatch),'model'),
           ('TbMatch.hasliveodds',json.dumps({'write':['hasliveodds']}),model_to_name(TbMatch),'model'),
           ('TbMatch.ishidden',json.dumps({'write':['ishidden']}),model_to_name(TbMatch),'model'),
           ('TbMatch.quit_ticket','','','single'),
           ('TbMatches.edit', model_full_permit(TbMatch,exclude=['isrecommend','hasliveodds','ishidden']), model_to_name(TbMatch), 'model'),
           
           ('TbPeriodscore',model_read_permit(TbPeriodscore),model_to_name(TbPeriodscore),'model'), # 比分
           ('TbLivefeed.edit',model_full_permit(TbLivefeed),model_to_name(TbLivefeed),'model'),# 危险球
           
           ('TbMarkets',model_read_permit(TbMarkets),model_to_name(TbMarkets),'model'), # 玩法
           ('TbMarkets.edit',model_full_permit(TbMarkets),model_to_name(TbMarkets),'model'), # 玩法
           
           ('TbMarkethcpswitch.edit',model_full_permit(TbMarkethcpswitch),model_to_name(TbMarkethcpswitch),'model'),
           ('manual_specialbetvalue','TbMarkethcpswitch.edit','','set'), # 封盘
           ('manual_outcome','','','single'), # 手动结算 
        
            
           ('TbTicketmaster', model_read_permit(TbTicketmaster), model_to_name(TbTicketmaster), 'model'), 
           ('TbTicketmaster.edit', model_full_permit(TbTicketmaster), model_to_name(TbTicketmaster), 'model'), 
           ('TbTicketstake', model_read_permit(TbTicketstake), model_to_name(TbTicketstake), 'model'),
           ('TbTicketparlay', model_read_permit(TbTicketparlay), model_to_name(TbTicketparlay), 'model'),
           
           ('TbTicketmaster_all_tab_read', ';'.join(['TbTicketmaster', 'TbTicketstake', 'TbTicketparlay']), '', 'set'), 
           # --------------------------------------------------------------

           ('TbUserConst.edit',model_full_permit(TbUserConst),model_to_name(TbUserConst),'model'),
           ('TbUserRank.edit',model_full_permit(TbUserRank),model_to_name(TbUserRank),'model'),
           
           ('TbParameterinfo', model_read_permit(TbParameterinfo), model_to_name(TbParameterinfo), 'model'), 
           ('TbParameterinfo.edit', model_full_permit(TbParameterinfo), model_to_name(TbParameterinfo), 'model'),
           # IP 黑名单
           ('Blackiprangelist', model_read_permit(Blackiprangelist), model_to_name(Blackiprangelist), 'model'), 
           ('Blackiprangelist.edit', model_full_permit(Blackiprangelist), model_to_name(Blackiprangelist), 'model'),
           
           # 登录地区黑名单
           ('TbAreablacklist', model_read_permit(TbAreablacklist), model_to_name(TbAreablacklist), 'model'), 
           ('TbAreablacklist.edit', model_full_permit(TbAreablacklist), model_to_name(TbAreablacklist), 'model'), 
           
           # 充值用户黑名单
           ('TbPaychannelblackaccount', model_read_permit(TbPaychannelblackaccount), model_to_name(TbPaychannelblackaccount), 'model'), 
           ('TbPaychannelblackaccount.edit', model_full_permit(TbPaychannelblackaccount), model_to_name(TbPaychannelblackaccount), 'model'), 
           # 充值地区黑名单
           ('TbRechargeareablacklist', model_read_permit(TbRechargeareablacklist), model_to_name(TbRechargeareablacklist), 'model'), 
           ('TbRechargeareablacklist.edit', model_full_permit(TbRechargeareablacklist), model_to_name(TbRechargeareablacklist),'model'),
           ('TbPaychannelblackiprange', model_read_permit(TbPaychannelblackiprange), model_to_name(TbPaychannelblackiprange), 'model'), 
           ('TbPaychannelblackiprange.edit', model_full_permit(TbPaychannelblackiprange), model_to_name(TbPaychannelblackiprange), 'model'), 
           
           ('TbWhiteiprangelist', model_read_permit(TbWhiteiprangelist), model_to_name(TbWhiteiprangelist), 'model'), 
           ('TbWhiteiprangelist.edit', model_full_permit(TbWhiteiprangelist), model_to_name(TbWhiteiprangelist), 'model'), 
           
           ('Whiteuserlist', model_read_permit(Whiteuserlist), model_to_name(Whiteuserlist), 'model'), 
           ('Whiteuserlist.edit', model_full_permit(Whiteuserlist), model_to_name(Whiteuserlist), 'model'), 
           
           ('member_statistic', '', '', 'single'), 
           ('platform_profit', '', '', 'single'), 
           
           # 代理用户
           ('agent', '', '', 'single'), 
           ('agent.parent.edit','','','single'),
           #('agent.edit', '', '', 'single'),  # 代理用户的编辑，取决于 TbAccount的权限
           
           #('agent.commission', '', '', 'single'), 
           
           ('risk.parameter', '', '', 'single'), 
           # 代理佣金
           ('TbAgentcommission', model_read_permit(TbAgentcommission), model_to_name(TbAgentcommission), 'model'), 
           ('TbAgentcommission.edit', model_full_permit(TbAgentcommission), model_to_name(TbAgentcommission), 'model'),
           
            ('TbLeagueGroup.edit', model_full_permit(TbLeagueGroup), model_to_name(TbLeagueGroup), 'model'), 
            ('TbLeaguegroupMarketweight.edit',model_full_permit(TbLeaguegroupMarketweight),model_to_name(TbLeaguegroupMarketweight),'model'),
            #('Account_list_write', ';'.join(['TbAccount.edit', 'TbBalancelog.edit', 'TbBankcard.edit', 'TbRecharge.edit', 'TbWithdraw.edit'
                                            #'TbTicketmaster.edit', 'TbLoginlog.edit', 'TbMatches.edit']), '', 'set'),  
           ('TbBonuslog', model_read_permit(TbBonuslog), model_to_name(TbBonuslog), 'model'), 
           ('TbBonuslog.edit', model_full_permit(TbBonuslog), model_to_name(TbBonuslog), 'model'),
           
           ('TbBonustype', model_read_permit(TbBonustype), model_to_name(TbBonustype), 'model'), 
           ('TbBonustype.edit', model_full_permit(TbBonustype), model_to_name(TbBonustype), 'model'),
           
           ('Bonuse-dispatch', ';'.join(['TbBonustype', 'TbBonuslog',]), '', 'set'), 
           ('Bonuse-dispatch.edit', ';'.join(['TbBonuslog.edit', 'TbBonustype.edit',]), '', 'set'), 
         
           ('report.recharge_reports', '', '', 'single'),
           ('TbLimitusergroup',model_read_permit(TbLimitusergroup),model_to_name(TbLimitusergroup),'model'),
           ('TbLimitusergroup.edit',model_full_permit(TbLimitusergroup),model_to_name(TbLimitusergroup),'model'),
           ('risk.RiskcontrolSetting','','','single'),
           
           ('TbBetfullrecord',model_read_permit(TbBetfullrecord),model_to_name(TbBetfullrecord),'model'),
           ('TbBetfullrecord.edit',model_full_permit(TbBetfullrecord),model_to_name(TbBetfullrecord),'model'),
           # 会员全标签  , 因为 TbBetfullrecord.edit 没有权限ui，所以只能在这里做一个集合来取它的值
           # 现在不用这个权限了，全部展开了
           ('TbAccount.all_tab',';'.join(['TbAccount.edit', 'TbBalancelog', 'TbLoginlog', 'TbBankcard', 'TbBankcard.edit', 'TbRecharge.edit',
                                'TbWithdraw.edit','TbBetfullrecord.edit']),'','set'),
           
           ('TbTrendstatistics',model_read_permit(TbTrendstatistics),model_to_name(TbTrendstatistics),'model'),
           
           ('report.betAnalysis',';'.join(['TbTrendstatistics']),'','set'),
           
           ('TbAdjusttemplate.edit',model_full_permit(TbAdjusttemplate),model_to_name(TbAdjusttemplate),'model'),
           
           ('TbDomain.edit',model_full_permit(TbDomain),model_to_name(TbDomain),'model'),
           
           ('TbAdvertisement',model_read_permit(TbAdvertisement),model_to_name(TbAdvertisement),'model'),
           ('TbAdvertisement.edit',model_full_permit(TbAdvertisement),model_to_name(TbAdvertisement),'model'),
           
           #- 即时消息
           #('TbTodolist.edit',model_full_permit(TbTodolist),model_to_name(TbTodolist),'model'),
           ('todolist_1','','','single'),
            ('todolist_2','','','single'),
           ('todolist_100','','','single'),
           
           
           # AG
           ('TbAgaccount',model_read_permit(TbAgaccount),model_to_name(TbAgaccount),'model'),
           ('TbAgaccount.edit',model_full_permit(TbAgaccount),model_to_name(TbAgaccount),'model'),
           ('TbAgprofitloss.edit',model_full_permit(TbAgprofitloss),model_to_name(TbAgprofitloss),'model'),
           ('TbGamemoneyininfo.edit',model_full_permit(TbGamemoneyininfo),model_to_name(TbGamemoneyininfo),'model'),
           ('TbGamemoneyoutinfo.edit',model_full_permit(TbGamemoneyoutinfo),model_to_name(TbGamemoneyoutinfo),'model'),
           
           # 沙巴
           ('TbSportaccount',model_read_permit(TbSportaccount),model_to_name(TbSportaccount),'model'),
           ('TbSportaccount.edit',model_full_permit(TbSportaccount),model_to_name(TbSportaccount),'model'),
           ('TbSportprofitloss.edit',model_full_permit(TbSportprofitloss),model_to_name(TbSportprofitloss),'model'),
           ('TbSportmoneyininfo.edit',model_full_permit(TbSportmoneyininfo),model_to_name(TbSportmoneyininfo),'model'),
           ('TbSportmoneyoutinfo.edit',model_full_permit(TbSportmoneyoutinfo),model_to_name(TbSportmoneyoutinfo),'model'),
           
            # 龙城
           ('TbLcityaccount',model_read_permit(TbLcityaccount),model_to_name(TbLcityaccount),'model'),
           ('TbLcityaccount.edit',model_full_permit(TbLcityaccount),model_to_name(TbLcityaccount),'model'),
           ('TbLcityprofitloss.edit',model_full_permit(TbLcityprofitloss),model_to_name(TbLcityprofitloss),'model'),
           ('TbLcitymoneyininfo.edit',model_full_permit(TbLcitymoneyininfo),model_to_name(TbLcitymoneyininfo),'model'),
           ('TbLcitymoneyoutinfo.edit',model_full_permit(TbLcitymoneyoutinfo),model_to_name(TbLcitymoneyoutinfo),'model'),
           
            # IM
            ('TbImaccount',model_read_permit(TbImaccount),model_to_name(TbImaccount),'model'),
            ('TbImaccount.edit',model_full_permit(TbImaccount),model_to_name(TbImaccount),'model'),
            ('TbImeaccount',model_read_permit(TbImeaccount),model_to_name(TbImeaccount),'model'),
            ('TbImeaccount.edit',model_full_permit(TbImeaccount),model_to_name(TbImeaccount),'model'),
            ('TbImprofitloss.edit',model_full_permit(TbImprofitloss),model_to_name(TbImprofitloss),'model'),
            ('TbImmoneyininfo.edit',model_full_permit(TbImmoneyininfo),model_to_name(TbImmoneyininfo),'model'),
            ('TbImmoneyoutinfo.edit',model_full_permit(TbImmoneyoutinfo),model_to_name(TbImmoneyoutinfo),'model'),
            
            # RG
            ('TbRgaccount',model_read_permit(TbRgaccount),model_to_name(TbRgaccount),'model'),
            ('TbRgaccount.edit',model_full_permit(TbRgaccount),model_to_name(TbRgaccount),'model'),
            ('TbRgprofitloss.edit',model_full_permit(TbRgprofitloss),model_to_name(TbRgprofitloss),'model'),
            ('TbRgmoneyininfo.edit',model_full_permit(TbRgmoneyininfo),model_to_name(TbRgmoneyininfo),'model'),
            ('TbRgmoneyoutinfo.edit',model_full_permit(TbRgmoneyoutinfo),model_to_name(TbRgmoneyoutinfo),'model'),
           
           
           # system
           ('TbUserex',model_read_permit(TbUserex),model_to_name(TbUserex),'model'),
           ('TbUserex.edit',model_full_permit(TbUserex),model_to_name(TbUserex),'model'),
           ]

add_permits(permits)



#permits = [ 
           #('TbMatches', model_full_permit(TbMatches), model_to_name(TbMatches) , 'model'), 
           #('TbTicketmaster', model_full_permit(TbTicketmaster), model_to_name(TbTicketmaster), 'model'), 
           #('TbTicketstake', model_full_permit(TbTicketstake), model_to_name(TbTicketstake), 'model'), 
           #('TbTicketparlay', model_full_permit(TbTicketparlay), model_to_name(TbTicketparlay), 'model'), 
           
            #('TbTicketmaster.all', 'TbTicketmaster;TbTicketstake;TbTicketparlay', '', 'set'), 
           #]

#add_permits(permits)  

#permits = [('TbAccount', model_full_permit(TbAccount), model_to_name(TbAccount), 'model'),
           #('TbLoginlog', model_full_permit(TbLoginlog), model_to_name(TbLoginlog), 'model'),
           #('TbBalancelog', model_full_permit(TbBalancelog), model_to_name(TbBalancelog), 'model'),
           #('TbAccount.all', 'TbAccount;TbLoginlog;TbBalancelog;TbTicketmaster', '', 'set'),
           #]

#add_permits(permits)

#permits = [('TbBanner', model_full_permit(TbBanner), model_to_name(TbBanner) , 'model'), 
           #('TbAppversion', model_full_permit(TbAppversion), model_to_name(TbAppversion) , 'model'), 
           #('TbNotice', model_full_permit(TbNotice), model_to_name(TbNotice), 'model'), 
           #('TbCurrency', model_full_permit(TbCurrency), model_to_name(TbCurrency), 'model'), 
           #('TbQa', model_full_permit(TbQa), model_to_name(TbQa), 'model'), 
           #('TbActivity', model_full_permit(TbActivity), model_to_name(TbActivity), 'model'), 
           #('TbAppresource', model_full_permit(TbAppresource), model_to_name(TbAppresource), 'model')
           #]

#add_permits(permits)

