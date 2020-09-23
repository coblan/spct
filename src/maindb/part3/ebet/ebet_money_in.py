from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from maindb. models import TbEbmoneyininfo

class EbMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbEbmoneyininfo
        exclude =[]
    
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class EbmoneyinfoForm(ModelFields):
    class Meta:
        model = TbEbmoneyininfo
        exclude =[]

director.update({
    'eb_moneyinfo':EbMoneyInPage.tableCls,
    'eb_moneyinfo.edit':EbmoneyinfoForm,
})

page_dc.update({
    'eb_moneyinfo':EbMoneyInPage
})