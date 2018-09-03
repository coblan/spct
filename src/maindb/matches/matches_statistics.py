# encoding:utf-8
from __future__ import unicode_literals

import re

from django.db import connections
from django.db.models import Q

from helpers.director.shortcut import ModelTable, TablePage, page_dc, RowSort, RowFilter
from helpers.director.table.row_search import SelectSearch
from ..models import TbMatches
from helpers.director.base_data import director
from django.utils import timezone


class MatchesStatisticsPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '赛事投注状况'

    class tableCls(ModelTable):
        model = TbMatches
        include = ['matchid']

        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')
            search_args['_start_matchdate'] = search_args.get('_start_matchdate', def_start)
            search_args['_end_matchdate'] = search_args.get('_end_matchdate', def_end)
            return search_args

        class search(SelectSearch):
            names = ['nickname']
            exact_names = ['matchid']

            def get_option(self, name):
                if name == 'nickname':
                    return {'value': 'nickname', 'label': '用户昵称', }
                else:
                    return super().get_option(name)

        class filters(RowFilter):
            range_fields = ['matchdate']
            names = ['tournamentid']

            def dict_head(self, head):
                if head['name'] == 'tournamentid':
                    head['editor'] = 'com-filter-search-select'
                    head['placeholder'] = '请选择联赛'
                    head['style'] = 'width:200px;'
                    head['order'] = True
                return head

        class sort(RowSort):
            names = ['TicketCount', 'UserCount', 'SumBetAmount', 'SumBetOutcome', 'SumGrossProfit', 'SumBonus',
                     'SumProfit']

        def get_rows(self):
            for row in self.matches:
                row['matchid'] = row['MatchID']
            return self.matches

        def __init__(self, *args, **kws):
            super().__init__(*args, **kws)
            nickname = ""
            matchid = 0
            if self.search_args.get('_qf') == 'nickname':
                nickname = self.search_args.get('_q', '')
            elif self.search_args.get('_qf') == 'matchid':
                matchid = self.search_args.get('_q', 0) or 0
            if not re.search('^\d*$', str(matchid)):
                matchid = -1
            sort = self.search_args.get('_sort') or '-MatchDate'
            if sort.startswith('-'):
                sort = sort[1:] + ' desc'

            sql_args = {
                'TournamentID': self.search_args.get('tournamentid', 0),
                'MatchID': matchid,
                'NickName': nickname,
                'MatchDateFrom': self.search_args.get('_start_matchdate', ''),
                'MatchDateTo': self.search_args.get('_end_matchdate', ''),
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'Sort': sort,
            }

            sql = r"exec dbo.SP_MatchesStatistics %(TournamentID)s,%(MatchID)s,'%(NickName)s','%(MatchDateFrom)s','%(MatchDateTo)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s'" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                self.total = cursor.fetchall()[0][0]
                cursor.nextset()
                self.matches = []
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    self.matches.append(dc)

        def getExtraHead(self):
            return [
                {'name': 'TournamentName', 'label': '联赛 ', 'width': 150},
                # {'name': 'MatchID', 'label': 'MatchID', },
                {'name': 'Team1ZH', 'label': '主队', 'width': 150},
                {'name': 'Team2ZH', 'label': '客队', 'width': 150},
                {'name': 'MatchDate', 'label': '比赛日期', 'width': 140},
                {'name': 'MatchScore', 'label': '比分', 'width': 80},
                {'name': 'StatusCode', 'label': '状态', },
                {'name': 'TicketCount', 'label': '注数', 'width': 80},
                {'name': 'UserCount', 'label': '用户数', 'width': 80},
                {'name': 'SumBetAmount', 'label': '投注金额', 'width': 100},
                {'name': 'SumBetOutcome', 'label': '派奖金额', 'width': 100},
                {'name': 'SumGrossProfit', 'label': '毛利', 'width': 100},
                {'name': 'SumBonus', 'label': '返水', 'width': 100},
                {'name': 'SumProfit', 'label': '亏盈', 'width': 100},
            ]

        def getRowPages(self):
            return {
                'crt_page': self.search_args.get('_page', 1),
                'total': self.total,
                'perpage': self.search_args.get('_perpage', 20)
            }


director.update({
    'match.viewbymatch': MatchesStatisticsPage.tableCls
})

page_dc.update({
    'maindb.MatchesStatisticsPage': MatchesStatisticsPage
})
