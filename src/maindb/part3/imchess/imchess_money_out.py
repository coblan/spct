from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from maindb.part3.ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb. models import TBIMChessMoneyOutInfo

class IMChessmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TBIMChessMoneyOutInfo
        exclude =[]
        
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class IMChessMoneyOutForm(ModelFields):
    class Meta:
        model = TBIMChessMoneyOutInfo
        exclude =[]


director.update({
    'imchess_moneyout':IMChessmoneyOutInfoPage.tableCls,
    'imchess_moneyout.edit':IMChessMoneyOutForm,
    
})
page_dc.update({
    'imchess_moneyout':IMChessmoneyOutInfoPage
})