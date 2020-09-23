from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb.models import TbPtmoneyoutinfo

class PtmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbPtmoneyoutinfo
        exclude =[]
        
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class PtMoneyOutInfoForm(ModelFields):
    class Meta:
        model = TbPtmoneyoutinfo
        exclude =[]

director.update({
    'pt_moneyout':PtmoneyOutInfoPage.tableCls,
    'pt_moneyout.edit':PtMoneyOutInfoForm,
    
})
page_dc.update({
    'pt_moneyout':PtmoneyOutInfoPage
})