from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from ..models import TbImmoneyoutinfo

class IMmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbImmoneyoutinfo
        exclude =[]
        
        class filters(RowFilter):
            names=['status','productid']
            range_fields=['ordertime']

director.update({
    'immoneyout':IMmoneyOutInfoPage.tableCls,
    
})
page_dc.update({
    'immoneyout':IMmoneyOutInfoPage
})