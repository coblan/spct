from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from maindb.models import TbImmoneyininfo

class IMMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbImmoneyininfo
        exclude =[]
    
        #class filters(RowFilter):
            #names=['status','productid']
            #range_fields=['ordertime']

class IMMoneyinfoForm(ModelFields):
    class Meta:
        model = TbImmoneyininfo
        exclude =[]

director.update({
    'immoneyinfo':IMMoneyInPage.tableCls,
    'immoneyinfo.edit':IMMoneyinfoForm,
})

page_dc.update({
    'immoneyinfo':IMMoneyInPage
})