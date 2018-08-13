# encoding:utf-8
from __future__ import unicode_literals

ACCOUNT_TYPE=(
    (1,'会员'),
    (2,'代理')
)

BALANCE_CAT=(
    (20002,'派彩'),
)

ONLINE_STATUS=(
    (1,'启用'),
    (0,'离线')
)

CHANNEL_STATUS=(
    (0,'close'),
    (1,'open')
)
CHANNEL_CASHFLOW=(
    (1,'Deposit'),
    (0,'Withdrawal')
)
PLATFORM=(
    (1,'IOS'),
    (2,'Android')
)
REQUIRED=(
    (0,'否'),
    (1,'是')
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
    (0, '未确认'), 
    (1, '成功订单'), 
    (2, '已结算'), 
    (11, '有危险球'), 
    (22, '赔率更新划单'), 
    (24, '赔率封盘划单'), 
    (26, '早盘已关盘'), 
    (28, '走地已关盘'), 
    (29, '赛事结束检查关盘'), 
    (30, '手动取消订单'), 
    (31, '赛事/玩法/盘口已关闭')
)

TbTicketmaster_WINBET = (
    (0, '输'), 
    (1, '赢'), 
    (2, '平')
)

