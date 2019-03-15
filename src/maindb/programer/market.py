from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from ..models import TbMarkets

class MarketPage(TablePage):
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_label(self):
        return '玩法管理'
    
    class tableCls(ModelTable):
        model = TbMarkets
        exclude=[]
        pop_edit_field = 'marketid'
        
        def dict_head(self, head):
            width_dc ={
                'marketname':140,
                'marketnamezh':180,
                'includesoutcomestype':150,
                'outcometype':130,
            }
            if width_dc.get(head['name']):
                head['width'] = width_dc.get(head['name'])
            return head
        
        def get_operation(self):
            return []        

class MarketForm(ModelFields):
    class Meta:
        model = TbMarkets
        exclude = []
        
    def dict_head(self, head):
        if head['name']=='marketid':
            head['readonly']='Boolean(scope.row.pk)'
        if head['name'] not in ['marketnamezh','enabled','description']:
            head['readonly']=True
        return head   
    


director.update({
    'marketpage':MarketPage.tableCls,
    'marketpage.edit':MarketForm,
})

page_dc.update({
    'marketpage':MarketPage
})