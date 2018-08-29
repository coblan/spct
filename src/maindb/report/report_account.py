# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowSort, RowFilter
from ..models import TbTicketmaster, TbAccount
from django.db.models.aggregates import Count, Sum
from django.db.models import F, ExpressionWrapper, FloatField
import decimal
from django.utils import timezone


class ReportAccout(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '账号统计'

    class tableCls(ModelTable):
        model = TbTicketmaster
        exclude = []

        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')
            search_args['_start_createtime'] = search_args.get('_start_createtime', def_start)
            search_args['_end_createtime'] = search_args.get('_end_createtime', def_end)
            return search_args

        def get_heads(self):
            heads = [
                {'name': 'accountid__nickname', 'label': '昵称', 'width': 120},
                {'name': 'accountid__amount', 'label': '余额', 'width': 100},
                {'name': 'num_ticket', 'label': '投注数', 'width': 60},
                {'name': 'num_win', 'label': '中注数', 'width': 80},
                {'name': 'ratio', 'label': '中注比', 'width': 100},
                {'name': 'sum_money', 'label': '投注金额', 'width': 120},
                {'name': 'sum_outcome', 'label': '派彩金额', 'width': 120},
                {'name': 'sum_bonus', 'label': '返水', 'width': 100},
                {'name': 'sum_turnover', 'label': '流水', 'width': 100},
                {'name': 'profit', 'label': '平台亏盈', 'width': 120},
            ]
            return heads

        def statistics(self, query):  # tbwithdrawlimit
            ss = query.defer("ticketid").values('accountid', 'accountid__nickname', 'accountid__amount') \
                .distinct() \
                .annotate(num_ticket=Count('ticketid'), num_win=Sum('winbet'),
                          sum_money=Sum('betamount'), sum_outcome=Sum('betoutcome'),
                          sum_bonus=Sum('bonus'), sum_turnover=Sum('turnover')) \
                .annotate(profit=F('sum_money') - F('sum_outcome'),
                          ratio=ExpressionWrapper(F('num_win') * 1.0 / F('num_ticket'),
                                                  output_field=FloatField())) \
                .order_by('accountid__nickname')
            return ss

        def get_rows(self):
            rows = ModelTable.get_rows(self)
            for row in rows:
                for k, v in row.items():
                    if isinstance(v, decimal.Decimal):
                        row[k] = str(v)
                    elif k == 'ratio':
                        row[k] = round(v * 100, 2)
            return rows

        def permited_fields(self):
            fields = ModelTable.permited_fields(self)
            fields.extend(['ratio', 'profit'])
            return fields

        class filters(RowFilter):
            range_fields = ['createtime']

        class sort(RowSort):
            names = ['ratio', 'profit']


director.update({
    'maindb.report.account': ReportAccout.tableCls
})

page_dc.update({
    'maindb.report.account': ReportAccout
})
