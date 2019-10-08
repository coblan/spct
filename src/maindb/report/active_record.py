from helpers.director.shortcut import TablePage,ModelTable,director,page_dc,RowFilter

from maindb.models import TbActivityRecord

class ActivityRecordPage(TablePage):
    def get_label(self):
        return '活动记录'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbActivityRecord
        exclude =['bid']
        
        def dict_head(self, head):
            width_dc ={
                'account':150
            }
            if head['name'] in width_dc:
                head['width'] = width_dc.get(head['name'])
            return head
        
        class filters(RowFilter):
            names =['activity','account__nickname']
            icontains=['account__nickname']
            def getExtraHead(self):
                return [
                    {'name':'account__nickname','placeholder':'用户昵称','editor':'com-filter-text'}
                ]
        

director.update({
    'activityrecord':ActivityRecordPage.tableCls,
})

page_dc.update({
    'activityrecord':ActivityRecordPage
})