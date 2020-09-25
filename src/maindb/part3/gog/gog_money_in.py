from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from maindb.models import TbGrmoneyininfo

class GogMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbGrmoneyininfo
        exclude =[]
    
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class GogMoneyInfoForm(ModelFields):
    class Meta:
        model = TbGrmoneyininfo
        exclude =[]

director.update({
    'gog_moneyinfo':GogMoneyInPage.tableCls,
    'gog_moneyinfo.edit':GogMoneyInfoForm,
})

page_dc.update({
    'gog_moneyinfo':GogMoneyInPage
})