from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch,RowSort,director_view
from helpers.func.dict_list import sort_by_name
from django.db.models import Sum
from helpers.director.model_func.dictfy import sim_dict,to_dict
from maindb.models import TbAccount,TbImmoneyoutinfo,TbImaccount
from django.utils import timezone
import time

class ImAccountPage(TablePage):
    def get_label(self):
        return '用户列表'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbImaccount
        exclude = []
        redraw_left_money_director = 'imsb/redraw_left_money'
        
        
        def inn_filter(self, query):
            return query.using('Sports_nolock')
        
        def get_operation(self):
            changeable_fields = self.permit.changeable_fields()
            return [
                {'fun':'selected_set_and_save','editor': 'com-op-btn','label':'打开资金开关','row_match':'many_row',
                 'pre_set':'rt={fundswitch:true}',
                 'confirm_msg':'确定要打开选中用户的资金开关?',
                 'visible': 'fundswitch' in changeable_fields},
                {'fun':'selected_set_and_save','editor': 'com-op-btn','label':'关闭资金开关','row_match':'many_row',
                 'pre_set':'rt={fundswitch:false}',
                  'confirm_msg':'确定要关闭选中用户的资金开关?',
                 'visible': 'fundswitch' in changeable_fields},
                {'label':'余额收回','editor':'com-op-btn','row_match':'many_row',
                 'confirm_msg':'确定要回收这些用户的余额?',
                 'visible':'availablescores' in changeable_fields,
                 'action':'var rows= ex.map(scope.ps.selected,(item)=>{return item.pk});cfg.show_load();ex.director_call("%s",{rows:rows}).then(()=>{cfg.hide_load();cfg.toast("提交成功")})'%self.redraw_left_money_director},
            ]
        
        def dict_head(self, head):
            width={
                'account':150,
                'username':150,
                'transferin':140,
                'transferout':140,
                'winorloss':140,
                'availablescores':140,
                'rebate':140,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head
                
        #def get_heads(self):
            #heads = super().get_heads()
            #heads = sort_by_name(heads,['account','account__nickname']) 
            #return heads
        
        #def get_foot_sql(self):
            #return ''' 
            #SELECT SUM(winorloss) as winorloss,
                   #SUM(transferin) as transferin,
                   #SUM(transferout) AS transferout,
                   #SUM(rebate) AS rebate,
                   #SUM(availablescores) as availablescores FROM (''' +self.sql +') bba'
        
        def statistics(self, query):
            dc = query.aggregate(total_winorloss=Sum('winorloss'),
                                 total_transferin=Sum('transferin'),
                                 total_transferout=Sum('transferout'),
                                 total_rebate=Sum('rebate'),
                                 total_availablescores=Sum('availablescores'))
            mapper = {
                'total_winorloss': 'winorloss' ,
                'total_transferin':'transferin',
                'total_transferout':'transferout',
                'total_rebate':'rebate',
                'total_availablescores':'availablescores'
            }

            normed_dc = {mapper.get(k): v for (k, v) in dc.items()}
            normed_dc.update({
                '_label':'合计'
            })
            self.footer = normed_dc
            return query
       
        
        class search(SelectSearch):
            #names = ['account__nickname','agusername']
            exact_names=['account__nickname','username','account',]
            def get_option(self, name):
                if name == 'account':
                    return {'value':name,'label':'账号ID'}
                elif name == 'account__nickname':
                    return {'value': name,
                                    'label': '账号', }
                else:
                    return super().get_option(name)
            
            def clean_search(self):
                if self.qf =='account__nickname':
                    return {
                        'account__nickname':self.q
                    }
                else:
                    return super().clean_search()
        
        class sort(RowSort):
            names = ['transferin','transferout','winorloss','availablescores']
            #general_sort ='-main.AccountId'

class ImAccountForm(ModelFields):
    class Meta:
        model = TbImaccount
        exclude = []

@director_view('imsb/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbImaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbImmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,productid = 301) )
    TbImmoneyoutinfo.objects.bulk_create(out_list)
    
director.update({
    'im_account':ImAccountPage.tableCls,
    'im_account.edit':ImAccountForm
})

page_dc.update({
    'im_account':ImAccountPage
})