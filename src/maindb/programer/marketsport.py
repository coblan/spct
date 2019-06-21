from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director
from maindb.models import TbMarketlistwithsport

class MarketSportPage(TablePage):
    def get_label(self):
        return '何步云专用'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        pop_edit_field = 'tid'
        model = TbMarketlistwithsport
        exclude = []

class MarketSportForm(ModelFields):
    class Meta:
        model = TbMarketlistwithsport
        exclude =[]

director.update({
    'marketsport':MarketSportPage.tableCls,
    'marketsport.edit':MarketSportForm,
})

page_dc.update({
    'marketsport':MarketSportPage
})