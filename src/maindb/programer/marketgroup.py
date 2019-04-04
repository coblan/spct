from helpers.director.shortcut import page_dc,ModelTable,ModelFields,TablePage,director,RowSearch,\
     director_view,RowFilter
from ..models import TbMarketgroup,TbMarketgroupwithmarket,TbMarkets
from django.db.models import Q

class MarketGroupPage(TablePage):
    def get_label(self):
        return '玩法组管理'
    
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
                    'get_row':'rt=scope.vc.get_row("marketgroup.edit",{pk:scope.vc.par_row.pk})',
                    #'get_data': {
                        #'fun': 'table_row',
                    #},
                    'after_save': {
                        'fun': 'update_or_insert'
                    },
                    'heads': marketgroup_form.get_heads(),
                    'ops': marketgroup_form.get_operations(),
                     'event_slots':[
                        {'event':'finish','express':'scope.ps.$emit("group-changed")'},
                    ]
                },
                {
                    'name':'Marketgroupwithmarket',
                    'label':'玩法组关联',
                    'com':'com-tab-table',
                    'pre_set':'rt={marketgroup:scope.par_row.groupid}',
                    'table_ctx': marketwithmarket.get_head_context(),
                    'event_slots':[
                       {'par_event':'group-changed','express':'scope.vc.loaded=false'},
                    ]
                   
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
        
        def get_operation(self):
            ops = super().get_operation()
            out_ops =[x for x in ops if x['name'] != 'delete_selected']
            return out_ops
            
        
        class search(RowSearch):
            names=['groupname','groupnamezh']
        class filters(RowFilter):
            names=['sportid']

class MarketGroupForm(ModelFields):
    class Meta:
        model = TbMarketgroup
        exclude = []
    
    #def getExtraHeads(self):
        #return [
            #{'name':'group_sort','label':'组排序','editor':'com-field-number'}
        #]
    
    #def dict_row(self, inst):
        
        #obj = TbMarketgroupwithmarket.objects.filter(groupid=inst.groupid).first()
        #if obj:
            #group_sort=obj.groupsort
        #else:
            #group_sort=0
        #return {
            #'group_sort':group_sort,
            #'meta_group_sort':group_sort,
        #}
    
    def dict_head(self, head):
        if head['name']=='groupid':
            head['readonly']='Boolean(scope.row.pk)'
        return head
    
    #def clean_save(self):
        #if self.kw['group_sort'] !=self.kw['meta_group_sort']:
            #TbMarketgroupwithmarket.objects.filter(groupid=self.instance.groupid).update(groupsort=self.kw['group_sort'])
    

class MarketgroupwithmarketTable(ModelTable):
    model = TbMarketgroupwithmarket
    exclude=[]
    hide_fields=['groupid']
    pop_edit_field='tid'
    def inn_filter(self, query):
        if self.kw.get('marketgroup'):
            return query.filter(groupid=self.kw.get('marketgroup')) 
    
    def dict_head(self, head):
        width_dc ={
            'marketid':250,
            'marketsort':130,
            'sort':130,
        }
        if head['name'] in width_dc:
            head['width'] = width_dc.get(head['name'])
        return head
    
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
            head['options']=[]
            head['dyn_options']='rt=scope.vc.update_options("get_market_options",scope.row)'
            head['style']=".jjyy select{width:300px}"
            head['class']='jjyy'
            #head['options']=[{'value':x.pk,'label':str(x) } for x in TbMarkets.objects.filter(enabled=True)]
            #head['event_slots']=[
                #{'event':'input','express':'alert("jjyy")'},
            #]
        return head
    
    def dict_row(self, inst):
        dc={}
        if self.kw.get('groupid'):
            dc['groupid']=self.kw.get('groupid')
        return dc
    

def get_market_options(**kws): 
    groupid= kws.get('groupid')
    exclude_ls = [x.marketid.marketid for x in TbMarketgroupwithmarket.objects.filter(groupid=groupid)]
    marketid = kws.get('marketid')
    if marketid:
        exclude_ls=list(filter(lambda x:x!=marketid,exclude_ls))
    return [{'value':x.pk,'label':str(x) } for x in TbMarkets.objects.filter(enabled=True).exclude(marketid__in=exclude_ls)]
 
director.update({
    'marketgroup':MarketGroupPage.tableCls,
    'marketgroup.edit':MarketGroupForm,
    'Marketgroupwithmarket':MarketgroupwithmarketTable,
    'Marketgroupwithmarket.edit':MarketgroupwithmarketForm,
    
    'get_market_options':get_market_options,
})

page_dc.update({
    'marketgroup':MarketGroupPage,
})