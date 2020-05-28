# encoding:utf-8
from __future__ import unicode_literals
from django.conf import settings

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

IS_AUTO = (
    (0,'手动'),
    (1,'自动'),
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
    (11, '危险球'),
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
    (0, '确认中'),
    (1, '已确认'),
    (21, '中注'),
    (22, '输半'),
    (23, '赢半'),
    (24, '平'),
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
ACCOUNT_AGENT_STATUS = (
    (0,'关闭'),
    (1,'开启'),
)

VIP_LEVEL = (
    (1, '青铜'),
    (2, '白银'),
    (3, '黄金'),
    (4, '钻石'),
    (5, '皇冠')
)

NEW_MATCH_STATUS=(
    (0, "未开赛"),
            (1, "第一节"),
            (2, "第二节"),
            (3, "第三节"),
            (4, "第四节"),
            (5, "第五节"),
            (6, "上半场"),
            (7, "下半场"),
            (8, "第一盘"),
            (9, "第二盘"),
            (10, "第三盘"),
            (11, "第四盘"),
            (12, "第五盘"),
            (13, "第一节"),
            (14, "第二节"),
            (15, "第三节"),
            (16, "第四节"),
            (17, "金局"),
            (20, "已开始"),
            (21, "进行中"),
            (22, "比赛即将开始"),
            (30, "暂停"),
            (31, "半场结束"),
            (32, "等待加时赛"),
            (33, "加时赛中场"),
            (34, "等待点球决胜"),
            (35, "等待点球决胜"),
            (36, "等待点球大战"),
            (37, "等待金局"),
            (40, "加时"),
            (41, "加时第一节"),
            (42, "加时第二节"),
            (50, "点球"),
            (51, "点球"),
            (52, "点球"),
            (60, "延期"),
            (61, "推迟开赛"),
            (70, "取消"),
            (71, "第1场比赛"),
            (72, "第2场比赛"),
            (73, "第3场比赛"),
            (74, "第4场比赛"),
            (75, "第5场比赛"),
            (76, "第6场比赛"),
            (77, "第7场比赛"),
            (80, "中断"),
            (81, "停赛"),
            (90, "弃赛"),
            (91, "单独完成赛事直接获胜"),
            (92, "退出"),
            (93, "主队大胜"),
            (94, "客队大胜"),
            (95, "主队弃赛,客队胜"),
            (96, "客队弃赛,主队胜"),
            (97, "主队违规,客队胜"),
            (98, "客队违规,主队胜"),
            (99, "唯一赛果"),
            (100, "比赛结束"),
            (110, "加时赛后"),
            (111, "加时赛后"),
            (120, "点球决胜后"),
            (130, "金局后"),
            (141, "第一图"),
            (142, "第二图"),
            (143, "第三图"),
            (144, "第四图"),
            (145, "第五图"),
            (146, "第六图"),
            (147, "第七图"),
            (151, "1st Game"),
            (152, "2nd Game"),
            (153, "3rd Game"),
            (154, "4th Game"),
            (155, "5th Game"),
            (161, "1st end"),
            (162, "2nd end"),
            (163, "3rd end"),
            (164, "4th end"),
            (165, "5th end"),
            (166, "6th end"),
            (167, "7th end"),
            (168, "8th end"),
            (169, "9th end"),
            (170, "10th end"),
            (171, "Extra end"),
            (301, "第一节结束"),
            (302, "第二节结束"),
            (303, "第三节结束"),
            (304, "第四节结束"),
            (305, "第五图结束"),
            (306, "第六图结束"),
            (401, "1st inning top"),
            (402, "1st inning bottom"),
            (403, "2nd inning top"),
            (404, "2nd inning bottom"),
            (405, "3rd inning top"),
            (406, "3rd inning bottom"),
            (407, "4th inning top"),
            (408, "4th inning bottom"),
            (409, "5th inning top"),
            (410, "5th inning bottom"),
            (411, "6th inning top"),
            (412, "6th inning bottom"),
            (413, "7th inning top"),
            (414, "7th inning bottom"),
            (415, "8th inning top"),
            (416, "8th inning bottom"),
            (417, "9th inning top"),
            (418, "9th inning bottom"),
            (419, "Extra inning top"),
            (420, "Extra inning bottom"),
            (421, "Break top1bottom1"),
            (422, "Break top2bottom1"),
            (423, "Break top2bottom2"),
            (424, "Break top3bottom2"),
            (425, "Break top3bottom3"),
            (426, "Break top4bottom3"),
            (427, "Break top4bottom4"),
            (428, "Break top5bottom4"),
            (429, "Break top5bottom5"),
            (430, "Break top6bottom5"),
            (431, "Break top6bottom6"),
            (432, "Break top7bottom6"),
            (433, "Break top7bottom7"),
            (434, "Break top8bottom7"),
            (435, "Break top8bottom8"),
            (436, "Break top9bottom8"),
            (437, "Break top9bottom9"),
            (438, "Break topEIbottom9"),
            (439, "Break topEIbottomEI"),
            (440, "突然死亡法"),
            (441, "第六盘"),
            (442, "第七盘"),
            (443, "等待突然死亡"),
            (444, "突然死亡后"),
            (445, "打破"),
            (501, "第一局,主队"),
            (502, "第一局,客队"),
            (503, "第二局,主队"),
            (504, "第二局,客队"),
            (505, "Awaiting super over"),
            (506, "Super over, home team"),
            (507, "Super over, away team"),
            (508, "After super over"),
            (509, "局休"),
            (510, "Super over break"),
            (511, "午休"),
            (512, "茶歇"),
            (513, "柱"),
            (514, "8th set"),
            (515, "9th set"),
            (516, "10th set"),
            (517, "11th set"),
            (518, "12th set"),
            (519, "13th set"),
            (520, "Third innings, home team"),
            (521, "Third innings, away team"),
            (522, "Fourth innings, home team"),
            (523, "Fourth innings, away team"),
            (524, "Dinner break"),
            (525, "Drinks"),
            (526, "Super over"),
            (531, "1st inning"),
            (532, "2nd inning"),
            (533, "3rd inning"),
            (534, "4th inning"),
            (535, "5th inning"),
            (536, "6th inning"),
            (537, "7th inning"),
            (538, "8th inning"),
            (539, "9th inning")
    
)

MATCH_SOURCE=(
    (1,'Betradar'),
    (2,'188'),
    (3,'沙巴'),
    (4,'IM'),
)

OUT_MATCH_SOURCE = (
    (2,'188'),
    (3,'沙巴'),
    (4,'IM'),
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
    (4, '推广线下'),
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
    (109,'反恐精英'),
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
    (1,'异常注单'),
    (2,'已审核')
)

TERMINAL_TYPE = (
    (1,'iOS'),
    (2,'Android'),
    (3,'H5'),
    (4,'PC')
)
OPERATE_TYPE = (
    (1,'下注'),
    (2,'充值'),
    (3,'登录'),
    (4,'注册'),
)


ACTIVITY_RECORD_STATE=(
    (0,'正在进行'),
    (1,'已完成'),
    (2,'已发放'),
    (3,'已失效'),
)

ZERO_ONE_STATUS=(
    (0,'失效'),
    (1,'启用'),
)

TODOLIST_CATEGORY=(
    (0,'未知'),
    (1,'结算相关'),
    (2,'结算提醒'),
    (100,'资金流'),
)
TODOLIST_STATUS=(
    (0,'未处理'),
    (1,'已处理'),
)

GAMEMONEY_IN_STATUS=(
    (0,'等待转入'),
    (1,'正在转入'),
    (2,'转入完成'),
    (3,'转入失败'),
    (4,'转入失败,已退款'),
)

GAMEMONEY_OUT_STATUS = (
    (0,'等待处理'),
    (1,'正在收回'),
    (2,'收回完成'),
    (4,'收回失败'),
)

ACCOUNT_POWERTYPE = (
    (1,'体育类型'),
    (2,'AG游戏'),
    (3,'沙巴体育'),
    (4,'龙城棋牌'),
    (5,'IM体育/电竞'),
    (6,'RG电竞'),
    (7,'PT电子'),
    (8,'双赢彩票'),
    (9,'eBet真人'),
    (10,'VR彩票'),
    (11,'PP电子'),
    (12,'IM棋牌'),
)

#ODDSOURCE =(
    #(0,'--'),
    #(1,'Betradar'),
    #(2,'188'),
    #(3,'沙巴'),
#)

SETTLEMSG_STATUS=(
    (0,'编辑中'),
    (1,'审核中'),
)

MESSAGE_SENDWAY=(
    (0,'立即推送'),
    (1,'定时推送'),
)

MESSAGE_RECIVER_TYPE=(
    (0,'全部'),
    (1,'用户ID'),
    (2,'用户组ID'),
    (3,'会员组ID'),
)

VIPBONUS_STATUS = (
    (0,'待领取'),
    (1,'已领取'),
)

VALID_STATUS= (
    (0,'无效'),
    (1,'有效'),
)

IM_PRODUCTID=(
    (301,'IM体育'),
    (401,'IM电竞')
)

if getattr(settings,'OPEN_SECRET',False):
    ACTIVITY2_CATAGORY = (
        (1,'新人优惠'),
        (2,'体育电竞'),
        (3,'真人娱乐') ,
        (4,'电子游戏') ,
        (5,'其他优惠'),
        #全部，新人优惠，体育优惠, 真人优惠,彩票优惠，其他优惠
        # 1.公用 2.新人优惠 3.体育电竞 4.真人娱乐 5.电子游戏 6.其他优惠
    )
else:
    ACTIVITY2_CATAGORY = (
        (1,'新人优惠'),
        (2,'体育电竞'),
        (5,'其他优惠'),
        #全部，新人优惠，体育优惠, 真人优惠,彩票优惠，其他优惠
    )