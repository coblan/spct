from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director

from ..models import TbSporttypes


class SportsTypesPage(TablePage):
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_label(self):
        return '运动类型'
    
    class tableCls(ModelTable):
        model = TbSporttypes
        exclude =[]
        #pop_edit_field='tid'
        def get_operation(self):
            return [
                {'fun':'selected_set_and_save','label':'启用','editor':'com-op-btn','pre_set':'rt={enabled:true}','match_row':'many_row'},
                {'fun':'selected_set_and_save','label':'禁用','editor':'com-op-btn','pre_set':'rt={enabled:false}','match_row':'many_row'},
            ]

class SportsTypeForm(ModelFields):
    class Meta:
        model = TbSporttypes
        exclude=[]
        
    def dict_row(self, inst):
        return {
            'updatetime':inst.updatetime.strftime('%Y-%m-%d %H:%M:%S')
        }

director.update({
    'sportstype':SportsTypesPage.tableCls,
    'sportstype.edit':SportsTypeForm
})



page_dc.update({
    'sportstype':SportsTypesPage
})