from helpers.director.shortcut import page_dc, director
from .matches import MatchsPage, MatchForm
from ..models import TbMatchesBasketball

class BasketMatchsPage(MatchsPage):
    class tableCls(MatchsPage.tableCls):
        model = TbMatchesBasketball


class BasketMatchForm(MatchForm):
    model = TbMatchesBasketball

director.update({
    'basketball_matchs': BasketMatchsPage.tableCls,
    'basketball_matchs.edit': BasketMatchForm,
})

page_dc.update({
    'basketball_matchs':BasketMatchsPage ,
})
