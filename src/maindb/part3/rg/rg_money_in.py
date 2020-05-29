from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from maindb.models import TbRgmoneyininfo

class RGMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbRgmoneyininfo
        exclude =[]
    
        class filters(RowFilter):
            names=['status']
            range_fields=['ordertime']

director.update({
    'rg_moneyinfo':RGMoneyInPage.tableCls
})

page_dc.update({
    'rg_moneyinfo':RGMoneyInPage
})