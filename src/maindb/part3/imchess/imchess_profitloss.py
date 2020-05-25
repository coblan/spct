from maindb.part3.ebet.ebet_profitloss import EbProfitlossPage
from helpers.director.shortcut import page_dc,director
from maindb.models import TBIMChessProfitLoss

class ImChessProfitlossPage(EbProfitlossPage):
    class tableCls(EbProfitlossPage.tableCls):
        model = TBIMChessProfitLoss


director.update({
    'imchess_profitloss':ImChessProfitlossPage.tableCls,
})

page_dc.update({
    'imchess_profitloss':ImChessProfitlossPage
})