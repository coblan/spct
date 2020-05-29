from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from maindb.models import TbLcitymoneyininfo

class SportMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbLcitymoneyininfo
        exclude =[]

director.update({
    'lcitymoneyinfo':SportMoneyInPage.tableCls
})

page_dc.update({
    'lcitymoneyinfo':SportMoneyInPage
})