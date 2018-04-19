# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group,User
from helpers.director.shortcut import TablePage,ModelTable,page_dc,model_dc
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
        exclude=[]

    #def dict_head(self, head):
        
        #if head['name']=='username':
            #UserForm = model_dc[User].get('fields')
            #userform = UserForm(crt_user=self.crt_user)
            #head['editor']='com-table-pop-fields'
            #head['get_row']={
                #"fun":'use_table_row'
            #}
            #head['fields_heads']=userform.get_heads()
            #head['after_save']={
                #'fun':'do_nothing'
                ##'fun':'update_or_insert'
            #}     
            #head['ops']=userform.get_operations()
        #return head

page_dc.update({
    'jb_user':UserPage,
    'jb_group':GroupPage
})