from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from .. ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb. models import TbEbmoneyoutinfo

class EbmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbEbmoneyoutinfo
        exclude =[]
        
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class EbMoneyOutForm(ModelFields):
    class Meta:
        model = TbEbmoneyoutinfo
        exclude = [] 


director.update({
    'eb_moneyout':EbmoneyOutInfoPage.tableCls,
    'eb_moneyout.edit':EbMoneyOutForm,
    
})
page_dc.update({
    'eb_moneyout':EbmoneyOutInfoPage
})