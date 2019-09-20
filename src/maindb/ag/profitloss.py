from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director,SelectSearch,RowFilter
from ..models import TbAgprofitloss
from helpers.func.dict_list import sort_by_name
from django.db.models import Sum

class AgprofitlossPage(TablePage):
    def get_label(self):
        return '投注列表'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbAgprofitloss
        exclude = ['profitlosstype','refid','parentid','bettime','savetime']
        
        def getExtraHead(self):
            return [
                {'name':'account__nickname','label':'昵称','editor':'com-table-span'}
            ]
        
        def dict_head(self, head):
            width = {
                'memo':200
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            if head['name'] == 'account':
                head['editor'] = 'com-table-span'
            elif head['name'] =='iswin':
                head['editor'] = 'com-table-bool-shower'
            return head
        
        def dict_row(self, inst):
            return {
                'account__nickname':inst.account.nickname
            }
        
        def get_heads(self):
            heads = super().get_heads()
            heads = sort_by_name(heads,['profitlossid','account','account__nickname','playid','username'])
            return heads
        
        def statistics(self, query):
            dc = query.aggregate(total_profitlossmoney=Sum('profitlossmoney'),
                                 total_prizemoney=Sum('prizemoney'),
                                 total_winmoney=Sum('winmoney'),)
     
            #for k in dc:
                #dc[k] = str(round(dc.get(k, 0) or 0, 2))
            normed_dc = {k[6:]: v for (k, v) in dc.items()}
            normed_dc.update({
                '_label':'合计'
            })
            self.footer = normed_dc
            return query
        
        class search(SelectSearch):
            names = ['account__nickname','username']
            exact_names=['account']
            
            def get_option(self, name):
                if name == 'account':
                    return {'value':name,'label':'账号ID'}
                elif name == 'account__nickname':
                    return {'value': name,
                                    'label': '用户昵称', }
                else:
                    return super().get_option(name)
        class filters(RowFilter):
            range_fields=['profitlosstime']

director.update({
    'agprofitloss':AgprofitlossPage.tableCls
})

page_dc.update({
    'agprofitloss':AgprofitlossPage
})