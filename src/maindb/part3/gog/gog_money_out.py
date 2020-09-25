from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb.models import TbGrmoneyoutinfo

class GogmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbGrmoneyoutinfo
        exclude =[]
        
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class GogMoneyoutInfoForm(ModelFields):
    class Meta:
        model = TbGrmoneyoutinfo
        exclude =[]

director.update({
    'gog_moneyout':GogmoneyOutInfoPage.tableCls,
    'gog_moneyout.edit':GogMoneyoutInfoForm,
    
})
page_dc.update({
    'gog_moneyout':GogmoneyOutInfoPage
})