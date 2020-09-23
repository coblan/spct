from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from maindb.part3.ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb. models import TBVRMoneyOutInfo

class VRmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TBVRMoneyOutInfo
        exclude =[]
        
        #class filters(RowFilter):
            #names=['status']
            #range_fields=['ordertime']

class VRMoneyOutInfoForm(ModelFields):
    class Meta:
        model = TBVRMoneyOutInfo
        exclude =[]

director.update({
    'vr_moneyout':VRmoneyOutInfoPage.tableCls,
    'vr_moneyout.edit':VRMoneyOutInfoForm,
    
})
page_dc.update({
    'vr_moneyout':VRmoneyOutInfoPage
})