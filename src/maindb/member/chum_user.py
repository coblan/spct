from helpers.director.shortcut import TablePage,ModelTable,page_dc,director
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
        exclude=['password','fundspassword']
        
        def inn_filter(self, query):
            return query.filter(sumrechargecount__lte=1)
        
        def get_operation(self):
            return [
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]

director.update({
    'chum_user':ChumUser.tableCls
})

page_dc.update({
    'chum_user':ChumUser
})