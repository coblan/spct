from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from ..models import TbRgmoneyoutinfo

class RGmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbRgmoneyoutinfo
        exclude =[]
        
        class filters(RowFilter):
            names=['status']
            range_fields=['ordertime']

director.update({
    'rg_moneyout':RGmoneyOutInfoPage.tableCls,
    
})
page_dc.update({
    'rg_moneyout':RGmoneyOutInfoPage
})