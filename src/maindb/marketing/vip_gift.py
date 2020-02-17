from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from ..models import TbVipgift

class VipgiftPage(TablePage):
    def get_label(self):
        return 'VIP豪礼'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbVipgift
        exclude = []
        pop_edit_fields=['tid']
        
        def dict_head(self, head):
            width ={
                'title':160,
                'content':160,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head

class VipgiftForm(ModelFields):
    class Meta:
        model = TbVipgift
        exclude =[]
        

director.update({
    'vipgift':VipgiftPage.tableCls,
    'vipgift.edit':VipgiftForm,
})

page_dc.update({
    'vipgift':VipgiftPage
})