# encoding:utf-8
from __future__ import unicode_literals

ACCOUNT_TYPE = (
    (0, '普通'),
    (1, '内部')
)

COMMON_STATUS = (
    (1, '启用'),
    (0, '禁用')
)

ONLINE_STATUS = (
    (1, '启用'),
    (0, '离线')
)

CHANNEL_STATUS = (
    (0, 'close'),
    (1, 'open')
)
CHANNEL_CASHFLOW = (
    (1, 'Deposit'),
    (0, 'Withdrawal')
)
PLATFORM = (
    (1, 'IOS'),
    (2, 'Android')
)
REQUIRED = (
    (0, '否'),
    (1, '是')
)

TEAM_STATUS = (
    (0, '初始'),
    (1, '人工')
)

periodtype_CHOICE = (
    (0, '全场'),
    (1, '半场')
)

LIMIT_TYPE = (
    (11, '赛事整场'),
    (12, '赛事玩法'),
    (13, '赛事用户等级'),
    (21, '用户整场'),
    (22, '用户玩法')
)

TbTicketmaster_STATUS = (
    (0, '确认中'),
    (1, '未结算'),
    (2, '已结算'),
    # (11, '危险球'),
    (-1, '已作废')
    # (11, '危险球'),
    # (22, '赔率更新划单'),
    # (24, '赔率封盘划单'),
    # (26, '早盘已关盘'),
    # (28, '走地已关盘'),
    # (29, '赛事结束检查关盘'),
    # (30, '手动取消订单'),
    # (31, '赛事/玩法/盘口已关闭')
)

TicketStake_STATUS = (
    (0, '注单建立'),
    (1, '赔率确认'),
    (21, '中注'),
    (22, '输半'),
    (23, '赢半'),
    (24, '全退'),
    (91, '未中'),
    (81, '赔率封盘')
)

TbTicketmaster_WINBET = (
    (0, '输'),
    (1, '赢'),
    (2, '平')
)

ACCOUNT_STATUS = (
    (0, '禁用'),
    (1, '激活')
)

VIP_LEVEL = (
    (1, '青铜'),
    (2, '白银'),
    (3, '黄金'),
    (4, '钻石'),
    (5, '皇冠')
)

NEW_MATCH_STATUS=(
    (0, '未开赛'),
    (6, '上半场'),
    (7,'下半场'),
    (13,'第一节'),
    (14,'第二节'),
    (15,'第三节'),
    (16,'第四节'),
    (31,'中场休息'),
    (32,'等待加时赛'),
    (34,'等待点球大战'),
    (40,'加时赛'),
    (41,'加时赛上半场'),
    (42,'加时赛下半场'),
    (50,'点球大战'),
    (90,'已取消'),
    (100,'全场结束'),
    (110,'加时赛结束'),
    (120,'点球大战结束'),
    (301,'第一次暂停'),
    (302,'第二次暂停'),
    (303,'第三次暂停'),
)


#MATCH_STATUS = (
    #(-1,'已取消'),
    #(0, '未开赛'),
    #(6, '上半场'),
    #(7, '下半场'),
    #(31, '中场休息'),
    #(100, '全场结束'),
#)
#BASKETBALL_MATCH_STATUS = (
    #(-1,'已取消'),
    #(0, '未开赛'),
    #(11, '上半场'),
    #(55, '下半场'),
    #(1, '第一节开始'),
    #(2, '第一节结束'),
    #(3, '第二节开始'),
    #(4, '上半场结束'),
    #(5, '第三节开始'),
    #(6, '第三节结束'),
    #(7, '第四节开始'),
    #(8, '第四节结束'),
    #(9, '加时赛开始'),
    #(100, '全场结束'),
#)

MATCH_MARKETSTATUS = (
    (1, '早盘'),
    (2, '滚球'),
    (3, '关闭')
)

MATCH_CLOSELIVEBET = (
    (0, '滚球'),
    (1, '关闭滚球')
)
RECHARGE_STATUS = (
    (1, '未充值'),
    (2, '成功'),
    (3, '失败')
)
WITHDRAW_STATUS = (
    (1, '处理中'),
    (2, '成功'),
    (3, '失败'),
    (4, '异常'),
    (5, '已退款')
)
AMOUNT_TYPE = (
    (1, '余额'),
    (2, '佣金')
)
WINNER = (
    (0, '--'),
    (1, '主胜'),
    (2, '客胜'),
    (3, '平')
)

AGENT_COMMISION_STATUS = (
    (0, '未审核'),
    (1, '审核中'),
    (2, '已发放'),
)

Account_Source = (
    (0, 'APP注册'),
    (1, '推广链接'),
    (2, '代理添加'), 
    (3, '后台添加'), 
)
WhiteIP_Type = (
    (0, '登录'),
    (1, '充值')
)

SPORTID_OPTION = (
    (0, '足球'), 
    (1, '篮球')
)

SPORTID_OPTION_2=(
    (1,'足球'),
    (2,'篮球'),
    (110,'英雄联盟'),
)


RANK_TYPE = (
    (1, '盈利榜'), 
    (2, '大奖榜'), 
    (3, '胜率榜'), 
   
)

RANK_PERIAD = (
    (1, '日'), 
    (2, '周'), 
    (4, '月')
)

BANNER_DISPLAYTYPE=(
    (0,'对外'),
    (1,'对内')
)

ACTIVITY_COM=(
    ('com-shouchun','首存再存'),
)


ODDSKIND=(
    (1,'早盘'),
    (2,'走地')
)

DATA_SOURCE=(
    (1,'Sportative'),
    (2,'Betrader')
)

AUDIT_OPTIONS=(
    (0,'正常注单'),
    (1,'异常注单')
)