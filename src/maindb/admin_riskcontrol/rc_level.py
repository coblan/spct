# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc,RowSort,RowFilter,model_dc,ModelFields,director
from ..models import TbRcLevel

class RcLevelPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return _('Main.TbRcLevel')
    
    class tableCls(ModelTable):
        model = TbRcLevel
        exclude=['rc_level_id']

        def dict_head(self, head):
            dc={
                'rc_level_name':160,
                'rc_level_type': 120,
             
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])   
                
            if head['name'] in ['rc_level_filter']:
                head['editor'] = 'com-table-linetext'

            return head
        
        class filters(RowFilter):
            names=['rc_level']

class RcLevelForm(ModelFields):
    class Meta:
        model=TbRcLevel
        exclude = []
        
    #def clean_dict(self, dc):
        #if dc.get('rc_active'):
            #dc['rc_active']=1
        #else:
            #dc['rc_active']=0
        #return dc

#model_dc[TbRcLevel]={'fields':RcLevelForm}

director.update({
    'risk.RcLevelPage':RcLevelPage.tableCls,
    'risk.RcLevelPage.edit':RcLevelForm,
})
page_dc.update({
    'maindb.TbRcLevel':RcLevelPage
})
