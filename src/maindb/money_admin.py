# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter
from helpers.director.model_func.dictfy import model_to_name
from .models import TbBalancelog,TbTrans,TbChannel
from .status_code import *

class BalancelogPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return '账目记录'
    
    class tableCls(ModelTable):
        model = TbBalancelog
        include = ['account','categoryid','beforeamount','amount','afteramount','memo','createtime','creater']
        
        #fields_sort=['accountid','account','accounttype','username']

        #def dict_row(self, inst):
            #account_type = dict(ACCOUNT_TYPE)
            #return {
                #'amount':unicode(inst.amount),
                #'accounttype': account_type.get(inst.accounttype)
            #}
        def dict_head(self, head):
            dc={
                'account':80,
                'categoryid':60,
                'beforeamount':120,
                'amount':120,
                'afteramount':120,
                'memo':250,
                'createtime':160,
                'creater':150
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head
        def get_operation(self):
            return []
        
        class filters(RowFilter):
            names=['categoryid']
            range_fields=['createtime']
        class search(RowSearch):
            names=['creater']
        class sort(RowSort):
            names=['createtime']
            

class TransPage(TablePage):
    template='jb_admin/table.html'
    class tableCls(ModelTable):
        model = TbTrans
        include=['account','channelid','amount','realamount','fee','status','createtime','exectime']
        def dict_head(self, head):
            dc={
                'account':80,
                'channelid':100,
                'amount':100,
                'realamount':100,
                'fee':100,
                'status':80,
                'createtime':150,
                'exectime':150
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head
        
        def get_operation(self):
            return []
        
        def dict_row(self, inst):
            channel = TbChannel.objects.get(pk=inst.channelid)
            return {
                'channelid':unicode(channel)
            }
        class filters(RowFilter):
            names=['channelid']
            range_fields=['createtime']
            
            def get_options(self, name):
                if name =='channelid':
                    return [{'value':x.channelid,'label':unicode(x)} for x in TbChannel.objects.all()]
                else:
                    return RowFilter.get_options(name)
            
        class sort(RowSort):
            names=['tranid'] 
            
    def get_label(self):
        return '存款记录'
        
class ChannelPage(TablePage):
    template='jb_admin/table.html'
    class tableCls(ModelTable):
        model = TbChannel
        exclude = []
        fields_sort=['channel','channelname','channelgroup','cashflow','returntype',
                     'maxlimit','minlimit','grouptitle','btnname','status']
        
        def dict_head(self, head):
            dc={
                'channel':80,
                'channelname':80,
                'channelgroup':80,
                'cashflow':80,
                'returntype':80,
                'maxlimit':80,
                'minlimit':80,
                'grouptitle':80,
                'btnname':80,
                'status':80,
              
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head        
        
        def get_operation(self):
            return []
        
        #class filters(RowFilter):
            #names=['channel','channelname','returntype']
        #class search(RowSearch):
            #names=['channel']
        class sort(RowSort):
            names=['channel','returntype']
    
    class fieldsCls(ModelFields):
        class Meta:
            model = TbChannel
            exclude=[]
    
    def get_context(self):
        ctx = TablePage.get_context(self)
        ctx['fields_heads']=self.fieldsCls(crt_user=self.crt_user).get_heads()
        ctx['model_class']= model_to_name(TbChannel)
        return ctx
    def get_label(self):
        return '金流渠道'

model_dc[TbChannel]={'fields':ChannelPage.fieldsCls}
                    