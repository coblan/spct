from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch
from .. models import TbAgaccount
from helpers.func.dict_list import sort_by_name
from django.db.models import Sum

class AgAccountPage(TablePage):
    def get_label(self):
        return '用户列表'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbAgaccount
        exclude = ['bonusrate','rebate','fishavailablescores','lastfishupdatetime']
        
        def getExtraHead(self):
            return [
                {'name':'account__nickname','label':"账号昵称",}
            ]
        
        def get_operation(self):
            return [
                {'fun':'selected_set_and_save','editor': 'com-op-btn','label':'打开资金开关','row_match':'many_row','pre_set':'rt={fundswitch:true}',
                 'confirm_msg':'确定要打开选中用户的资金开关?',
                 'visible': 'fundswitch' in self.permit.changeable_fields()},
                {'fun':'selected_set_and_save','editor': 'com-op-btn','label':'关闭资金开关','row_match':'many_row','pre_set':'rt={fundswitch:false}',
                  'confirm_msg':'确定要关闭选中用户的资金开关?',
                 'visible': 'fundswitch' in self.permit.changeable_fields()},
            ]
        
        def dict_head(self, head):
            width={
                'account__nickname':150,
                'agusername':150,
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
            heads = sort_by_name(heads,['account','account__nickname']) 
            return heads
        
        def statistics(self, query):
            dc = query.aggregate(total_winorloss=Sum('winorloss'),
                                 total_transferin=Sum('transferin'),
                                 total_transferout=Sum('transferout'),
                                 total_availablescores=Sum('availablescores'))
            mapper = {
                'total_winorloss': 'winorloss' ,
                'total_transferin':'transferin',
                'total_transferout':'transferout',
                'total_availablescores':'availablescores'
            }
            #for k in dc:
                #dc[k] = str(round(dc.get(k, 0) or 0, 2))
            normed_dc = {mapper.get(k): v for (k, v) in dc.items()}
            normed_dc.update({
                '_label':'合计'
            })
            self.footer = normed_dc
            return query
       
        
        class search(SelectSearch):
            names = ['account__nickname','agusername']
            exact_names=['account']
            
            def get_option(self, name):
                if name == 'account':
                    return {'value':name,'label':'账号ID'}
                elif name == 'account__nickname':
                    return {'value': name,
                                    'label': '用户昵称', }
                else:
                    return super().get_option(name)

class AgAccountForm(ModelFields):
    class Meta:
        model = TbAgaccount
        exclude = []
        


director.update({
    'agaccount':AgAccountPage.tableCls,
    'agaccount.edit':AgAccountForm
})

page_dc.update({
    'agaccount':AgAccountPage
})