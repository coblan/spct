from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from maindb. ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb. models import TbEbmoneyoutinfo

class EbmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbEbmoneyoutinfo
        exclude =[]
        
        class filters(RowFilter):
            names=['status']
            range_fields=['ordertime']

director.update({
    'eb_moneyout':EbmoneyOutInfoPage.tableCls,
    
})
page_dc.update({
    'eb_moneyout':EbmoneyOutInfoPage
})