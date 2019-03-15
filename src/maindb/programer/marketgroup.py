from helpers.director.shortcut import page_dc,ModelTable,ModelFields,TablePage,director
from ..models import TbMarketgroup,TbMarketgroupwithmarket

class MarketGroupPage(TablePage):
    def get_label(self):
        return '市场组管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_context(self):
        ctx = super().get_context()
        marketgroup_form = MarketGroupForm(crt_user=self.crt_user)
        marketwithmarket = MarketgroupwithmarketTable(crt_user=self.crt_user)
        ctx['named_ctx']={
            'marketgroup-tabs':[
                {
                    'name':'marketgroup',
                    'label':'基本信息',
                    'com':'com-tab-fields',
                    'get_data': {
                        'fun': 'table_row',
                    },
                    'after_save': {
                        'fun': 'update_or_insert'
                    },
                    'heads': marketgroup_form.get_heads(),
                    'ops': marketgroup_form.get_operations()                        
                },
                {
                    'name':'Marketgroupwithmarket',
                    'label':'市场分组市场',
                    'com':'com-tab-table',
                    'pre_get':'rt={marketgroup:scope.par_row.groupid}',
                    'table_ctx': marketwithmarket.get_head_context(),
                    
                }
            ]
        }
        return ctx
    
    class tableCls(ModelTable):
        model = TbMarketgroup
        exclude=[]
        
        def dict_head(self, head):
            width_dc = {
                'groupname':150,
                'groupnamezh':150,
                'description':200
            }
            if width_dc.get(head['name']):
                head['width']=width_dc.get(head['name'])
            if head['name']=='groupid':
                head['editor']='com-table-switch-to-tab'
                head['ctx_name']='marketgroup-tabs'
                head['tab_name']='marketgroup'
            return head

class MarketGroupForm(ModelFields):
    class Meta:
        model = TbMarketgroup
        exclude = []


class MarketgroupwithmarketTable(ModelTable):
    model = TbMarketgroupwithmarket
    exclude=[]
    hide_fields=['groupid']
    pop_edit_field='tid'
    def inn_filter(self, query):
        if self.kw.get('marketgroup'):
            return query.filter(groupid=self.kw.get('marketgroup')) 
    
    def get_operation(self):
        ops = super().get_operation()
        for op in ops:
            if op['name']=='add_new':
                op['pre_set']='rt={groupid:scope.search_args.marketgroup}'
        return ops


class MarketgroupwithmarketForm(ModelFields):
    hide_fields=['groupid']
    class Meta:
        model = TbMarketgroupwithmarket
        exclude = []
    
    def dict_head(self, head):
        if head['name']=='marketid':
            #head['editor']='com-field-search-select'
            head['editor']='com-field-single-select2'
        return head
    
    def dict_row(self, inst):
        dc={}
        if self.kw.get('groupid'):
            dc['groupid']=self.kw.get('groupid')
        return dc
    

    

director.update({
    'marketgroup':MarketGroupPage.tableCls,
    'marketgroup.edit':MarketGroupForm,
    'Marketgroupwithmarket':MarketgroupwithmarketTable,
    'Marketgroupwithmarket.edit':MarketgroupwithmarketForm
})

page_dc.update({
    'marketgroup':MarketGroupPage,
})