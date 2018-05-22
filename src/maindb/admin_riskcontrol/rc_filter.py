# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc,RowSort,RowFilter,model_dc,ModelFields,director
from ..models import TbRcFilter

class RcFilterPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return _('Main.TbRcFilter')
    
    class tableCls(ModelTable):
        model = TbRcFilter
        exclude=['rc_rule_id']
        #fields_sort=['rc_level','rc_rule','rc_rule_name','rc_filter','rc_active','']
        
        def dict_head(self, head):
            
            if head['name'] in ['rc_filter','rc_days']:
                head['editor'] = 'com-table-linetext'
            if head['name'] == 'rc_active':
                head['editor'] = 'com-table-checkbox'
                
            dc={
                'rc_level':60,
                'rc_rule':80,
                'rc_rule_name':70,
                'rc_filter':60,
                'rc_active':60,
                'rc_days':80,
                'description': 200,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])   
                
            return head
        def dict_row(self, inst):
            return {
                'rc_active': inst.rc_active ==1
            }
        
        class filters(RowFilter):
            names=['rc_level']

class RcFilterForm(ModelFields):
    class Meta:
        model=TbRcFilter
        exclude = []
        
    def clean_dict(self, dc):
        if dc.get('rc_active'):
            dc['rc_active']=1
        else:
            dc['rc_active']=0
        return dc
    

model_dc[TbRcFilter]={'fields':RcFilterForm}

director.update({
    'risk.filter':RcFilterPage.tableCls,
    'risk.filter.edit':RcFilterForm
})

page_dc.update({
    'maindb.TbRcFilter':RcFilterPage
})
