# encoding:utf-8

from ..models import TbAppresource
from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, ModelFields
import re
class AppResource(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return 'App资源管理'
    
    class tableCls(ModelTable):
        pop_edit_field = 'name'
        hide_fields = ['url']
        model = TbAppresource
        exclude = []
        
        def dict_head(self, head): 
            dc={
                'md5':150,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head

class AppResourceForm(ModelFields):
    hide_fields = ['md5']
    class Meta:
        model = TbAppresource
        exclude = []
    
    def clean_dict(self, dc): 
        super().clean_dict(dc)
        url =  dc.get('url')
        if url:
            ls = url.split('/')
            name = ls[-1]
            md5 = name[:32]
            dc['md5'] = md5
        
        return dc
        
    #def save_form(self): 
        #super().save_form()
        #if self.kw.url:
            #pass
        
        
        
director.update({
    'AppResource': AppResource.tableCls,
    'AppResource.edit': AppResourceForm,
})
page_dc.update({
    'AppResource': AppResource,
    
})