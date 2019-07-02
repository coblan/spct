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
            return ops

class AjusttemplateForm(ModelFields):
    hide_fields=['operatetime','operateuser']
    class Meta:
        model = TbAdjusttemplate
        exclude =[]
        
    def dict_head(self, head):
        if head['name'] =='adjustsettings':
            head['editor']='com-field-table-list'
            head['table_heads']=[
                {'name':'Percent','label':'百分比','editor':'com-table-pop-fields-local'},
                {'name':'AdjustValue','label':'调整值','editor':'com-table-span'}
            ]
            head['fields_heads']=[
                {'name':'Percent','label':'百分比','editor':'com-field-number','fv_rule':'range(0~1)'},
                {'name':'AdjustValue','label':'调整值','editor':'com-field-number','fv_rule':'range(0~1)'}
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