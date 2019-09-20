from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch,RowFilter,RowSort
from ..models import TbGamemoneyininfo
from helpers.func.dict_list import sort_by_name
from django.db.models import Sum
from django.utils import timezone

class GameMoneyininfoPage(TablePage):
    def get_label(self):
        return '资金转入AG'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbGamemoneyininfo
        exclude =['tsamp']
        
        def getExtraHead(self):
            return [
                {'name':'account__nickname','label':"账号昵称",}
            ]
        
        @classmethod
        def clean_search_args(cls, search_args):
            if '_searched' not in search_args:
                now = timezone.now()
                search_args['_start_ordertime'] = now.strftime('%Y-%m-%d '+'00:00:00')
                search_args['_end_ordertime'] = now.strftime('%Y-%m-%d '+'23:59:59')
                search_args['_searched'] = 1
            return search_args
        
        def dict_head(self, head):
            width={
                'account__nickname':150,
                'username':150,
                'memo':200,
                'amount':150,
                
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            if head['name'] =='account':
                head['label'] = '用户ID'
                head['editor'] = 'com-table-span'
            return head
        
        def dict_row(self, inst):
            return {
                'account__nickname':inst.account.nickname,
            }
        
        def get_heads(self):
            heads = super().get_heads()
            heads = sort_by_name(heads,['moneyinid','account','account__nickname','username']) 
            return heads
        
        def statistics(self, query):
            dc = query.aggregate(total_amount=Sum('amount'),)
            
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
            names=['status']
            range_fields=['ordertime']
        
        class sort(RowSort):
            names = ['amount','handtime','ordertime']

director.update({
    'gamemoneyininfo':GameMoneyininfoPage.tableCls
})

page_dc.update({
    'gamemoneyininfo':GameMoneyininfoPage
})