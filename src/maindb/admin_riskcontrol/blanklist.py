# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc,RowSort,RowFilter,model_dc,ModelFields,RowSearch,director
from ..models import TbBlackuserlist,TbBlackuserlistLog,Blackiplist,Blackiprangelist,\
     Whiteiplist,Whiteuserlist,TbAccount

class TbBlackuserlistPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return _('Main.TbBlackuserlist')
    
    class tableCls(ModelTable):
        model = TbBlackuserlist
        exclude=[]

class TbBlackuserlistLogPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return _('Main.TbBlackuserlistLog')
    
    class tableCls(ModelTable):
        model = TbBlackuserlistLog
        exclude=[]
        
#class BlankiplistPage(TablePage):
    #template='jb_admin/table.html'
    #class tableCls(ModelTable):
        #model=Blackiplist
        #exclude=[]

class BlankipRangeListPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return 'IP黑名单(范围)'
    
    class tableCls(ModelTable):
        model=Blackiprangelist
        exclude=[]
        pop_edit_field='blackiprangelistid'
        

class WhiteIpListPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return 'IP白名单'
    
    class tableCls(ModelTable):
        model = Whiteiplist
        exclude=[]
        pop_edit_field='whiteiplistid'

class WhiteuserlistPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return '用户白名单'
    
    class tableCls(ModelTable):
        model=Whiteuserlist
        exclude=['username','addtime']
    
        pop_edit_field='whiteuserlistid'

class BlankipRangeListForm(ModelFields):
    class Meta:
        model=Blackiprangelist
        exclude=[]
        
    def dict_head(self, head):
        if head['name'] in ['startip','endip']:
            head['fv_rule']='ip'
        if head['name'] in ['startipnum','endipnum']:
            head['readonly'] = True
        return head
    
    def clean_dict(self, dc):
        if dc.get('startip'):
            dc['startipnum']=ip2num(dc.get('startip'))
        else:
            dc['startipnum']=0
    
        if dc.get('endip'):
            dc['endipnum']=ip2num(dc.get('endip'))
        else:
            dc['endipnum']=0  
        return dc
            
class WhiteIpListForm(ModelFields):
    class Meta:
        model = Whiteiplist
        exclude = []
    def dict_head(self, head):
        if head['name']=='ip':
            head['fv_rule']='ip'
        return head

class WhiteuserlistForm(ModelFields):
    class Meta:
        model=Whiteuserlist
        exclude = ['username','addtime']
    
    def dict_head(self, head):
        if head['name'] =='account':
            table_obj = AccountSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
        return head
            

class AccountSelect(ModelTable):
    model = TbAccount
    include=['accountid','account']
    def dict_head(self, head):
        if head['name']=='accountid':
            head['editor']='com-table-foreign-click-select'
        return head
    
    class search(RowSearch):
        names=['account']

def ip2num(ip):
    arr=ip.split('.')
    num = 256 * 256 * 256 * long(arr[0]) + 256 * 256 * long(arr[1]) + 256 * long(arr[2]) +long(arr[3])
    return num

#model_dc[Blackiprangelist]={'fields':BlankipRangeListForm}
#model_dc[Whiteiplist]={'fields':WhiteIpListForm}
#model_dc[Whiteuserlist]={'fields':WhiteuserlistForm}

director.update({
    'risk.TbBlackuserlistPage':TbBlackuserlistPage.tableCls,
    'risk.TbBlackuserlistLogPage':TbBlackuserlistLogPage.tableCls,
 
    'risk.WhiteIpListPage':WhiteIpListPage.tableCls,
    'risk.WhiteIpListPage.edit':WhiteIpListForm,
    
    'risk.WhiteuserlistPage':WhiteuserlistPage.tableCls,
    'risk.WhiteuserlistPage.edit':WhiteuserlistForm,
    'risk.AccountSelect':AccountSelect,
    
    'risk.BlankipRangeListPage':BlankipRangeListPage.tableCls,
    'risk.BlankipRangeListPage.edit':BlankipRangeListForm
    
    
})

page_dc.update({
    'maindb.TbBlackuserlist':TbBlackuserlistPage,
    'maindb.TbBlackuserlistLog':TbBlackuserlistLogPage,
    
    #'maindb.Blackiplist':BlankiplistPage,
    'maindb.BlankipRangeList':BlankipRangeListPage,
    'maindb.WhiteIpList':WhiteIpListPage,
    'maindb.Whiteuserlist':WhiteuserlistPage,
})
