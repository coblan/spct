from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from maindb.models import TbActivityRecord
class ActivityRecoredPage(TablePage):
    def get_label(self):
        return '活动记录'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbActivityRecord
        exclude = []

director.update({
    'activity_record':ActivityRecoredPage.tableCls,
})

page_dc.update({
    'activity_record':ActivityRecoredPage
})