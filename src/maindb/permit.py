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
           
           #------活动2--------
           ('TbActivityV2', model_read_permit(TbActivityV2), model_to_name(TbActivityV2), 'model'), 
           ('TbActivityV2.edit', model_full_permit(TbActivityV2), model_to_name(TbActivityV2), 'model'), 
           ('TbActivityV2.update_cache', '', '', 'single'), 
           ('TbActivitySettings.edit', model_full_permit(TbActivitySettings), model_to_name(TbActivitySettings), 'model'),
           
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
           ('TbTournament.edit', model_full_permit(TbTournament), model_to_name(TbTournament), 'model'), 
           
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
           
           ('TbPaychannel', model_read_permit(TbPaychannel), model_to_name(TbPaychannel), 'model'), 
           ('TbPaychannel.edit', model_full_permit(TbPaychannel), model_to_name(TbPaychannel), 'model'), 
           
           ('TbPaychanneljoinlevel', model_read_permit(TbPaychanneljoinlevel), model_to_name(TbPaychanneljoinlevel), 'model'), 
           ('TbPaychanneljoinlevel.edit', model_full_permit(TbPaychanneljoinlevel), model_to_name(TbPaychanneljoinlevel), 'model'), 
           #----------------------------------------------------------------
           
           ('TbAccount', model_read_permit(TbAccount), model_to_name(TbAccount), 'model'), 
           ('TbAccount.edit', model_full_permit(TbAccount), model_to_name(TbAccount), 'model'), 
           ('TbBalancelog', model_read_permit(TbBalancelog), model_to_name(TbBalancelog), 'model'), 
           
           ('TbBankcard', model_read_permit(TbBankcard), model_to_name(TbBankcard), 'model'), 
           ('TbBankcard.edit', model_full_permit(TbBankcard), model_to_name(TbBankcard), 'model'), 
           
           ('TbRecharge', model_read_permit(TbRecharge), model_to_name(TbRecharge), 'model'), 
           ('TbRecharge.edit', model_full_permit(TbRecharge), model_to_name(TbRecharge), 'model'), 
           
           ('TbWithdraw', model_read_permit(TbWithdraw), model_to_name(TbWithdraw), 'model'), 
           ('TbWithdraw.edit', model_full_permit(TbWithdraw), model_to_name(TbWithdraw), 'model'), 
           
           
           
           ('TbLoginlog', model_read_permit(TbLoginlog), model_to_name(TbLoginlog), 'model'), 
           
           #------比赛----------------------------------------------
           
           ('TbMatches', model_read_permit(TbMatch), model_to_name(TbMatch), 'model'), 
           ('TbMatches.edit', model_full_permit(TbMatch), model_to_name(TbMatch), 'model'),
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
           
           ('agent', '', '', 'single'), 
           ('agent.edit', '', '', 'single'), 
           
           ('agent.commission', '', '', 'single'), 
           
           ('risk.parameter', '', '', 'single'), 
           
           ('TbAgentcommission', model_read_permit(TbAgentcommission), model_to_name(TbAgentcommission), 'model'), 
           ('TbAgentcommission.edit', model_full_permit(TbAgentcommission), model_to_name(TbAgentcommission), 'model'),
           
            #('TbLeagueGroup.edit', model_full_permit(TbLeagueGroup), model_to_name(TbLeagueGroup), 'model'), 
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
           ('member.chum_user','','','single'), # 流失用户
           #('TbBetfullrecord',model_read_permit(TbBetfullrecord),model_to_name(TbBetfullrecord),'model'),
           #('TbBetfullrecord.edit',model_full_permit(TbBetfullrecord),model_to_name(TbBetfullrecord),'model'),
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

