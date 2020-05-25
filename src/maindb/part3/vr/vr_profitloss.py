from maindb.part3.ebet.ebet_profitloss import EbProfitlossPage
from helpers.director.shortcut import page_dc,director
from maindb.models import TBVRProfitLoss

class VRProfitlossPage(EbProfitlossPage):
    class tableCls(EbProfitlossPage.tableCls):
        model = TBVRProfitLoss


director.update({
    'vr_profitloss':VRProfitlossPage.tableCls,
})

page_dc.update({
    'vr_profitloss':VRProfitlossPage
})