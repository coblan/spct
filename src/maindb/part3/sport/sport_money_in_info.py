from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from ..ag.gamemoneyinfo import GameMoneyininfoPage
from maindb.models import TbSportmoneyininfo

class SportMoneyInPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model =TbSportmoneyininfo
        exclude =[]

class SportMoneyinfoForm(ModelFields):
    class Meta:
        model = TbSportmoneyininfo
        exclude =[]

director.update({
    'sportmoneyinfo':SportMoneyInPage.tableCls,
    'sportmoneyinfo.edit':SportMoneyinfoForm,
})

page_dc.update({
    'sportmoneyinfo':SportMoneyInPage
})