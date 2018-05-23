# encoding:utf-8

from ..models import TbAppresource
from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, ModelFields

class AppResource(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return 'App资源管理'
    
    class tableCls(ModelTable):
        pop_edit_field = 'name'
        hide_fields = ['url']
        model = TbAppresource
        exclude = []

class AppResourceForm(ModelFields):
    class Meta:
        model = TbAppresource
        exclude = []
        
director.update({
    'AppResource': AppResource.tableCls,
    'AppResource.edit': AppResourceForm,
})
page_dc.update({
    'AppResource': AppResource,
    
})