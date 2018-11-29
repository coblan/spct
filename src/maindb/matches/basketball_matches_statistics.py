from helpers.director.shortcut import page_dc, director
from .matches_statistics import MatchesStatisticsPage, DetailStatistic, TickmasterTab, TicketMasterPage
from ..models import TbMatchesBasketball
class BasketballMatchesStatisticsPage(MatchesStatisticsPage):
    def get_label(self): 
        return '篮球赛事统计'
    
    @classmethod
    def get_tabs(cls, crt_user): 
        ls = [
           {'name': 'detailStatic',
            'label': '详细统计',
            'com': 'com-tab-table',
            'par_field': 'matchid',
            'table_ctx': BasketballDetailStatistic(crt_user=crt_user).get_head_context(),
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
        dc .update( TicketMasterPage.get_tabs() )
        return dc
    
    class tableCls(MatchesStatisticsPage.tableCls):
        model = TbMatchesBasketball
        
        def get_statistic_sql(self, sql_args): 
            sql = r"exec dbo.SP_MatchesStatistics_Basketball %(TournamentID)s,%(MatchID)s,%%s,%(StatusCode)s,%(LiveBet)s,%%s,%(AccountID)s,'%(MatchDateFrom)s','%(MatchDateTo)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s'" \
                  % sql_args
            return sql       

class BasketballDetailStatistic(DetailStatistic):
    sql_fun = 'SP_SingleMatchStatistics_Basketball'

director.update({
    'BasketballMatchesStatisticsPage': BasketballMatchesStatisticsPage.tableCls,
    'BasketballDetailStatistic': BasketballDetailStatistic,
})

page_dc.update({
    'BasketballMatchesStatisticsPage': BasketballMatchesStatisticsPage,
})