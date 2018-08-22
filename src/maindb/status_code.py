# encoding:utf-8
from __future__ import unicode_literals

ACCOUNT_TYPE = (
    (1, '会员'),
    (2, '代理')
)

BALANCE_CAT = (
    (20002, '派彩'),
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
    (0, '未确认'),
    (1, '已确认'),
    (2, '已结算'),
    (11, '危险球'),
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

MATCH_STATUS = (
    (0, '未开赛'),
    (6, '上半场'),
    (7, '下半场'),
    (31, '中场休息'),
    (100, '全场结束'),
)

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
    (1, '待处理'),
    (2, '成功'),
    (3, '失败')
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
