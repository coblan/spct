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
        
        def dict_head(self, head): 
            dc={
                'blackuserlistid':120,
                'accounttype':100,
                'ban_status':100,
         
              
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head

class TbBlackuserlistLogPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return _('Main.TbBlackuserlistLog')
    
    class tableCls(ModelTable):
        model = TbBlackuserlistLog
        exclude=[]
        
        def dict_head(self, head): 
            dc={
                'blacklogid':100,
                'before_ban_status':130,
                'alter_ban_status':120,
                'modify_user': 120,
         
              
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head        
        
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
        hide_fields = ['startipnum', 'endipnum']
        pop_edit_field='blackiprangelistid'
    
        def dict_head(self, head): 
            dc={
                'startip':100,
                'endip':100,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head          

class WhiteIpListPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return 'IP白名单'
    
    class tableCls(ModelTable):
        model = Whiteiplist
        exclude=['itype']
        pop_edit_field='whiteiplistid'

        def dict_head(self, head): 
            dc={
                'whiteiplistid':120,
                'ip': 120,
                'remark': 150,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head 

class WhiteuserlistPage(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return '用户白名单'
    
    class tableCls(ModelTable):
        model=Whiteuserlist
        exclude=['username','addtime', 'itype']
    
        pop_edit_field='whiteuserlistid'

class BlankipRangeListForm(ModelFields):
    #hide_fields = ['startipnum', '']
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
        super().clean_dict(dc)
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
    include=['accountid','username']
    def dict_head(self, head):
        dc={
               'accountid':100,
               'username': 150,
      
           }
        if dc.get(head['name']):
            head['width'] =dc.get(head['name'])
            
        if head['name']=='accountid':
            head['editor']='com-table-foreign-click-select'
        return head
    
    class search(RowSearch):
        names=['accountid', 'username']

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
