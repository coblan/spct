from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowFilter,SelectSearch,RowSort,RawTable,has_permit
from ..models import TbAccount 
from django.core.exceptions import PermissionDenied

from django.db.models import F
from django.utils import timezone
from helpers.director.network import argument
import re
from django.db import connections
from hello.merchant_user import get_user_merchantid

class ChumUser(TablePage):
    
    def get_label(self):
        return '流失用户'
    
    def check_permit(self): 
        if not has_permit(self.crt_user, 'member.chum_user'):
            raise PermissionDenied('没有权限访问流失用户')
        
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbAccount
        exclude=['password','fundspassword','agent','pwupdatetime','avatar',
                 'gender','birthday','points','codeid','parentid','isriskleveldown','phone','cashchannel','agentamount','powertype']
        #hide_fields =['lastbettime']
        selectable = False
        
        #fields_sort=['myops','accountid','nickname','status','viplv','createtime','']  
        
        @classmethod
        def clean_search_args(cls, search_args):
            argument.validate_argument(search_args,{
                'sumrechargecount':[argument.int_str]
            })
            return search_args
         
        def get_heads(self):
            heads = super().get_heads()
            out_heads = []
            for head in heads:
                if head['name'] == 'myops':
                    out_heads = [head] + out_heads
                else:
                    out_heads.append(head)
            return out_heads
        
        def dict_head(self, head):
            width_dc={
                'nickname':180,
                'account':150,
                'createtime':150,
                'amount':130,
                
            }
            if width_dc.get(head['name']):
                head['width']=width_dc.get(head['name'])
            return head
        
        def getExtraHead(self):
            return [
                {'name':'sleep_days','label':'休眠天数','editor':'com-table-span'},
                {'name':'myops','label':'操作','editor':'com-table-ops-cell',
                 'show_tooltip':False,
                 'width':60,
                 'ops':[
                    {'editor':'com-op-plain-btn','icon':'fa-phone-square',
                     'css':'.myphone{color:green;font-size:150%; padding: 0;border: none;}',
                     'class':'myphone',
                     'action':'cfg.show_load();ex.director_call("call_client",{rows:[scope.row]}).then(()=>{cfg.hide_load();cfg.toast("接通成功！")})'}
                ]}
            ]
        
        def inn_filter(self, query):
            if has_permit(self.crt_user,'-i_am_merchant'):
                query = query.filter(merchant_id=get_user_merchantid(self.crt_user))
            return query.filter(sumrechargecount__lte=1)
        
        def get_operation(self):
            return [
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]
        
        def dict_row(self, inst):
            now = timezone.now()
            
            return {
                'sleep_days': (now - inst.lastbettime).days if inst.lastbettime else '',
                'account':inst.account[:3] +'****' + inst.account[7:]
            }
        
        class sort(RowSort):
            names = ['sleep_days']
            
            def get_query(self, query):
                if self.sort_str =='sleep_days':
                    return query.order_by('-lastbettime')
                elif self.sort_str =='-sleep_days':
                    return  query.order_by('lastbettime')
                else:
                    return super().get_query(query)
                
        class filters(RowFilter):
            #names=['accounttype','groupid','source','sumrechargecount']
            range_fields = ['createtime']   
            
            @property
            def names(self):
                if has_permit(self.crt_user,'-i_am_merchant'):
                    return ['accounttype','groupid','source','sumrechargecount']
                else:
                    return ['merchant','accounttype','groupid','source','sumrechargecount']
                
            def dict_head(self, head):
                if head['name'] == 'sumrechargecount':
                    head['options'] =[]
                    head['width'] ='150px'
                    head['editor'] = 'com-filter-compare'
                return head
            
        class search(SelectSearch):
            names = ['nickname']
            exact_names = ['accountid','parentid']

            def get_option(self, name):
                if name == 'accountid':
                    return {'value': name,
                            'label': '账户ID', }
                elif name == 'nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }
                elif name =='parentid':
                    return {
                        'value':name,
                        'label':'父级ID',
                    }

            def clean_search(self):
                if self.qf in ['accountid','parentid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search() 
                
            def get_query(self, query):
                if self.qf == 'parentid':
                    return query
                else:
                    return super().get_query(query)


director.update({
    'chum_user':ChumUser.tableCls
})

#page_dc.update({
    #'chum_user':ChumUser
#})