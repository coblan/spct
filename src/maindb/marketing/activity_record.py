from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from maindb.models import TbActivityRecord
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
        
        class filters(RowFilter):
            names = ['account__nickname']
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