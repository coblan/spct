from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director,RowSort
from ..models import TbPaychannelgroup

class PaychannelgroupPage(TablePage):
    def get_label(self):
        return '充值渠道组'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        pop_edit_fields=['groupid']
        model = TbPaychannelgroup
        exclude = []
        def dict_head(self, head):
            width = {
                'groupway':120,
                'groupicon':200,
                'groupsubtitle':150,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head
        
        class sort(RowSort):
            names = ['sort']

class TbPaychannelgroupForm(ModelFields):
    class Meta:
        model = TbPaychannelgroup
        exclude = []

director.update({
    'TbPaychannelgroup':PaychannelgroupPage.tableCls,
    'TbPaychannelgroup.edit':TbPaychannelgroupForm
})

page_dc.update({
    'TbPaychannelgroup':PaychannelgroupPage
})