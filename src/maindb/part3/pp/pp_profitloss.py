from maindb.part3.ebet.ebet_profitloss import EbProfitlossPage
from helpers.director.shortcut import page_dc,director
from maindb.models import TbPpprofitloss

class PPProfitlossPage(EbProfitlossPage):
    class tableCls(EbProfitlossPage.tableCls):
        model = TbPpprofitloss


director.update({
    'pp_profitloss':PPProfitlossPage.tableCls,
})

page_dc.update({
    'pp_profitloss':PPProfitlossPage
})