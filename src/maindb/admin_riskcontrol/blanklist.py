# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc,RowSort,RowFilter,model_dc,ModelFields
from ..models import TbBlackuserlist,TbBlackuserlistLog

class TbBlackuserlistPage(TablePage):
    template='maindb/table.html'
    def get_label(self):
        return _('Main.TbBlackuserlist')
    
    class tableCls(ModelTable):
        model = TbBlackuserlist
        exclude=[]

class TbBlackuserlistLogPage(TablePage):
    template='maindb/table.html'
    def get_label(self):
        return _('Main.TbBlackuserlistLog')
    
    class tableCls(ModelTable):
        model = TbBlackuserlistLog
        exclude=[]
        
page_dc.update({
    'maindb.TbBlackuserlist':TbBlackuserlistPage,
    'maindb.TbBlackuserlistLog':TbBlackuserlistLogPage
})
