from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director

from ..models import TbSporttypes
#from helpers.director.access.permit import can_touch

class SportsTypesPage(TablePage):
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_label(self):
        return '运动类型'
    
    class tableCls(ModelTable):
        model = TbSporttypes
        exclude =['createtime','status','onlinetime','sort']
        pop_edit_field = 'tid'
        def get_operation(self):
            changeable_fields = self.permit.changeable_fields()
            return [
                {'fun':'selected_set_and_save','label':'启用','editor':'com-op-btn','pre_set':'rt={enabled:true}',
                 'confirm_msg':'是否【启用】选中运动类型','match_row':'many_row','visible':'enabled' in changeable_fields},
                {'fun':'selected_set_and_save','label':'禁用','editor':'com-op-btn','pre_set':'rt={enabled:false}',
                 'confirm_msg':'是否【禁用】选中运动类型','match_row':'many_row','visible':'enabled' in changeable_fields},
            ]
        
        def dict_head(self, head):
            dc={
                'updatetime':200,
                'sportnamezh':100,
            }
            if dc.get(head['name']):
                head['width']=dc.get(head['name'])
            return head
        

class SportsTypeForm(ModelFields):
    class Meta:
        model = TbSporttypes
        exclude=['createtime','status','tid','onlinetime','sort']
        
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