# encoding:utf-8
from __future__ import unicode_literals
from django.db import connections
from helpers.director.shortcut import TablePage, page_dc, SimTable, FieldsPage, Fields
from helpers.director.base_data import director
from django.utils import timezone


class PlatformProfitFieldsPage(FieldsPage):
    template = 'jb_admin/fields.html'

    class fieldsCls(Fields):
        def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw):
            sql_args = {
                'StartTime': self.search_args.get('_start_date', ''),
                'EndTime': self.search_args.get('_end_date', '')
            }
            sql = r"exec dbo.[SP_PlatformProfit] '%(StartTime)s','%(EndTime)s'" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                self.row = {}
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    self.row = dc

        def get_heads(self):
            heads = [
                {'name': 'BetAmount', 'label': '投注金额 ', 'width': 150},
                {'name': 'Turnover', 'label': '流水', 'width': 130},
                {'name': 'BetBonus', 'label': '返水', 'width': 130},
                {'name': 'BetOutCome', 'label': '派奖金额', 'width': 130},
                {'name': 'RechargeBonus', 'label': '充值红利', 'width': 130},
                {'name': 'BirthdayBonus', 'label': '生日礼金', 'width': 130},
                {'name': 'RescueBonus', 'label': '救援金', 'width': 130},
                {'name': 'AdjustAmount', 'label': '调账', 'width': 100},
                {'name': 'Profit', 'label': '亏盈', 'width': 100}
            ]
            for head in heads:
                head['editor'] = 'linetext'
                head['readonly'] = True
            return heads

        def get_row(self):
            row = self.row
            row['BetAmount'] = row['BetAmount']
            row['Turnover'] = round(row['Turnover'], 2)
            row['BetBonus'] = round(row['BetBonus'], 2)
            row['BetOutCome'] = round(row['BetOutCome'], 2)
            row['RechargeBonus'] = round(row['RechargeBonus'], 2)
            row['BirthdayBonus'] = round(row['BirthdayBonus'], 2)
            row['RescueBonus'] = round(row['RescueBonus'], 2)
            row['AdjustAmount'] = round(row['AdjustAmount'], 2)
            row['Profit'] = round(row['Profit'], 2)
            return row


class PlatformProfit(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '平台亏盈'

    class tableCls(SimTable):
        fields_sort = ['Profit', 'BetAmount', 'Turnover', 'BetBonus', 'BetOutCome', 'RechargeBonus', 'BirthdayBonus',
                       'RescueBonus', 'AdjustAmount']

        def getRowFilters(self):
            return [{'name': 'date', 'label': '日期', 'editor': 'com-date-datetimefield-range-filter'}]

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

        def get_rows(self):
            self.getData()
            for row in self.data:
                row['BetAmount'] = round(row['BetAmount'], 2)
                row['Turnover'] = round(row['Turnover'], 2)
                row['BetBonus'] = round(row['BetBonus'], 2)
                row['BetOutCome'] = round(row['BetOutCome'], 2)
                row['RechargeBonus'] = round(row['RechargeBonus'], 2)
                row['BirthdayBonus'] = round(row['BirthdayBonus'], 2)
                row['RescueBonus'] = round(row['RescueBonus'], 2)
                row['AdjustAmount'] = round(row['AdjustAmount'], 2)
                row['Profit'] = round(row['Profit'], 2)
            return self.data

        def getData(self):
            sql_args = {
                'StartTime': self.search_args.get('_start_date', ''),
                'EndTime': self.search_args.get('_end_date', '')
            }
            sql = r"exec dbo.[SP_PlatformProfit] '%(StartTime)s','%(EndTime)s'" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                # cursor.fetchall()
                self.data = []
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    self.data.append(dc)
                self.total = 1

        def get_heads(self):
            return [
                {'name': 'BetAmount', 'label': '投注金额 ', 'width': 150},
                {'name': 'Turnover', 'label': '流水', 'width': 130},
                {'name': 'BetBonus', 'label': '返水', 'width': 130},
                {'name': 'BetOutCome', 'label': '派奖金额', 'width': 130},
                {'name': 'RechargeBonus', 'label': '充值红利', 'width': 130},
                {'name': 'BirthdayBonus', 'label': '生日礼金', 'width': 130},
                {'name': 'RescueBonus', 'label': '救援金', 'width': 130},
                {'name': 'AdjustAmount', 'label': '调账', 'width': 100},
                {'name': 'Profit', 'label': '亏盈', 'width': 100}
            ]

        def getRowPages(self):
            return {
                'crt_page': self.search_args.get('_page', 1),
                'total': self.total,
                'perpage': self.search_args.get('_perpage', 20)
            }

        def get_operation(self):
            return [
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]


director.update({
    'platform_profit': PlatformProfit.tableCls
})

page_dc.update({
    'platform_profit': PlatformProfit
})
