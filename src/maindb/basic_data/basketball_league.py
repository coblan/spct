from helpers.director.shortcut import page_dc, director
from ..models import TbTournamentBasketball
from . league import League, LeagueForm

class BasekballLeague(League):
    def get_label(self): 
        return '篮球联赛资料'
    
    class tableCls(League.tableCls):
        model = TbTournamentBasketball

class BasketballForm(LeagueForm):
    class Meta:
        model = TbTournamentBasketball
        exclude = ['categoryid', 'uniquetournamentid', 'createtime']
    
director.update({
    'basketball_league': BasekballLeague.tableCls,
    'basketball_league.edit': BasketballForm,
})

page_dc.update({
    'basketball_league': BasekballLeague,
})