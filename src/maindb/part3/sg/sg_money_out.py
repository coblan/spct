from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb.models import TbSgmoneyoutinfo

class SgmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbSgmoneyoutinfo
        exclude =[]
        
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class SgMoneyoutInfoForm(ModelFields):
    class Meta:
        model = TbSgmoneyoutinfo
        exclude =[]

director.update({
    'sg_moneyout':SgmoneyOutInfoPage.tableCls,
    'sg_moneyout.edit':SgMoneyoutInfoForm,
    
})
page_dc.update({
    'sg_moneyout':SgmoneyOutInfoPage
})