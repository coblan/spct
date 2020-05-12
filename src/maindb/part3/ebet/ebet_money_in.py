from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from maindb.ag.gamemoneyinfo import GameMoneyininfoPage
from maindb. models import TbEbmoneyininfo

class EbMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbEbmoneyininfo
        exclude =[]
    
        class filters(RowFilter):
            names=['status']
            range_fields=['ordertime']

director.update({
    'eb_moneyinfo':EbMoneyInPage.tableCls
})

page_dc.update({
    'eb_moneyinfo':EbMoneyInPage
})