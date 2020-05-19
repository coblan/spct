from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter,has_permit
from maindb.models import TbActivityRecord
from hello.merchant_user import get_user_merchantid

class ActivityRecoredPage(TablePage):
    def get_label(self):
        return '活动记录'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbActivityRecord
        exclude = []
        
        def dict_head(self, head):
            width ={
                'activity':130,
                'account':130,
                'amount':100,
                'bonus':120,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head
        
        def inn_filter(self, query):
            if has_permit(self.crt_user,'-i_am_merchant'):
                query = query.filter(merchant_id = get_user_merchantid(self.crt_user))
            return query
        
        class filters(RowFilter):
            @property
            def names(self):
                if has_permit(self.crt_user,'-i_am_merchant'):
                    return ['account__nickname']
                else:
                    return ['merchant','account__nickname']
                    
            range_fields=['createtime']
            icontains = ['account__nickname']
            def getExtraHead(self):
                return [
                    {'name':'account__nickname','label':'用户昵称'}
                ]

director.update({
    'activity_record':ActivityRecoredPage.tableCls,
})

page_dc.update({
    'activity_record':ActivityRecoredPage
})