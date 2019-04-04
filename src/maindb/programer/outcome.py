from helpers.director.shortcut import ModelFields,ModelTable,TablePage,page_dc,director,RowSearch
from ..models import TbOutcomes

class OutcomePage(TablePage):
    def get_label(self):
        return '投注项'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        pop_edit_field='uniqueoutcomid'
        model = TbOutcomes
        exclude = []
        
        def dict_head(self, head):
            width_dc ={
                'uniqueoutcomid':120,
                'outcomeid':300,
                'outcomename':180,
                'outcomenamezh':190,
            }
            if head['name'] in width_dc:
                head['width'] = width_dc.get(head['name'])
            return head
        
        def get_operation(self):
            return []
        
        class search(RowSearch):
            names =['outcomeid','outcomename','outcomenamezh']

class OutcomeForm(ModelFields):
    readonly=['uniqueoutcomid','outcomeid','description','outcomename']

    class Meta:
        model = TbOutcomes
        exclude =[]

director.update({
    'outcome':OutcomePage.tableCls,
    'outcome.edit':OutcomeForm
    
})

page_dc.update({
    'outcome':OutcomePage
})