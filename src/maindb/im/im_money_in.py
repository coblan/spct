from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from ..models import TbImmoneyininfo

class IMMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbImmoneyininfo
        exclude =[]
    
        class filters(RowFilter):
            names=['status','productid']
            range_fields=['ordertime']

director.update({
    'immoneyinfo':IMMoneyInPage.tableCls
})

page_dc.update({
    'immoneyinfo':IMMoneyInPage
})