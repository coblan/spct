from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from maindb.models import TbPtmoneyininfo

class PTMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbPtmoneyininfo
        exclude =[]
    
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

director.update({
    'pt_moneyinfo':PTMoneyInPage.tableCls
})

page_dc.update({
    'pt_moneyinfo':PTMoneyInPage
})