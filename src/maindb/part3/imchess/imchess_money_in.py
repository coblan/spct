from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from maindb.ag.gamemoneyinfo import GameMoneyininfoPage
from maindb. models import TBIMChessMoneyInInfo

class IMchessMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TBIMChessMoneyInInfo
        exclude =[]
    
        class filters(RowFilter):
            names=['status']
            range_fields=['ordertime']

director.update({
    'imchess_moneyinfo':IMchessMoneyInPage.tableCls
})

page_dc.update({
    'imchess_moneyinfo':IMchessMoneyInPage
})