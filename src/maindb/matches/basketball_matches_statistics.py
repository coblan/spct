from helpers.director.shortcut import page_dc, director
from .matches_statistics import MatchesStatisticsPage, DetailStatistic, TickmasterTab, TicketMasterPage
from ..models import TbMatchesBasketball
from ..status_code import BASKETBALL_MATCH_STATUS

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
        dc .update( TicketMasterPage.get_named_ctx() )
        return dc
    
    class tableCls(MatchesStatisticsPage.tableCls):
        model = TbMatchesBasketball
        
        def get_statistic_sql(self, sql_args): 
            sql = r"exec dbo.SP_MatchesStatistics_Basketball %(TournamentID)s,%(MatchID)s,%%s,%(StatusCode)s,%(LiveBet)s,%%s,%(AccountID)s,'%(MatchDateFrom)s','%(MatchDateTo)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s'" \
                  % sql_args
            return sql  
        
        def dict_head(self, head):
            head = super().dict_head(head)
            if head['name'] == 'StatusCode':
                head['options'] = [{'value': value, 'label': label} for (value, label) in BASKETBALL_MATCH_STATUS]
                head['editor'] = 'com-table-mapper'
            return head        

class BasketballDetailStatistic(DetailStatistic):
    sql_fun = 'SP_SingleMatchStatistics_Basketball'

director.update({
    'BasketballMatchesStatisticsPage': BasketballMatchesStatisticsPage.tableCls,
    'BasketballDetailStatistic': BasketballDetailStatistic,
})

page_dc.update({
    'BasketballMatchesStatisticsPage': BasketballMatchesStatisticsPage,
})