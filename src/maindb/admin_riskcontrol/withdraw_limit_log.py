# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc,RowSort,RowFilter,model_dc,ModelFields
from ..models import TbWithdrawlimitlog

class TbWithdrawlimitlogPage(TablePage):
    template='maindb/table.html'
    def get_label(self):
        return _('Main.TbWithdrawlimitlog')
    
    class tableCls(ModelTable):
        model = TbWithdrawlimitlog
        exclude=[]
        #fields_sort=['accounttype','account','rc_level']

        #def dict_head(self, head):
            #if head['name'] in ['rc_level_filter']:
                #head['editor'] = 'com-table-linetext'

            #return head
        
        class filters(RowFilter):
            names=['categoryid']
            range_fields=['createtime']


page_dc.update({
    'maindb.TbWithdrawlimitlog':TbWithdrawlimitlogPage
})
