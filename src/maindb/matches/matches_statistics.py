# encoding:utf-8
from __future__ import unicode_literals

from django.db import connections
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable, TablePage, page_dc, RowSort, RowFilter, RowSearch
from helpers.director.table.row_search import SelectSearch
from ..models import TbMatches
from django.db.models.aggregates import Count, Sum
from django.db.models import F, Q
from helpers.director.base_data import director


class MatchesStatisticsPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '赛事投注状况'

    class tableCls(ModelTable):
        model = TbMatches
        include = ['matchid']

        def get_rows(self):
            for row in self.matches:
                row['matchid'] = row['MatchID']
            return self.matches

        def __init__(self, *args, **kws):
            super().__init__(*args, **kws)
            sql_args = {
                'TournamentID': self.search_args.get('TournamentID', 0),
                'MatchID': self.search_args.get('Matchid', 0),
                'NickName': self.search_args.get('NickName', ''),
                'MatchDateFrom': self.search_args.get('MatchDateFrom', '2018-08-01'),
                'MatchDateTo': self.search_args.get('MatchDateTo', '2018-08-31'),
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'Sort': self.search_args.get('_sort', ''),
                'Total': self.search_args.get('_sort', '')
            }

            sql = "exec dbo.SP_MatchesStatistics %(TournamentID)s,%(MatchID)s,'%(NickName)s','%(MatchDateFrom)s','%(MatchDateTo)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s'" \
                  % sql_args

            cursor = connections['Sports'].cursor()
            cursor.execute(sql)
            self.total = cursor.fetchall()[0][0]
            cursor.nextset()
            self.matches=[]
            for row in cursor:
                dc = {}
                for index, head in enumerate(cursor.description):
                    dc[head[0]] = row[index]
                self.matches.append(dc)




        def getExtraHead(self):
            return [
                {'name': 'TournamentName', 'label': 'TournamentName', },
                # {'name': 'MatchID', 'label': 'MatchID', },
                {'name': 'Team1ZH', 'label': 'Team1ZH', },
                {'name': 'Team2ZH', 'label': 'Team2ZH', },
                {'name': 'MatchDate', 'label': 'MatchDate', },
                {'name': 'MatchScore', 'label': 'MatchScore', },
                {'name': 'StatusCode', 'label': 'StatusCode', },
                {'name': 'TicketCount', 'label': 'TicketCount', },
                {'name': 'UserCount', 'label': 'UserCount', },
                {'name': 'SumBetAmount', 'label': 'SumBetAmount', },
                {'name': 'SumBetOutcome', 'label': 'SumBetOutcome', },
                {'name': 'SumGrossProfit', 'label': 'SumGrossProfit', },
                {'name': 'SumBonus', 'label': 'SumBonus', },
                {'name': 'SumProfit', 'label': 'SumProfit', },
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
