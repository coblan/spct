from helpers.director.shortcut import page_dc, director
from .matches_statistics import MatchesStatisticsPage
from ..models import TbMatchesBasketball

class BasketballMatchesStatisticsPage(MatchesStatisticsPage):
    def get_label(self): 
        return '篮球赛事统计'
    
    class tableCls(MatchesStatisticsPage.tableCls):
        model = TbMatchesBasketball
        
        def get_statistic_sql(self, sql_args): 
            sql = r"exec dbo.SP_MatchesStatistics_Basketball %(TournamentID)s,%(MatchID)s,%%s,%(StatusCode)s,%(LiveBet)s,%%s,%(AccountID)s,'%(MatchDateFrom)s','%(MatchDateTo)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s'" \
                  % sql_args
            return sql       

director.update({
    'BasketballMatchesStatisticsPage': BasketballMatchesStatisticsPage.tableCls,
})

page_dc.update({
    'BasketballMatchesStatisticsPage': BasketballMatchesStatisticsPage,
})