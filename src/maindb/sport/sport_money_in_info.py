from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from ..models import TbSportmoneyininfo

class SportMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbSportmoneyininfo
        exclude =[]

page_dc.update({
    'sportmoneyinfo':SportMoneyInPage
})