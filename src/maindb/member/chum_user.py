from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowFilter,SelectSearch
from ..models import TbAccount 
from django.core.exceptions import PermissionDenied
from helpers.director.access.permit import has_permit

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
                 'gender','birthday','points','codeid','parentid','isriskleveldown','phone','cashchannel']
        
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
        
        def inn_filter(self, query):
            return query.filter(sumrechargecount__lte=1)
        
        def get_operation(self):
            return [
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]
        
        class filters(RowFilter):
            names=['accounttype','groupid']
            range_fields = ['createtime']   
        
        class search(SelectSearch):
            names = ['nickname']
            exact_names = ['accountid']

            def get_option(self, name):
                if name == 'accountid':
                    return {'value': name,
                            'label': '账户ID', }
                elif name == 'nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }

            def clean_search(self):
                if self.qf in ['accountid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()        

director.update({
    'chum_user':ChumUser.tableCls
})

page_dc.update({
    'chum_user':ChumUser
})