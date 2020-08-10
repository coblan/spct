from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director,RowFilter,has_permit
from maindb.models import TbUserLog
from hello.merchant_user import get_user_merchantid
from django.utils import timezone

class UserlogPage(TablePage):
    def get_label(self):
        return '用户日志'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    class tableCls(ModelTable):
        model = TbUserLog
        exclude=[]
        
        @classmethod
        def clean_search_args(cls, search_args):
            if '_seached' not in search_args:
                now = timezone.now()
                search_args['_start_createtime'] = now.strftime('%Y-%m-%d 00:00:00')
                search_args['_end_createtime'] = now.strftime('%Y-%m-%d 23:59:59')
                search_args['_seached'] = 1
            return search_args
        
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
            #if self.is_export_excel:
            query= query.using('Sports_nolock')
            if self.crt_user.merchant:
                query = query.filter(merchant_id=self.crt_user.merchant.id)
            return query
        
        def get_operation(self):
            return [
                    {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
                ]
        
        class filters(RowFilter):
            
            range_fields=['createtime']
            icontains=['account__nickname']
            
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['account__nickname','operatetype']
                else:
                    return ['merchant','account__nickname','operatetype']
            
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