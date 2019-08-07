
import maindb
import helpers
import django
import hello
page_dc = {
    "kv"	:helpers.common.admin.KvTablePage,
    "kv.edit"	:helpers.common.admin.KvFormPage,
    "del_rows"	:helpers.director.fields.delpage.DelPage,
    "log"	:helpers.director.log.logpage.LogPage,
    "user"	:helpers.director.admin.UserTablePage,
    "user.edit"	:helpers.director.admin.UserFormPage,
    "group"	:helpers.director.admin.GroupTablePage,
    "group.edit"	:helpers.director.admin.GroupFormPage,
    "permit.edit"	:helpers.director.admin.PermitFormPage,
    "group_human"	:helpers.director.admin.GroupGroup,
    "group_human.edit"	:helpers.director.access.assem_group.AssemGroupPage,
    "jb_user"	:helpers.case.jb_admin.admin.UserPage,
    "jb_group"	:helpers.case.jb_admin.admin.GroupPage,
    "matches"	:maindb.matches.matches.MatchsPage,
    "tickets"	:maindb.matches.ticket_master.TicketMasterPage,
    "matches_statistics"	:maindb.matches.matches_statistics.MatchesStatisticsPage,
    "ChargeFlow"	:maindb.money.chargeflow.ChargeFlowPage,
    "balancelog"	:maindb.money.balancelog.BalancelogPage,
    "bankcards"	:maindb.member.bankcard.BankCard,
    "recharge"	:maindb.money.recharge.RechargePage,
    "withdraw"	:maindb.money.withdraw.WithdrawPage,
    "loginlog"	:maindb.member.loginlog.LoginLogPage,
    "user_statistics"	:maindb.report.user_statistics.UserStatisticsPage,
    "account"	:maindb.member.account.AccountPage,
    "operation_log"	:maindb.member.operation_log.OperationLog,
    "ReleventUser"	:maindb.member.relevent_user.ReleventUserPage,
    "chum_user"	:maindb.member.chum_user.ChumUser,
    "maindb.TbOdds"	:maindb.matches.odds.OddsPage,
    "basketball_matchs"	:maindb.matches.basketball_matches.BasketMatchsPage,
    "BasketballMatchesStatisticsPage"	:maindb.matches.basketball_matches_statistics.BasketballMatchesStatisticsPage,
    "adjusttemplate"	:maindb.matches.ajusttemplate.AdjusttemplatePage,
    "banner"	:maindb.marketing.banner.BannerPage,
    "notice"	:maindb.marketing.notice.NoticePage,
    "currency"	:maindb.basic_data.currency.CurrencyPage,
    "help"	:maindb.marketing.help_center.HelpPage,
    "activity"	:maindb.marketing.activity.ActivityPage,
    "app_resource"	:maindb.basic_data.app_resource.AppResource,
    "app_package"	:maindb.marketing.app_package.AppPackage,
    "agentnotice"	:maindb.marketing.agent_notice.AgentNoticePage,
    "activity_v2"	:maindb.marketing.active_v2.ActiviyV2Page,
    "rankuser"	:maindb.marketing.rank.RankUserPage,
    "rank"	:maindb.marketing.rank.RankPage,
    "blackip_range"	:maindb.riskcontrol.black_users.BlackIPRangeListPage,
    "white_ips"	:maindb.riskcontrol.black_users.WhiteIpListPage,
    "white_users"	:maindb.riskcontrol.black_users.WhiteUserListPage,
    "bonuspage"	:maindb.marketing.bonus_dispatch.BonusPage,
    "feedback"	:maindb.marketing.feedback.Feedback,
    "agent_qa"	:maindb.marketing.agent_qa.AgentQAPage,
    "advertise"	:maindb.marketing.advertisement.AdvertisementPage,
    "maindb.report.channel"	:maindb.report.report_channel.ReportChnnel,
    "platform_profit"	:maindb.report.platform_profit.PlatformProfit,
    "recharge_reports"	:maindb.report.recharge_report.RechargeReport,
    "everyday_report"	:maindb.report.every_day.EveryDayReportPage,
    "bet_analysis"	:maindb.report.bet_analysis.BetAnalysisPage,
    "activityrecord"	:maindb.report.active_record.ActivityRecordPage,
    "bet_type"	:maindb.basic_data.bet_type.BetTypePage,
    "league"	:maindb.basic_data.league.League,
    "teams"	:maindb.basic_data.teams.TeamsPage,
    "banktypes"	:maindb.basic_data.banktypes.BankTypesPage,
    "paychannel"	:maindb.basic_data.paychannel.PayChannelPage,
    "sportstype"	:maindb.basic_data.sporttype.SportsTypesPage,
    "teams_basketball"	:maindb.basic_data.teams_basketball.TeamBasketballPage,
    "LeagueGroupPage"	:maindb.riskcontrol.admin_league_group.LeagueGroupPage,
    "ParameterPage"	:maindb.riskcontrol.admin_parameter.ParameterPage,
    "sourececontrol"	:maindb.riskcontrol.sourcecontral.SourceControlPage,
    "Paychannelblackaccount"	:maindb.riskcontrol.paychannel_blackaccount.PaychannelblackaccountPage,
    "limitusergroup"	:maindb.riskcontrol.limitusergroup.LimitUserGroupPage,
    "RiskcontrolSetting"	:maindb.riskcontrol.riskcontrol_setting.RiskcontrolSetting,
    "withdraw_limit"	:maindb.riskcontrol.withdraw_limit.WithdrawLimitPage,
    "paychannel_blackip"	:maindb.riskcontrol.paychannel_blackiprange.PayChannelBlackIPRangeList,
    "area_blacklist"	:maindb.riskcontrol.area_blacklist.AreaBlackList,
    "paychannel_area_blacklist"	:maindb.riskcontrol.paychannel_area_blacklist.PayChannelAreaBlackList,
    "white_ip_rangelist"	:maindb.riskcontrol.white_ip_rangelist.WhiteIPRangeList,
    "vip_paychannel"	:maindb.money.vip_paychannel.VIPPayChannelPage,
    "agent_user"	:maindb.admin_agent.agentuser.AgentUser,
    "agent_commission"	:maindb.admin_agent.agent_commission.AgentCommission,
    "parameterinfo"	:maindb.riskcontrol.new_withdraw_limit.WithDrawLimitContralPage,
    "todolist"	:maindb.admin_todolist.TodoList,
    "domain"	:maindb.yunwei.domain.DomainPage,
    "badurl"	:maindb.yunwei.badurl.BadurlPage,
    "marketgroup"	:maindb.programer.marketgroup.MarketGroupPage,
    "marketpage"	:maindb.programer.market.MarketPage,
    "usermarket"	:maindb.programer.market.UserMarketPage,
    "outcome"	:maindb.programer.outcome.OutcomePage,
    "marketsport"	:maindb.programer.marketsport.MarketSportPage,
    "home"	:hello.admin.Home,
    
    # 三方网站比赛匹配
    "web_match_data"	:maindb.matches.event_match.OtherWebMatchPage,
    "newleaguegroup"	:maindb.riskcontrol.new_league_group.LeagueGroupPage,
}
director = {
    "cloudfile_uploader"	:maindb.cus_models_fields.CloudFileUploader,
    "permit.programer"	:helpers.director.admin.PermitPage.PermitTable,
    "permit.programer.edit"	:helpers.director.admin.PermitFormPage.PermitForm,
    "jb_user"	:helpers.case.jb_admin.admin.UserPage.tableCls,
    "jb_user.edit"	:helpers.case.jb_admin.admin.UserFields,
    "jb_group"	:helpers.case.jb_admin.admin.GroupPage.tableCls,
    "jb_group.edit"	:helpers.case.jb_admin.admin.GroupForm,
    "authuser.regist"	:helpers.authuser.admin_regist.RegistFormPage.fieldsCls,
    "PeriodScoreTab"	:maindb.matches.matches.PeriodScoreTab,
    "match.table"	:maindb.matches.matches.MatchsPage.tableCls,
    "match.table.edit"	:maindb.matches.matches.MatchForm,
    "outcome_tab"	:maindb.matches.matches.OutcomeTab,
    "TbLivescout.table"	:maindb.matches.matches.TbLivescoutTable,
    "games.ticketmaster"	:maindb.matches.ticket_master.TicketMasterPage.tableCls,
    "games.ticketmaster.edit"	:maindb.matches.ticket_master.TicketMasterForm,
    "games.TicketstakeTable"	:maindb.matches.ticket_master.TicketstakeTable,
    "games.TicketparlayTable"	:maindb.matches.ticket_master.TicketparlayTable,
    "games.ticketstake.matchform"	:maindb.matches.ticket_master.MatchForm,
    "match.viewbymatch"	:maindb.matches.matches_statistics.MatchesStatisticsPage.tableCls,
    "DetailStatistic"	:maindb.matches.matches_statistics.DetailStatistic,
    "match_statistic.ticket_master"	:maindb.matches.matches_statistics.TickmasterTab,
    "match_statistic.ticket_master.edit"	:maindb.matches.ticket_master.TicketMasterForm,
    "ChargeFlow"	:maindb.money.chargeflow.ChargeFlowPage.tableCls,
    "money.balancelog"	:maindb.money.balancelog.BalancelogPage.tableCls,
    "BankCards"	:maindb.member.bankcard.BankCard.tableCls,
    "BankCards.edit"	:maindb.member.bankcard.BankCardForm,
    "Recharge"	:maindb.money.recharge.RechargePage.tableCls,
    "Recharge.edit"	:maindb.money.recharge.ConfirmRechargeForm,
    "tab.ticketmaster"	:maindb.money.withdraw.TicketmasterTab,
    "Withdraw"	:maindb.money.withdraw.WithdrawPage.tableCls,
    "Withdraw.edit"	:maindb.money.withdraw.WithDrawForm,
    "account.loginpage"	:maindb.member.loginlog.LoginLogPage.tableCls,
    "UserStatisticsPage"	:maindb.report.user_statistics.UserStatisticsPage.tableCls,
    "account"	:maindb.member.account.AccountPage.tableCls,
    "account.edit"	:maindb.member.account.AccoutBaseinfo,
    "account.base.edit"	:maindb.member.account.AccoutBaseinfo,
    "account.amount.edit"	:maindb.member.account.AccoutModifyAmount,
    "account.betfullmodify"	:maindb.member.account.ModifyBetFullRecord,
    "account.bankcard"	:maindb.member.account.UserBankCard,
    "account.bankcard.edit"	:maindb.member.bankcard.BankCardForm,
    "account.UserRecharge"	:maindb.member.account.UserRecharge,
    "account.UserWithdraw"	:maindb.member.account.UserWithdraw,
    "account.log"	:maindb.member.account.AccountLoginTable,
    "account.ticketmaster"	:maindb.member.account.AccountTicketTable,
    "account.balancelog"	:maindb.member.account.AccountBalanceTable,
    "account.statistc"	:maindb.member.account.UserStatisticsTab,
    "account.matches_statistics"	:maindb.member.account.MatchesStatisticsTab,
    "account.betfullrecordtab"	:maindb.member.account.BetFullRecordTab,
    "OperationLog"	:maindb.member.operation_log.OperationLog.tableCls,
    "OperationLog.edit"	:maindb.member.operation_log.OperationLogForm,
    "ReleventUser"	:maindb.member.relevent_user.ReleventUserPage.tableCls,
    "chum_user"	:maindb.member.chum_user.ChumUser.tableCls,
    "maindb.OddsTypeGroup4Table"	:maindb.matches.odds.OddsTypeGroup4Table,
    "maindb.typegroup_2"	:maindb.matches.odds.OddsTypeGroup2Table,
    "basketball.manul_outcome"	:maindb.matches.basketball_matches.BasketOutcome,
    "basketball_matchs"	:maindb.matches.basketball_matches.BasketMatchsPage.tableCls,
    "basketball_matchs.edit"	:maindb.matches.basketball_matches.BasketMatchForm,
    "BasketballMatchesStatisticsPage"	:maindb.matches.basketball_matches_statistics.BasketballMatchesStatisticsPage.tableCls,
    "BasketballDetailStatistic"	:maindb.matches.basketball_matches_statistics.BasketballDetailStatistic,
    "adjusttemplate"	:maindb.matches.ajusttemplate.AdjusttemplatePage.tableCls,
    "adjusttemplate.edit"	:maindb.matches.ajusttemplate.AjusttemplateForm,
    "banner.table"	:maindb.marketing.banner.BannerPage.tableCls,
    "banner.table.edit"	:maindb.marketing.banner.BannerForm,
    "notice.table"	:maindb.marketing.notice.NoticePage.tableCls,
    "notice.table.edit"	:maindb.marketing.notice.NoticeForm,
    "currency.table"	:maindb.basic_data.currency.CurrencyPage.tableCls,
    "currency.table.edit"	:maindb.basic_data.currency.CurrencyForm,
    "help.table"	:maindb.marketing.help_center.HelpPage.tableCls,
    "help.table.edit"	:maindb.marketing.help_center.HelpForm,
    "get_mtype_options"	:maindb.marketing.help_center.get_mtype_options,
    "gen_help_static_file"	:maindb.marketing.help_center.HelpPage.tableCls.gen_help_static_file,
    "activity.table"	:maindb.marketing.activity.ActivityPage.tableCls,
    "activity.table.edit"	:maindb.marketing.activity.ActiveForm,
    "AppResource"	:maindb.basic_data.app_resource.AppResource.tableCls,
    "AppResource.edit"	:maindb.basic_data.app_resource.AppResourceForm,
    "app_pkg"	:maindb.marketing.app_package.AppPackage.tableCls,
    "app_pkg.edit"	:maindb.marketing.app_package.AppPackageForm,
    "agentnotice"	:maindb.marketing.agent_notice.AgentNoticePage.tableCls,
    "agentnotice.edit"	:maindb.marketing.agent_notice.NoticeForm,
    "activity_v2"	:maindb.marketing.active_v2.ActiviyV2Page.tableCls,
    "activity_v2.edit"	:maindb.marketing.active_v2.ActivityV2Form,
    "activity_v2.setting"	:maindb.marketing.active_v2.ActivitySettingTable,
    "activity_v2.setting.edit"	:maindb.marketing.active_v2.ActivitySettingForm,
    "rankuser"	:maindb.marketing.rank.RankUserPage.tableCls,
    "rankuser.edit"	:maindb.marketing.rank.RankUserForm,
    "rank"	:maindb.marketing.rank.RankPage.tableCls,
    "rank.edit"	:maindb.marketing.rank.RankForm,
    "risk.WhiteIpListPage"	:maindb.riskcontrol.black_users.WhiteIpListPage.tableCls,
    "risk.WhiteIpListPage.edit"	:maindb.riskcontrol.black_users.WhiteIPForm,
    "risk.WhiteuserlistPage"	:maindb.riskcontrol.black_users.WhiteUserListPage.tableCls,
    "risk.WhiteuserlistPage.edit"	:maindb.riskcontrol.black_users.WhiteUserForm,
    "risk.AccountSelect"	:maindb.riskcontrol.black_users.AccountSelect,
    "risk.BlankipRangeListPage"	:maindb.riskcontrol.black_users.BlackIPRangeListPage.tableCls,
    "risk.BlankipRangeListPage.edit"	:maindb.riskcontrol.black_users.BlackIPRangeForm,
    "bonuslog_list"	:maindb.marketing.bonus_dispatch.BonuslogTable,
    "bonuslog_list.edit"	:maindb.marketing.bonus_dispatch.BonuslogForm,
    "bonustype"	:maindb.marketing.bonus_dispatch.BonusTypeTable,
    "bonustype.edit"	:maindb.marketing.bonus_dispatch.BonusTypeForm,
    "feedback.table"	:maindb.marketing.feedback.Feedback.tableCls,
    "feedback.table.edit"	:maindb.marketing.feedback.FeedbackForm,
    "agent_qa"	:maindb.marketing.agent_qa.AgentQAPage.tableCls,
    "agent_qa.edit"	:maindb.marketing.agent_qa.AgentQAForm,
    "advertise"	:maindb.marketing.advertisement.AdvertisementPage.tableCls,
    "advertise.edit"	:maindb.marketing.advertisement.AdvertiseForm,
    "maindb.report.channel"	:maindb.report.report_channel.ReportChnnel.tableCls,
    "platform_profit"	:maindb.report.platform_profit.PlatformProfit.tableCls,
    "recharge_reports"	:maindb.report.recharge_report.RechargeReport.tableCls,
    "everyday_report"	:maindb.report.every_day.EveryDayReportPage.tableCls,
    "WinbetRatio"	:maindb.report.bet_analysis.WinbetRatio,
    "LoginNumer"	:maindb.report.bet_analysis.LoginNumer,
    "BetCondition"	:maindb.report.bet_analysis.BetCondition,
    "BetWeekChart"	:maindb.report.bet_analysis.BetWeekChart,
    "MarketAnalysis"	:maindb.report.bet_analysis.MarketAnalysis,
    "TournamentAnalysis"	:maindb.report.bet_analysis.TournamentAnalysis,
    "ReportTicketState"	:maindb.report.bet_analysis.ReportTicketState,
    "ReportTicketSummary"	:maindb.report.bet_analysis.ReportTicketSummary,
    "activityrecord"	:maindb.report.active_record.ActivityRecordPage.tableCls,
    "maindb.TbOddstypeGroupPage"	:maindb.basic_data.bet_type.BetTypePage.tableCls,
    "maindb.TbOddstypeGroupPage.edit"	:maindb.basic_data.bet_type.BetTypeForm,
    "match.league"	:maindb.basic_data.league.League.tableCls,
    "match.league.edit"	:maindb.basic_data.league.LeagueForm,
    "maindb.teams"	:maindb.basic_data.teams.TeamsPage.tableCls,
    "maindb.teams.edit"	:maindb.basic_data.teams.TeamsFields,
    "league-options"	:maindb.basic_data.teams.TeamsPage.tableCls.filters.getLeagueOptions,
    "contry-options"	:maindb.basic_data.teams.TeamsPage.tableCls.filters.getCountry,
    "banktypes"	:maindb.basic_data.banktypes.BankTypesPage.tableCls,
    "banktypes.edit"	:maindb.basic_data.banktypes.BankTypesForm,
    "paychannel"	:maindb.basic_data.paychannel.PayChannelPage.tableCls,
    "paychannel.edit"	:maindb.basic_data.paychannel.PayChannelForm,
    "sportstype"	:maindb.basic_data.sporttype.SportsTypesPage.tableCls,
    "sportstype.edit"	:maindb.basic_data.sporttype.SportsTypeForm,
    "teams_basketball"	:maindb.basic_data.teams_basketball.TeamBasketballPage.tableCls,
    "teams_basketball.edit"	:maindb.basic_data.teams_basketball.TeamsBasketballFields,
    "LeagueGroupPage"	:maindb.riskcontrol.admin_league_group.LeagueGroupPage.tableCls,
    "LeagueGroupPage.edit"	:maindb.riskcontrol.admin_league_group.LeagueGroupForm,
    "LeagueidInGroupForm"	:maindb.riskcontrol.admin_league_group.LeagueidInGroupForm,
    "LeagueGroupSpreadForm"	:maindb.riskcontrol.admin_league_group.LeagueGroupSpreadForm,
    "ParameterForm"	:maindb.riskcontrol.admin_parameter.ParameterPage.fieldsCls,
    "sourececontrol"	:maindb.riskcontrol.sourcecontral.SourceControlPage.tableCls,
    "sourececontrol.edit"	:maindb.riskcontrol.sourcecontral.SoureceControlForm,
    "Paychannelblackaccount"	:maindb.riskcontrol.paychannel_blackaccount.PaychannelblackaccountPage.tableCls,
    "Paychannelblackaccount.edit"	:maindb.riskcontrol.paychannel_blackaccount.PaychannelblackaccountForm,
    "limitusergroup"	:maindb.riskcontrol.limitusergroup.LimitUserGroupPage.tableCls,
    "limitusergroup.edit"	:maindb.riskcontrol.limitusergroup.LimitUserForm,
    "RiskcontrolSetting"	:maindb.riskcontrol.riskcontrol_setting.RiskcontrolSetting.tableCls,
    "RiskcontrolForm"	:maindb.riskcontrol.riskcontrol_setting.RiskcontrolForm,
    "withdraw_limit"	:maindb.riskcontrol.withdraw_limit.WithdrawLimitPage.fieldsCls,
    "PayChannelBlackIPRangeList"	:maindb.riskcontrol.paychannel_blackiprange.PayChannelBlackIPRangeList.tableCls,
    "PayChannelBlackIPRangeList.edit"	:maindb.riskcontrol.paychannel_blackiprange.PayChannelBlackIPRangeForm,
    "AreaBlackList"	:maindb.riskcontrol.area_blacklist.AreaBlackList.tableCls,
    "AreaBlackList.edit"	:maindb.riskcontrol.area_blacklist.AreaBlackListForm,
    "PayChannelAreaBlackList"	:maindb.riskcontrol.paychannel_area_blacklist.PayChannelAreaBlackList.tableCls,
    "PayChannelAreaBlackList.edit"	:maindb.riskcontrol.paychannel_area_blacklist.PayChannelAreaBlackListForm,
    "WhiteIPRangeList"	:maindb.riskcontrol.white_ip_rangelist.WhiteIPRangeList.tableCls,
    "WhiteIPRangeList.edit"	:maindb.riskcontrol.white_ip_rangelist.WhiteIPRangeForm,
    "ChargeType"	:maindb.money.vip_paychannel.VIPPayChannelPage.tableCls,
    "ChargeType.edit"	:maindb.money.vip_paychannel.ChargeTypeForm,
    "get_no_relation_vip_level"	:maindb.money.vip_paychannel.get_left_vip_options,
    "YongJingForm"	:maindb.admin_agent.agentuser.YongJingForm,
    "agent.parentselect"	:maindb.admin_agent.agentuser.ParentSelect,
    "agent.ParentForm"	:maindb.admin_agent.agentuser.ParentForm,
    "AgentUser"	:maindb.admin_agent.agentuser.AgentUser.tableCls,
    "new_AgentUser"	:maindb.admin_agent.agentuser.NewAgentUserForm,
    "agent_commission"	:maindb.admin_agent.agent_commission.AgentCommission.tableCls,
    "agent_commission.audit"	:maindb.admin_agent.agent_commission.AgentCommission.tableCls.audit,
    "agent_commission.onekey_all"	:maindb.admin_agent.agent_commission.AgentCommission.tableCls.onekey_audit_all,
    "parameterinfo"	:maindb.riskcontrol.new_withdraw_limit.WithDrawLimitContralPage.tableCls,
    "parameterinfo.edit"	:maindb.riskcontrol.new_withdraw_limit.WithDrawForm,
    "todolist"	:maindb.admin_todolist.TodoList.tableCls,
    "todolist.edit"	:maindb.admin_todolist.TodoForm,
    "domain"	:maindb.yunwei.domain.DomainPage.tableCls,
    "domain.edit"	:maindb.yunwei.domain.DomainForm,
    "badurl"	:maindb.yunwei.badurl.BadurlPage.tableCls,
    "marketgroup"	:maindb.programer.marketgroup.MarketGroupPage.tableCls,
    "marketgroup.edit"	:maindb.programer.marketgroup.MarketGroupForm,
    "Marketgroupwithmarket"	:maindb.programer.marketgroup.MarketgroupwithmarketTable,
    "Marketgroupwithmarket.edit"	:maindb.programer.marketgroup.MarketgroupwithmarketForm,
    "get_market_options"	:maindb.programer.marketgroup.get_market_options,
    "marketpage"	:maindb.programer.market.MarketPage.tableCls,
    "marketpage.edit"	:maindb.programer.market.MarketForm,
    "usermarket"	:maindb.programer.market.UserMarketPage.tableCls,
    "usermarket.edit"	:maindb.programer.market.UserMarketForm,
    "outcome"	:maindb.programer.outcome.OutcomePage.tableCls,
    "outcome.edit"	:maindb.programer.outcome.OutcomeForm,
    "marketsport"	:maindb.programer.marketsport.MarketSportPage.tableCls,
    "marketsport.edit"	:maindb.programer.marketsport.MarketSportForm,
    
    "web_match_data"	:maindb.matches.event_match.OtherWebMatchPage.tableCls,
    "web_match_data.edit_self"	:maindb.matches.event_match.WebMatchForm,
    "matchpicker"	:maindb.matches.event_match.MatchPicker,
    "newleaguegroup"	:maindb.riskcontrol.new_league_group.LeagueGroupPage.tableCls,
    "newleaguegroup.edit"	:maindb.riskcontrol.new_league_group.LeagureGroupForm,
}
director_views = {
    "get_row"	:helpers.director.dapi.get_row,
    "save_rows"	:helpers.director.dapi.save_rows,
    "do_login"	:helpers.authuser.admin_login.do_login,
    "match.quit_ticket"	:maindb.matches.matches.quit_ticket,
    "match.livescout_status"	:maindb.matches.matches.match_livescout_status,
    "match.add_livescout"	:maindb.matches.matches.add_livescout,
    "get_special_bet_value"	:maindb.matches.matches.getSpecialbetValue,
    "save_special_bet_value"	:maindb.matches.matches.save_special_bet_value_proc,
    "get_match_outcome_info"	:maindb.matches.matches.get_match_outcome_info,
    "out_com_save"	:maindb.matches.matches.out_com_save,
    "notify_match_recommend"	:maindb.matches.matches.notify_match_recommend,
    "has_audit_ticketmaster"	:maindb.money.withdraw.has_audit_ticketmaster,
    "gen_notice_static"	:maindb.marketing.notice.NoticePage.tableCls.gen_notice_static,
    "update_activity_file"	:maindb.marketing.activity.update_activity_file,
    "update_activity_file_v2"	:maindb.marketing.active_v2.update_activity_file_v2,
    "basketball-contry-options"	:maindb.basic_data.teams_basketball.getCountry,
    "basketball-league-options"	:maindb.basic_data.teams_basketball.getLeagueOptions,
    "league_group.league_options"	:maindb.riskcontrol.admin_league_group.league_options,
    "todolist.hasnew_todolist"	:maindb.admin_todolist.hasnew_todolist,
    "todolist.get_counter"	:maindb.admin_todolist.get_counter,
    "trend_data"	:hello.admin.trend_data,
    "batch_recommand"	:maindb.matches.matches.batch_recommand,
}
sim_signal = {
    "notice.static.changed"	:[maindb.update_cache.clear_notice_cache],
    "help.static.changed"	:[maindb.update_cache.clear_help_cache],
    "tbsetting.maxpayout.changed"	:[maindb.update_cache.clear_maxpayout],
    "tbsetting.quickamount.changed"	:[maindb.update_cache.clear_quickamount],
}
field_map = {
    maindb.cus_models_fields.CusPictureField	:maindb.cus_models_fields.CusPictureMap,
    maindb.cus_models_fields.CusFileField	:maindb.cus_models_fields.CusFielFieldProc,
    maindb.cus_models_fields.CloudFileField	:maindb.cus_models_fields.CloudFileFieldProc,
    helpers.director.model_func.cus_fields.cus_picture.PictureField	:helpers.director.model_func.cus_fields.cus_picture.PictureProc,
    helpers.director.model_func.cus_fields.cus_decimal.CusDecimalField	:helpers.director.model_func.cus_fields.cus_decimal.CusDecimalProc,
    maindb.create_user.CreateUserField	:maindb.create_user.CreateUserProc,
    maindb.create_user.UpdateUserField	:maindb.create_user.UpdateUserPorc,
    django.db.models.fields.DateField	:helpers.director.model_func.field_procs.dateproc.DateProc,
    django.db.models.fields.DateTimeField	:helpers.director.model_func.field_procs.datetimeproc.DateTimeProc,
    django.db.models.fields.DecimalField	:helpers.director.model_func.field_procs.decimalproc.DecimalProc,
    django.db.models.fields.related.ForeignKey	:helpers.director.model_func.field_procs.foreignproc.ForeignProc,
    django.db.models.fields.related.ManyToManyField	:helpers.director.model_func.field_procs.manyproc.ManyProc,
    django.db.models.fields.related.OneToOneField	:helpers.director.model_func.field_procs.oneproc.OneProc,
    django.db.models.fields.CharField	:helpers.director.model_func.field_procs.charproc.CharProc,
    django.db.models.fields.IntegerField	:helpers.director.model_func.field_procs.intproc.IntProc,
    django.db.models.fields.SmallIntegerField	:helpers.director.model_func.field_procs.intproc.IntProc,
    django.db.models.fields.BigIntegerField	:helpers.director.model_func.field_procs.intproc.BigProc,
    django.db.models.fields.BooleanField	:helpers.director.model_func.field_procs.boolproc.BoolProc,
    django.db.models.fields.TextField	:helpers.director.model_func.field_procs.textproc.TextProc,
    django.db.models.fields.NullBooleanField	:helpers.director.model_func.field_procs.nullboolproc.NullBoolProc,
    "maindb.tbchargeflow.createtime"	:maindb.money.chargeflow.CreateTimeProc,
    "maindb.tbaccount.weight"	:maindb.member.account.Digit3,
    "maindb.tbadjusttemplate.adjustsettings"	:maindb.matches.ajusttemplate.AdjustSettingProc,
    "maindb.tbadjusttemplate.status"	:helpers.director.model_func.field_procs.intBoolProc.IntBoolProc,
    "maindb.tbappversion.packageurl"	:maindb.marketing.app_package.AppPkgUrlProc,
    "maindb.tbchargeflow.createdate"	:maindb.report.report_channel.ReportCreatedateProc,
    "maindb.tboddstypegroup.enabled"	:helpers.director.model_func.field_procs.intBoolProc.IntBoolProc,
    "maindb.tbtournament.issubscribe"	:helpers.director.model_func.field_procs.intBoolProc.IntBoolProc,
    "maindb.tbtournament.closelivebet"	:helpers.director.model_func.field_procs.intBoolProc.IntBoolProc,
    "maindb.tbtournament.typegroupswitch"	:helpers.director.model_func.field_procs.dotStrArray.DotStrArrayProc,
    "maindb.tbteams.icon"	:maindb.basic_data.teams.TeamIconProc,
    "maindb.tbteamsbasketball.icon"	:maindb.basic_data.teams_basketball.TeamBasketballIconProc,
    "maindb.tbareablacklist.status"	:helpers.director.model_func.field_procs.intBoolProc.IntBoolProc,
    "maindb.tbrechargeareablacklist.status"	:helpers.director.model_func.field_procs.intBoolProc.IntBoolProc,
    "maindb.tbleaguegroup.enabled"	:helpers.director.model_func.field_procs.intBoolProc.IntBoolProc,
}
