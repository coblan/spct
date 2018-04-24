# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group,User
from helpers.director.shortcut import TablePage,ModelTable,page_dc,model_dc,ModelFields
from helpers.director.models import PermitModel 
import re
# Register your models here.
class UserPage(TablePage):
    template='jb_admin/table.html'
    class tableCls(ModelTable):
        model = User
        exclude=['password']
        
        def dict_head(self, head):
            
            if head['name']=='username':
                UserForm = model_dc[User].get('fields')
                userform = UserForm(crt_user=self.crt_user)
                head['editor']='com-table-pop-fields'
                head['get_row']={
                    "fun":'use_table_row'
                }
                head['fields_heads']=userform.get_heads()
                head['after_save']={
                    'fun':'do_nothing'
                    #'fun':'update_or_insert'
                }     
                head['ops']=userform.get_operations()
            return head
        



class GroupPage(TablePage):
    template='jb_admin/table.html'
   
    class tableCls(ModelTable):
        model=Group
        exclude=['permissions']
    
    
        def dict_head(self, head):
            
            if head['name']=='name':
                groupform = GroupForm(crt_user=self.crt_user)
                head['editor']='com-table-pop-fields'
                head['get_row']={
                    "fun":'use_table_row'
                }
                head['fields_heads']=groupform.get_heads()
                head['after_save']={
                    'fun':'do_nothing'
                    #'fun':'update_or_insert'
                }     
                head['ops']=groupform.get_operations()

            #if head['name']=='permissions':
                #head['editor'] = 'com-field-ele-tree-name-layer'
                
            return head
    
        def dict_row(self, inst):
            dc ={}
            if inst.pk:
                dc['permit']=[x.pk for x in inst.permitmodel_set.all()]
            else:
                dc['permit']=[]
            return dc
        
        def get_operation(self):
            opt = ModelTable.get_operation(self)
            for k in opt:
                if k['name'] == 'add_new':
                    fieldobj= GroupForm(crt_user=self.crt_user)
                    k['heads']=fieldobj.get_heads()
                    k['ops']= fieldobj.get_operations()     
            return opt        
        


class GroupForm(ModelFields):
    class Meta:
        model=Group
        fields=['name']
    
    #def dict_head(self, head):
        #if head['name']=='permissions':
            #head['editor'] = 'com-field-ele-tree-name-layer'   
        #return head
    
    def get_heads(self):
        heads= super(self.__class__,self).get_heads()
        options = [{'value':x.pk,'label':unicode(x)} for x in PermitModel.objects.all()]
        options = list2tree(options)
        heads.append({
            'name':'permit',
            'editor':'com-field-ele-tree-name-layer',
            'label':'权限选择',
            'options':options
        })
        return heads    
    
    def get_row(self):
        row=super(self.__class__,self).get_row()
        if self.instance.pk:
            row['permit']=[x.pk for x in self.instance.permitmodel_set.all()]
        else:
            row['permit']=[]
        return row    

def list2tree(ls):
    clsfy = {}
    for i in ls:
        lb = i['label']
        mt = re.search('(.+)\.(.+)',lb)
        if mt:
            prefix,suffix = mt.group(1),mt.group(2)
            i['label'] = suffix
            if not clsfy.get(prefix):
                clsfy[prefix] =[]
            clsfy[prefix].append(i)
        else:
            clsfy[lb]= i 
    outer =[]
    for k,v in clsfy.items():
        
        if isinstance(v,list):
            dc = {'label':k,
                  'children':v}
        else:
            dc=v
        
        outer.append(dc)
    return outer
                

page_dc.update({
    'jb_user':UserPage,
    'jb_group':GroupPage
})