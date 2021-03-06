# encoding:utf-8

from maindb.models import TbAppresource
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
        fields_sort = ['id', 'name', 'valid', 'md5','type', 'remark']
        exclude = []

        def dict_head(self, head):
            dc = {
                'name': 150,
                'md5': 240,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def getExtraHead(self):
            return [{'name': 'valid', 'label': '有效', 'editor': 'com-table-bool-shower'}]

        def get_operation(self):
            return ModelTable.get_operation(self)[0:1]

        def dict_row(self, inst):
            return {
                'valid': not bool(inst.isexpired)
            }


class AppResourceForm(ModelFields):
    hide_fields = ['md5', 'isexpired' ]

    class Meta:
        model = TbAppresource
        exclude = []

    def dict_row(self, inst): 
        return {
                'valid': not bool(inst.isexpired)
            }
    
    def getExtraHeads(self): 
        return [
            {'name': 'valid','label': '有效','editor': 'bool',}
        ]
    
    def clean_dict(self, dc):
        super().clean_dict(dc)
        url = dc.get('url')
        if url:
            ls = url.split('/')
            name = ls[-1]
            md5 = name[:32]
            dc['md5'] = md5
        dc['isexpired'] = False if dc.get('valid') else True
            
        return dc
    
    
    


director.update({
    'AppResource': AppResource.tableCls,
    'AppResource.edit': AppResourceForm,
})
page_dc.update({
    'app_resource': AppResource,

})
