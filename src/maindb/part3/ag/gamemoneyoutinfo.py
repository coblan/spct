from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,director,RowFilter
from maindb.models import TbGamemoneyoutinfo
from . gamemoneyinfo import GameMoneyininfoPage
from helpers.func.dict_list import sort_by_name

class GamemoneyoutinfoPage(TablePage):
    def get_label(self):
        return '资金转出AG'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model = TbGamemoneyoutinfo
        exclude = []
        
        def get_heads(self):
            heads = super().get_heads()
            heads = sort_by_name(heads,['moneyoutid','account','account__nickname','username']) 
            return heads

#class GamemoneyoutinfoForm(ModelFields):
    #class Meta:
        #model = TbGamemoneyoutinfo
        #exclude = []

director.update({
    'gamemoneyoutinfo':GamemoneyoutinfoPage.tableCls,
    #'gamemoneyoutinfo.edit':GamemoneyoutinfoForm,
})

page_dc.update({
    'gamemoneyoutinfo':GamemoneyoutinfoPage
})