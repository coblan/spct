from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from ..ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from ..models import TbLcitymoneyoutinfo

class SportmoneyOutInfo(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbLcitymoneyoutinfo
        exclude =[]

director.update({
    'lcitymoneyout':SportmoneyOutInfo.tableCls,
    
})
page_dc.update({
    'lcitymoneyout':SportmoneyOutInfo
})