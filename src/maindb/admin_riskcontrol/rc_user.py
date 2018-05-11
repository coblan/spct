# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc,RowSort,RowFilter,model_dc,ModelFields,director
from ..models import TbRcUser

class RcUserPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return _('Main.TbRcUser')
    
    class tableCls(ModelTable):
        model = TbRcUser
        exclude=[]
        fields_sort=['accounttype','account','rc_level']

        #def dict_head(self, head):
            #if head['name'] in ['rc_level_filter']:
                #head['editor'] = 'com-table-linetext'

            #return head
        
        class filters(RowFilter):
            names=['rc_level']

director.update({
    'risk.RcUserPage':RcUserPage.tableCls,
    
})
page_dc.update({
    'maindb.TbRcUser':RcUserPage
})
