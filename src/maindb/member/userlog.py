from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director,RowFilter
from maindb.models import TbUserLog

class UserlogPage(TablePage):
    def get_label(self):
        return '用户日志'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    class tableCls(ModelTable):
        model = TbUserLog
        exclude=[]
        
        def dict_head(self, head):
            width = {
                'ipaddress':150,
                'account':150,
                'area':130,
                'deviceid':150,
                'createtime':150,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head
        
        def inn_filter(self, query):
            if self.is_export_excel:
                return query.using('Sports_nolock')
            else:
                return query
        
        def get_operation(self):
            return [
                    {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
                ]
        
        class filters(RowFilter):
            names=['account__nickname','operatetype']
            range_fields=['createtime']
            icontains=['account__nickname']
            def getExtraHead(self):
                return [
                    {'name':'account__nickname','label':'用户昵称'}
                ]

director.update({
    'userlog':UserlogPage.tableCls
})
page_dc.update({
    'userlog':UserlogPage
})