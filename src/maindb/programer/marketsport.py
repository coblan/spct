from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director
from maindb.models import TbMarketlistwithsport

class MarketSportPage(TablePage):
    def get_label(self):
        return '列表玩法'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        pop_edit_fields = ['tid']
        model = TbMarketlistwithsport
        exclude = []
        
        def dict_head(self, head):
            width = {
                'market':200,
                'marketshowname':160,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head

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