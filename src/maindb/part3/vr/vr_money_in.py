from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from maindb.ag.gamemoneyinfo import GameMoneyininfoPage
from maindb. models import TBVRMoneyInInfo

class VRMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TBVRMoneyInInfo
        exclude =[]
    
        class filters(RowFilter):
            names=['status']
            range_fields=['ordertime']

director.update({
    'vr_moneyinfo':VRMoneyInPage.tableCls
})

page_dc.update({
    'vr_moneyinfo':VRMoneyInPage
})