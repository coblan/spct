from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..models import TbBackendloginlog

class BackendLoginlogPage(TablePage):
    def get_label(self):
        return '后台登录日志'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbBackendloginlog
        exclude =[]
        
        def dict_head(self, head):
            width ={
                'ipaddress':100,
                'area':150,
            }
            if head['name'] in width:
                head['width'] =width.get(head['name'])
            return head
        
        class filters(RowFilter):
            names = ['username','area']
            icontains=['username','area']
            range_fields=['createtime']
        
        

director.update({
    'bacnend_loginlog':BackendLoginlogPage.tableCls
})

page_dc.update({
    'bacnend_loginlog':BackendLoginlogPage
})