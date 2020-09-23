from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from maindb.part3.ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb. models import TbPpmoneyoutinfo

class PPmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbPpmoneyoutinfo
        exclude =[]
        
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class PPMoneyOutInfoForm(ModelFields):
    class Meta:
        model = TbPpmoneyoutinfo
        exclude =[]

director.update({
    'pp_moneyout':PPmoneyOutInfoPage.tableCls,
    'pp_moneyout.edit':PPMoneyOutInfoForm,
    
})
page_dc.update({
    'pp_moneyout':PPmoneyOutInfoPage
})