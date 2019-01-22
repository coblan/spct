from helpers.director.shortcut import page_dc, director, field_map
from ..models import TbTournamentBasketball
from . league import League, LeagueForm
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.model_func.field_procs.dotStrArray import DotStrArrayProc

class BasekballLeague(League):
    def get_label(self): 
        return '篮球联赛资料'
    
    class tableCls(League.tableCls):
        model = TbTournamentBasketball
        def inn_filter(self, query):
            return query.extra(
                where=["TB_SportTypes.source= TB_Tournament_Basketball.source","TB_SportTypes.SportID=1"],
                tables=['TB_SportTypes']                
            )        

class BasketballForm(LeagueForm):
    class Meta:
        model = TbTournamentBasketball
        exclude = ['categoryid', 'uniquetournamentid', 'createtime', 'specialcategoryid']


field_map.update({
    'maindb.tbtournamentbasketball.issubscribe': IntBoolProc,
    'maindb.tbtournamentbasketball.closelivebet': IntBoolProc,
    'maindb.tbtournamentbasketball.typegroupswitch': DotStrArrayProc,
})

director.update({
    'basketball_league': BasekballLeague.tableCls,
    'basketball_league.edit': BasketballForm,
})

page_dc.update({
    'basketball_league': BasekballLeague,
})