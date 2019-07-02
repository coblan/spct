from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,field_map,model_to_name,BaseFieldProc
from maindb.models import TbAdjusttemplate
import json

class AdjusttemplatePage(TablePage):
    def get_label(self):
        return '调水模板'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        pop_edit_fields=['templateid']
        model = TbAdjusttemplate
        exclude = []
        
        def dict_head(self, head):
            if head['name'] == 'adjustsettings':
                head['editor']='com-table-label-shower'
            return head
        
        def get_operation(self):
            ops = super().get_operation()
            ops= [x for x in ops if x['name'] !='delete_selected']
            ops+=[
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '启用', 'confirm_msg': '确认启用？',
                 'pre_set': 'rt={status:1}', 'row_match': 'many_row', 
                 'visible': 'status' in self.permit.changeable_fields(),},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '禁用', 'confirm_msg': '确认禁用？',
                 'pre_set': 'rt={status:0}', 'row_match': 'many_row', 
                 'visible': 'status' in self.permit.changeable_fields(),},
            ]
            return ops

class AjusttemplateForm(ModelFields):
    hide_fields=['operatetime','operateuser']
    class Meta:
        model = TbAdjusttemplate
        exclude =[]
        
    def dict_head(self, head):
        if head['name'] =='adjustsettings':
            head['editor']='com-field-table-list'
            head['fv_rule']='group_unique(Percent);express(scope.value!="[]")'
            head['fv_msg']='不能为空,且比值不能重复'
            head['table_heads']=[
                {'name':'Percent','label':'比值','editor':'com-table-pop-fields-local'},
                {'name':'AdjustValue','label':'调整值','editor':'com-table-span'}
            ]
            head['fields_heads']=[
                {'name':'Percent','label':'比值','editor':'com-field-number','fv_rule':'range(0.1~0.9)','required':True},
                {'name':'AdjustValue','label':'调整值','editor':'com-field-number','fv_rule':'range(0.01~0.5)','required':True}
            ]
        if head['name']=='minlimit':
            head['fv_rule']='range(0.1~0.9)'
        if head['name']=='maxlimit':
            head['fv_rule']='range(-0.9~-0.1)'
        return head
    
    def dict_row(self, inst):
        return {
            'operatetime':inst.operatetime.strftime('%Y-%m-%d %H:%M:%S') if inst.operatetime else ''
        }
    

class AdjustSettingProc(BaseFieldProc):
    def to_dict(self, inst, name):
        value = getattr(inst,name,'')
        if value:
            set_rows = json.loads(value)
            ls=['%(Percent)s  /  %(AdjustValue)s'%x for x in set_rows]
            return {
                name:value,
                '_adjustsettings_label':'<br />'.join(ls)
            }
        else:
            return {
                name:value,
            }

field_map.update({
    '%s.adjustsettings'%model_to_name(TbAdjusttemplate):AdjustSettingProc
})

director.update({
    'adjusttemplate':AdjusttemplatePage.tableCls,
    'adjusttemplate.edit':AjusttemplateForm
})

page_dc.update({
    'adjusttemplate':AdjusttemplatePage,
})