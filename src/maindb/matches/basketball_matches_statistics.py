from helpers.director.shortcut import page_dc, director
from .matches_statistics import MatchesStatisticsPage, DetailStatistic, TickmasterTab, TicketMasterPage
from ..models import TbMatch
#from ..status_code import BASKETBALL_MATCH_STAsTUS

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
        sportid=2
    
class BasketballDetailStatistic(DetailStatistic):
    sql_fun = 'SP_SingleMatchStatistics'

director.update({
    'BasketballMatchesStatisticsPage': BasketballMatchesStatisticsPage.tableCls,
    'BasketballDetailStatistic': BasketballDetailStatistic,
})

page_dc.update({
    'BasketballMatchesStatisticsPage': BasketballMatchesStatisticsPage,
})