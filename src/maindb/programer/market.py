from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowSearch,RowFilter,RowSort
from ..models import TbMarkets
import base64

class MarketPage(TablePage):
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_label(self):
        return '玩法管理'
    
    class tableCls(ModelTable):
        model = TbMarkets
        exclude=[]
        pop_edit_fields = ['marketid']
        
        def dict_head(self, head):
            width_dc ={
                'marketname':140,
                'marketnamezh':200,
                'includesoutcomestype':150,
                'outcometype':130,
            }
            if width_dc.get(head['name']):
                head['width'] = width_dc.get(head['name'])
            return head
        
        def get_operation(self):
            return []
        
        class search(RowSearch):
            names=['marketname','marketnamezh','marketid']
        
        class filters(RowFilter):
            names=['includesoutcomestype','outcometype','enabled']
        

class MarketForm(ModelFields):
    field_sort=['marketid','marketname','marketnamezh','description','enabled','templateid','isasian','sort',]
    class Meta:
        model = TbMarkets
        exclude = []
        
        
    def dict_head(self, head):
        if head['name']=='marketid':
            head['readonly']='Boolean(scope.row.pk)'
        if head['name']  in  ['marketname']: #['marketnamezh','enabled','description','isasian','templateid']:
            head['readonly']=True
        return head   
    

class UserMarketPage(MarketPage):
    class tableCls(MarketPage.tableCls):
        exclude=['includesoutcomestype','outcometype','isasian','templateid','ticketdelay']
        def inn_filter(self, query):
            return query.filter(enabled=1)
        
        class filters(RowFilter):
            names=['enabled']
        class sort(RowSort):
            names=['sort']

class UserMarketForm(MarketForm):
    
    field_sort=['marketid','marketname','marketnamezh','description','enabled','sort','weight','extendweight']
    readonly=['marketid','marketname','marketnamezh','description','enabled',]
    class Meta:
        model = TbMarkets
        fields = ['marketid','marketname','marketnamezh','description','enabled','sort','weight','extendweight']
    
    def dict_head(self, head):
        if head['name'] =='extendweight':
            express = base64.b64encode("parseFloat(scope.value) > 0".encode('utf-8'))
            msg = base64.b64encode('必须大于0'.encode('utf-8'))
            head['fv_rule']= 'express(%s , %s)'%( express.decode('utf-8'),msg.decode('utf-8'))
        return head


director.update({
    'marketpage':MarketPage.tableCls,
    'marketpage.edit':MarketForm,
    
    'usermarket':UserMarketPage.tableCls,
    'usermarket.edit':UserMarketForm
})

page_dc.update({
    'marketpage':MarketPage,
    
    'usermarket':UserMarketPage,
})