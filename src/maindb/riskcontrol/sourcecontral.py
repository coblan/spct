from helpers.director.shortcut import TablePage,ModelFields,ModelTable,field_map,director,page_dc
from ..models import TbSourcecontrol
class SourceControlPage(TablePage):
    template = 'jb_admin/table.html'
    
    def get_label(self):
        return '数据源维护'
    
    class tableCls(ModelTable):
        model=TbSourcecontrol
        exclude=[]
        pop_edit_fields = ['tid']

class SoureceControlForm(ModelFields):
    readonly=['source','sporttype','oddskind','sites','status','enabled','updatetime']
    class Meta:
        model=TbSourcecontrol
        exclude=[]

director.update({
    'sourececontrol':SourceControlPage.tableCls,
    'sourececontrol.edit':SoureceControlForm
})

page_dc.update({
    'sourececontrol':SourceControlPage,
    
})