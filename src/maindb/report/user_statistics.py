# encoding:utf-8
from __future__ import unicode_literals
from django.db import connections
from helpers.director.shortcut import ModelTable, TablePage, page_dc, RowSort, RowFilter
from helpers.director.table.row_search import SelectSearch
from ..models import TbAccount
from helpers.director.base_data import director
from django.utils import timezone


class UserStatisticsPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '会员统计'

    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid']

        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')
            search_args['_start_date'] = search_args.get('_start_date') or def_start
            search_args['_end_date'] = search_args.get('_end_date') or def_end
            return search_args

        class search(SelectSearch):
            names = ['nickname']

            def get_option(self, name):
                if name == 'nickname':
                    return {'value': 'nickname', 'label': '用户昵称', }
                else:
                    return super().get_option(name)

        class filters(RowFilter):
            range_fields = ['date']

            def dict_head(self, head):
                if head['name'] == 'date':
                    head['label'] = '日期'
                return head

        class sort(RowSort):
            names = ['Amount', 'GameCoinRechargeAmount', 'CommissionRechargeAmount', 'ReservedAmount',
                     'CommissionWithDrawAmount', 'BetAmount', 'Turnover', 'BetOutcome', 'BetBonus', 'OrderCount',
                     'WinCount', 'WinRate', 'FirstRechargeBonus', 'SecondRechargeBonus', 'RescueBonus', 'BirthdayBonus',
                     'AdjustAmount', 'Profit']

        def get_rows(self):
            for row in self.matches:
                row['accountid'] = row['AccountID']
                row['Amount'] = round(row['Amount'], 2)
                row['BetAmount'] = round(row['BetAmount'], 2)
                row['Turnover'] = round(row['Turnover'], 2)
                row['BetOutcome'] = round(row['BetOutcome'], 2)
                row['BetBonus'] = round(row['BetBonus'], 2)
                row['FirstRechargeBonus'] = round(row['FirstRechargeBonus'], 2)
                row['SecondRechargeBonus'] = round(row['SecondRechargeBonus'], 2)
                row['RescueBonus'] = round(row['RescueBonus'], 2)
                row['BirthdayBonus'] = round(row['BirthdayBonus'], 2)
                row['AdjustAmount'] = round(row['AdjustAmount'], 2)
                row['Profit'] = round(row['Profit'], 2)
                row['GameCoinRechargeAmount'] = round(row['GameCoinRechargeAmount'], 2)
                row['CommissionRechargeAmount'] = round(row['CommissionRechargeAmount'], 2)
                row['ReservedAmount'] = round(row['ReservedAmount'], 2)
                row['CommissionWithDrawAmount'] = round(row['CommissionWithDrawAmount'], 2)
            return self.matches

        def __init__(self, *args, **kws):
            super().__init__(*args, **kws)
            nickname = ""
            if self.search_args.get('_qf') == 'nickname':
                nickname = self.search_args.get('_q', '')
            sort = self.search_args.get('_sort') or '-Profit'
            sortway = 'asc'
            if sort.startswith('-'):
                sort = sort[1:]
                sortway = 'desc'

            sort_dc = {
                'FirstRechargeBonus':'1stRCBonus',
                'SecondRechargeBonus':'2ndRCBonus',
                'RescueBonus':'Rescue',
                'BirthdayBonus':'BdBonus',
                'GameCoinRechargeAmount': 'GameRCAmt',
                'CommissionRechargeAmount':'CommRCAmt',
                'CommissionWithDrawAmount':'CommWDAmt',
                'ReservedAmount':'RvAmt',
                'AdjustAmount':'AdjAmount'
            }
            realsort = sort_dc.get(sort) or sort;

            sql_args = {
                'NickName': nickname,
                'AccountID': 0,
                'StartTime': self.search_args.get('_start_date', ''),
                'EndTime': self.search_args.get('_end_date', ''),
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'Sort': realsort,
                'SortWay': sortway
            }
            sql = r"exec dbo.SP_UserStatistics '%(NickName)s',%(AccountID)s,'%(StartTime)s','%(EndTime)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s','%(SortWay)s'" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                set0 = cursor.fetchall()
                self.total = set0[0][0]

                footer = {}
                for col_data, col in zip(set0[0], cursor.description):
                    head_name = col[0]
                    if head_name.startswith('Sum'):
                        head_name = head_name[3:]
                    footer[head_name] = round(col_data, 2)
                self.footer = ['合计'] + self.footer_by_dict(footer)

                cursor.nextset()
                self.matches = []
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    self.matches.append(dc)

        def getExtraHead(self):
            return [
                {'name': 'NickName', 'label': '昵称 ', 'width': 150},
                {'name': 'Amount', 'label': '余额', 'width': 130},
                {'name': 'GameCoinRechargeAmount', 'label': '充值金额', 'width': 130},
                {'name': 'CommissionRechargeAmount', 'label': '佣金充值金额', 'width': 130},
                {'name': 'ReservedAmount', 'label': '提现金额', 'width': 130},
                {'name': 'CommissionWithDrawAmount', 'label': '佣金提现金额', 'width': 130},
                {'name': 'BetAmount', 'label': '投注金额', 'width': 130},
                {'name': 'Turnover', 'label': '流水', 'width': 100},
                {'name': 'BetOutcome', 'label': '派奖金额', 'width': 100},
                {'name': 'BetBonus', 'label': '返水', 'width': 100},
                {'name': 'OrderCount', 'label': '注数', 'width': 100},
                {'name': 'WinCount', 'label': '中注数', 'width': 100},
                {'name': 'WinRate', 'label': '中注比', 'width': 100},
                {'name': 'FirstRechargeBonus', 'label': '首存红利', 'width': 100},
                {'name': 'SecondRechargeBonus', 'label': '再存红利', 'width': 100},
                {'name': 'RescueBonus', 'label': '救援金', 'width': 100},
                {'name': 'BirthdayBonus', 'label': '生日礼金', 'width': 100},
                {'name': 'AdjustAmount', 'label': '调账', 'width': 100},
                {'name': 'Profit', 'label': '亏盈', 'width': 100}
            ]

        def getRowPages(self):
            return {
                'crt_page': self.search_args.get('_page', 1),
                'total': self.total,
                'perpage': self.search_args.get('_perpage', 20)
            }


director.update({
    'UserStatisticsPage': UserStatisticsPage.tableCls
})

page_dc.update({
    'UserStatisticsPage': UserStatisticsPage
})
