# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter
from .models import TbTicketmaster
from .status_code import *

class TicketMasterPage(TablePage):
    template='maindb/table_plain.html'
    class tableCls(ModelTable):
        model = TbTicketmaster
        exclude = []
        #fields_sort=['accountid','account','accounttype','username']

        #def dict_row(self, inst):
            #account_type = dict(ACCOUNT_TYPE)
            #return {
                #'amount':unicode(inst.amount),
                #'accounttype': account_type.get(inst.accounttype)
            #}
        class filters(RowFilter):
            range_fields=[{'name':'createtime','type':'date'},
                          {'name':'settletime','type':'date'}]