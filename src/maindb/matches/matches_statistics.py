# encoding:utf-8
from __future__ import unicode_literals
import re
from django.db import connections
from helpers.director.shortcut import ModelTable, TablePage, page_dc, RowSort, RowFilter
from helpers.director.table.row_search import SelectSearch
from ..models import TbMatch, NEW_MATCH_STATUS,TbTicketmaster,TbTournament
from helpers.director.base_data import director
from django.utils import timezone
from helpers.director.table.table import PlainTable
from .ticket_master import TicketMasterPage,TicketMasterForm
from helpers.director.engine import BaseEngine, page, fa, can_list, can_touch

class MatchesStatisticsPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '赛事投注状况'

    class tableCls(ModelTable):
        model = TbMatch
        include = ['matchid', 'livebet', 'statuscode', 'matchdate', 'tournamentid']
        hide_fields = ['livebet', 'statuscode', 'matchdate', 'tournamentid']

        def dict_head(self, head):
            if head['name'] == 'StatusCode':
                head['options'] = [{'value': value, 'label': label} for (value, label) in NEW_MATCH_STATUS]
                head['editor'] = 'com-table-mapper'
            if head['name'] == 'matchid':
                if can_touch (TbTicketmaster,self.crt_user):
                    head['editor'] = 'com-table-switch-to-tab'
                    head['tab_name'] = 'detailStatic'
                    head['ctx_name'] = 'match_statistic'
            return head

        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today #- sp
            def_start = last.strftime('%Y-%m-%d') + ' 00:00:00'
            def_end = today.strftime('%Y-%m-%d') + ' 23:59:59'
            search_args['_start_matchdate'] = search_args.get('_start_matchdate') or def_start
            search_args['_end_matchdate'] = search_args.get('_end_matchdate') or def_end
            return search_args

        class search(SelectSearch):
            names = ['teamzh', 'nickname']
            exact_names = ['matchid']

            def get_option(self, name):
                if name == 'nickname':
                    return {'value': 'nickname', 'label': '用户昵称', }
                elif name == 'teamzh':
                    return {'value': 'teamzh', 'label': '球队名称', }
                else:
                    return super().get_option(name)

        class filters(RowFilter):
            range_fields = ['matchdate']
            names = ['tournamentid', 'statuscode', 'livebet']

            def dict_head(self, head):
                if head['name'] == 'tournamentid':
                    #head['editor'] = 'com-filter-search-select'
                    head['editor'] = 'com-filter-single-select2'
                    head['placeholder'] = '请选择联赛'
                    head['style'] = 'width:200px;'
                    head['options']=[
                        {'value':x.tournamentid,'label':str(x)} for x in TbTournament.objects.filter(sportid=1)
                        #{'value':x.tournamentid,'label':str(x)} for x in TbTournament.objects.extra(
                            #where=["TB_SportTypes.source= TB_Tournament.source","TB_SportTypes.SportID=0"],
                            #tables=['TB_SportTypes'])
                    ]                    
                    #head['order'] = True
                    
                return head

        class sort(RowSort):
            names = ['MatchDate', 'TicketCount', 'SeriesTicketCount', 'UserCount', 'SumBetAmount', 'SumBetOutcome',
                     'SumGrossProfit', 'SumBonus',
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

        def get_statistic_sql(self, sql_args): 
            sql = r"exec dbo.SP_MatchesStatistics %(TournamentID)s,%(MatchID)s,%%s,%(StatusCode)s,%(LiveBet)s,%%s,%(AccountID)s,'%(MatchDateFrom)s','%(MatchDateTo)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s'" \
                  % sql_args
            return sql
        
        def getData(self):
            nickname = ""
            matchid = 0
            teamzh = ''
            if self.search_args.get('_qf') == 'nickname':
                nickname = self.search_args.get('_q', '')
            elif self.search_args.get('_qf') == 'matchid':
                matchid = self.search_args.get('_q', 0) or 0
            elif self.search_args.get('_qf') == 'teamzh':
                teamzh = self.search_args.get('_q', '')
            if not re.search('^\d*$', str(matchid)):
                matchid = -1
            sort = self.search_args.get('_sort') or '-MatchDate'
            if sort.startswith('-'):
                sort = sort[1:] + ' desc'

            sql_args = {
                'TournamentID': self.search_args.get('tournamentid', 0),
                'MatchID': matchid,
                'TeamZH': teamzh,
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
            sql = self.get_statistic_sql(sql_args)
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql, [teamzh, nickname ])
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

                self.footer = ['合计'] + self.footer_by_dict(self.footer_dc)[0:]

        def getExtraHead(self):
            return [
                {'name': 'TournamentName', 'label': '联赛 ', 'width': 150},
                # {'name': 'MatchID', 'label': 'MatchID', },
                {'name': 'Team1ZH', 'label': '主队', 'width': 150},
                {'name': 'Team2ZH', 'label': '客队', 'width': 150},
                {'name': 'MatchDate', 'label': '比赛日期', 'width': 140},
                {'name': 'MatchScore', 'label': '比分', 'width': 80},
                {'name': 'StatusCode', 'label': '状态', },
                {'name': 'LiveBet', 'label': '走地盘', 'editor': 'com-table-bool-shower'},
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
    def get_context(self): 
        ctx = super().get_context()
        #ls = [
           #{'name': 'detailStatic',
            #'label': '详细统计',
            #'com': 'com_tab_table',
            #'par_field': 'matchid',
            #'table_ctx': DetailStatistic(crt_user=self.crt_user).get_head_context(),
            #'visible': True,
            #},
           #{'name': 'ticket_master',
            #'label': '注单', 
            #'com': 'com_tab_table',
            #'par_field': 'matchid',
            #'table_ctx': TickmasterTab(crt_user=self.crt_user).get_head_context(),
            #'visible': True, }        
        #]
        ##ctx['tabs'] = ls
        
        #ctx['named_tabs'] = {
            #'match_statistic': ls,
        #}
        #ctx['named_tabs'] .update( TicketMasterPage.get_tabs() )
        
        ctx['named_ctx'] = self.get_tabs(self.crt_user)
        

        return ctx
    
    @classmethod
    def get_tabs(cls, crt_user): 
        ls = [
           {'name': 'detailStatic',
            'label': '详细统计',
            'com': 'com-tab-table',
            'par_field': 'matchid',
            'table_ctx': DetailStatistic(crt_user=crt_user).get_head_context(),
            'visible': True,
            },
           {'name': 'ticket_master',
            'label': '注单', 
            'com': 'com-tab-table',
            'par_field': 'matchid',
            'table_ctx': TickmasterTab(crt_user=crt_user).get_head_context(),
            'visible': True, }        
        ]
        
        dc = {
            'match_statistic': ls,
        }
        dc .update( TicketMasterPage.get_named_ctx() )
        return dc
    


class DetailStatistic(PlainTable):
    sql_fun = 'SP_SingleMatchStatistics'

    def get_head_context(self): 
        ctx = super().get_head_context()
        ctx.update({
            'selectable': False,
        })
        return ctx
    
    def get_heads(self): 
        return [
            {'name': 'MarketID','label': '玩法ID',}, 
            {'name': 'MarketName','label': '玩法','width': 150,}, 
            {'name': 'SpecialBetValue','label': '盘口',}, 
            {'name': 'OutcomeName','label': '投注项' },
            {'name': 'BetAmout','label': '投注金额','editor': 'com-table-digit-shower','digit': 2,  }
        ]

    
    def get_rows(self): 
        #exec [dbo].[SP_SingleMatchStatistics] 97856,0,1 
        sql_args = {
            'sql_fun': self.sql_fun,
            'matchid': self.kw.get('matchid'),
            'half_or_full': self.search_args.get('half_or_full', 'null'),
            'oddkind': self.search_args.get('oddkind', 'null'),
        }    
        sql = r"exec dbo.%(sql_fun)s %(matchid)s" % sql_args   
        
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
            rows = []
            for row in cursor:
                dc = {}
                for index, head in enumerate(cursor.description):
                    dc[head[0]] = row[index]
                rows.append(dc) 

        return rows
    


    
class TickmasterTab(TicketMasterPage.tableCls):
    
    def inn_filter(self, query): 
        query = super().inn_filter(query)
        return query.filter(tbticketstake__matchid = int(self.kw.get('matchid')) )
    
    @classmethod
    def get_director_name(cls):
        return 'match_statistic.ticket_master'

director.update({
    'match.viewbymatch': MatchesStatisticsPage.tableCls, 
    'DetailStatistic': DetailStatistic,
    'match_statistic.ticket_master': TickmasterTab,
    'match_statistic.ticket_master.edit': TicketMasterForm,
})

page_dc.update({
    'matches_statistics': MatchesStatisticsPage
})
