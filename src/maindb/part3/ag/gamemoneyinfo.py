from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch,RowFilter,RowSort
from maindb.models import TbGamemoneyininfo,TbMerchants
from helpers.func.dict_list import sort_by_name
from django.db.models import Sum
from django.utils import timezone
from django.db.models import F

class GameMoneyininfoPage(TablePage):
    def get_label(self):
        return '资金转入'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbGamemoneyininfo
        exclude =[]
        
        def getExtraHead(self):
            return [
                {'name':'account__nickname','label':"账号昵称",},
                {'name':'account__merchant__name','label':'商户'},
            ]
        
        def get_operation(self):
            return [
                {'label':'等待转入',
                 'editor':'com-btn',
                 'row_match':'many_row',
                 'match_express':'scope.row.status==1 && scope.row._ordertime_life>300',
                 'match_msg':'只能选择下单时间超过5分钟且状态为正在转入的记录',
                 'preset_express':'rt={status:0}',
                 'click_express':'scope.ps.selected_set_and_save(scope.head)',
                 'visible':self.permit.can_edit()}
            ]
        
        @classmethod
        def clean_search_args(cls, search_args):
            if '_searched' not in search_args:
                now = timezone.now()
                search_args['_start_ordertime'] = now.strftime('%Y-%m-%d '+'00:00:00')
                search_args['_end_ordertime'] = now.strftime('%Y-%m-%d '+'23:59:59')
                search_args['_searched'] = 1
            return search_args
        
        def inn_filter(self, query):
            query = query.using('Sports_nolock')
            if self.crt_user.merchant:
                query = query.filter(account__merchant = self.crt_user.merchant)
            query = query.annotate(account__merchant__name = F('account__merchant__name'))
            return query
        
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
            now = timezone.now()
            return {
                'account__nickname':inst.account.nickname,
                'account__merchant__name':inst.account__merchant__name,
                '_ordertime_life': (now - inst.ordertime).seconds
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
            #names = ['account__nickname','username']
            exact_names=['account__nickname','username','account']
            
            def get_option(self, name):
                if name == 'account':
                    return {'value':name,'label':'账号ID'}
                elif name == 'account__nickname':
                    return {'value': name,
                                    'label': '用户昵称', }
                else:
                    return super().get_option(name)
        
        class filters(RowFilter):
            range_fields=['ordertime']
            
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['status']
                else:
                    return ['account__merchant_id','status']
                
            def getExtraHead(self):
                if self.crt_user.merchant:
                    return []
                else:
                    return [{
                        'name':'account__merchant_id','label':'商户','editor':'com-filter-select','options':[
                            {'value':x.pk,'label':str(x)} for x in TbMerchants.objects.all()
                        ]
                    }]
        
        class sort(RowSort):
            names = ['amount','handtime','ordertime']


class GameMoneyinfoForm(ModelFields):
    class Meta:
        model = TbGamemoneyininfo
        exclude =[]

director.update({
    'gamemoneyininfo':GameMoneyininfoPage.tableCls,
    'gamemoneyininfo.edit':GameMoneyinfoForm
})

page_dc.update({
    'gamemoneyininfo':GameMoneyininfoPage
})