# encoding:utf-8
from __future__ import unicode_literals
import re
from django.db import connections
from helpers.director.shortcut import ModelTable, TablePage, page_dc, RowSort, RowFilter
from helpers.director.table.row_search import SelectSearch
from ..models import TbMatches, MATCH_STATUS
from helpers.director.base_data import director
from django.utils import timezone


class MatchesStatisticsPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '赛事投注状况'

    class tableCls(ModelTable):
        model = TbMatches
        include = ['matchid']

        def dict_head(self, head):
            if head['name'] == 'StatusCode':
                head['options'] = [{'value': value, 'label': label} for (value, label) in MATCH_STATUS]
                head['editor'] = 'com-table-mapper'
            return head

        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')
            search_args['_start_matchdate'] = search_args.get('_start_matchdate') or def_start
            search_args['_end_matchdate'] = search_args.get('_end_matchdate') or def_end
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
            names = ['tournamentid', 'statuscode', 'livebet']

            def dict_head(self, head):
                if head['name'] == 'tournamentid':
                    head['editor'] = 'com-filter-search-select'
                    head['placeholder'] = '请选择联赛'
                    head['style'] = 'width:200px;'
                    head['order'] = True
                return head

        class sort(RowSort):
            names = ['MatchDate','TicketCount','SeriesTicketCount', 'UserCount', 'SumBetAmount', 'SumBetOutcome', 'SumGrossProfit', 'SumBonus',
                     'SumProfit']

        def get_rows(self):
            self.getData()
            for row in self.matches:
                row['matchid'] = row['MatchID']
                row['SumBetAmount'] = round(row['SumBetAmount'], 2)
                row['SumBetOutcome'] = round(row['SumBetOutcome'], 2)
                row['SumGrossProfit'] = round(row['SumGrossProfit'], 2)
                row['SumBonus'] = round(row['SumBonus'], 2)
                row['SumProfit'] = round(row['SumProfit'], 2)
            return self.matches

        def getData(self):
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
                'StatusCode': self.search_args.get('statuscode', -1),
                'LiveBet': int(self.search_args.get('livebet', -1)),
                'NickName': nickname,
                'AccountID': self.search_args.get('accountid', 0),
                'MatchDateFrom': self.search_args.get('_start_matchdate', ''),
                'MatchDateTo': self.search_args.get('_end_matchdate', ''),
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'Sort': sort,
            }

            sql = r"exec dbo.SP_MatchesStatistics %(TournamentID)s,%(MatchID)s,%(StatusCode)s,%(LiveBet)s,'%(NickName)s',%(AccountID)s,'%(MatchDateFrom)s','%(MatchDateTo)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s'" \
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
                cursor.nextset()
                for row in cursor:
                    dc = {}
                    for index, desp_item in enumerate(cursor.description):
                        head_name = desp_item[0]
                        dc[head_name] = round(row[index], 2)
                    self.footer_dc = dc

                self.footer = ['合计'] + self.footer_by_dict(self.footer_dc)[1:]

        def getExtraHead(self):
            return [
                {'name': 'TournamentName', 'label': '联赛 ', 'width': 150},
                # {'name': 'MatchID', 'label': 'MatchID', },
                {'name': 'Team1ZH', 'label': '主队', 'width': 150},
                {'name': 'Team2ZH', 'label': '客队', 'width': 150},
                {'name': 'MatchDate', 'label': '比赛日期', 'width': 140},
                {'name': 'MatchScore', 'label': '比分', 'width': 80},
                {'name': 'StatusCode', 'label': '状态', },
                {'name': 'LiveBet', 'label': '走地盘','editor':'com-table-bool-shower' },
                {'name': 'TicketCount', 'label': '单注注数', 'width': 80},
                {'name': 'SeriesTicketCount', 'label': '串关注数', 'width': 80},
                {'name': 'UserCount', 'label': '用户数', 'width': 80},
                {'name': 'SumBetAmount', 'label': '投注金额', 'width': 120},
                {'name': 'SumBetOutcome', 'label': '派奖金额', 'width': 120},
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

        def get_operation(self):
            return [
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]


director.update({
    'match.viewbymatch': MatchesStatisticsPage.tableCls
})

page_dc.update({
    'matches_statistics': MatchesStatisticsPage
})
