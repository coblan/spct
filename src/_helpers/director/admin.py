# encoding:utf-8
from __future__ import unicode_literals

from .base_data import model_dc,page_dc,permit_list
from .fields.fieldspage import FieldsPage
from .fields.fields import ModelFields

from .table.tablepage import TablePage
from .table.tabpage import TabPage
from .table.table import ModelTable,RowFilter,RowSort

from django.contrib.auth.models import Group,User
from django.conf import settings
from django import forms

import json


from .models import PermitModel 

from .access.assem_group import AssemGroupPage
from .model_func.dictfy import to_dict,model_to_name

from django.utils.translation import ugettext as _
from .access.permit import permit_to_text
import ajax
from .fields.delpage import DelPage
from .log.logpage import LogPage
from .base_data import page_dc

page_dc.update({
    'del_rows':DelPage,
        'log':LogPage,
} )

class UserGroupTable(ModelTable):
    
    class GroupFilter(RowFilter):
        names=['prefix']
        
        def get_query(self, query):
            prefix=self.filter_args.get('prefix',None)
            search_kwords={}
            if prefix:
                search_kwords['name__startswith']=prefix
            return query.filter(**search_kwords)
        
    filters=GroupFilter
    
    model=Group
    include=['name']
    
    def inn_filter(self, query):
        return query.order_by('name')
    
    def get_heads(self):
        heads = super(self.__class__,self).get_heads()
        heads.append({'name':'users','label':'包含用户'})
        return heads
    
    def dict_row(self, inst):
        dc={
            'permit':[to_dict(x) for x in inst.permitmodel_set.all()],
            'users':[to_dict(u,include=['first_name','username']) for u in inst.user_set.all()]
        }
        
        # if hasattr(inst,'permitmodel'):
            # if inst.permitmodel.permit:
                # permit_dc = json.loads(inst.permitmodel.permit)
                # if isinstance(permit_dc,list):
                    # gp = Group.objects.filter(pk__in=permit_dc)
                    # dc= {
                        # 'permit':[to_dict(x) for x in gp]
                    # }

        return dc
        

class UserGroupFields(ModelFields):
    #template='user_admin/permit.html'
    class Meta:
        model=Group
        fields=['name',]
        
    # def get_context(self):
        # ctx = super(UserGroupFields,self).get_context()
        # group = self.instance
        # if hasattr(group,'permitmodel') and group.permitmodel.permit:
            # ctx['permits']=json.loads(group.permitmodel.permit) #[{'model':x.model,'permit': json.loads(x.permit)} for x in self.instance.per.all()]
        # else:
            # ctx['permits']={}
        # ctx['permit_heads']=self.permit.get_heads()
        # return ctx

class GroupFormPage(FieldsPage):
    template='authuser/permit_group_form.html'
    class GroupForm(ModelFields):
        class Meta:
            model=Group
            fields=['name']
        def get_heads(self):
            heads= super(self.__class__,self).get_heads()
            heads.append({
                'name':'permit',
                'editor':'tow_col',
                'label':'权限选择',
                'options':[{'value':x.pk,'label':unicode(x)} for x in PermitModel.objects.all()]
            })
            return heads
        
        def get_row(self):
            row=super(self.__class__,self).get_row()
            if self.instance.pk:
                row['permit']=[x.pk for x in self.instance.permitmodel_set.all()]
            else:
                row['permit']=[]
            return row
        
        def save_form(self):
            super(self.__class__,self).save_form()
            if self.kw.get('permit',None):
                permits=PermitModel.objects.filter(pk__in=self.kw.get('permit'))
                self.instance.permitmodel_set.add(*list(permits))
            else:
                self.instance.permitmodel_set.clear()
                # self.instance.save()
    fieldsCls=GroupForm
            
        

class GroupTablePage(TablePage):
    template='authuser/group_table.html'
    tableCls=UserGroupTable

class GroupAssemPage(TablePage):
    tableCls=UserGroupTable
    template='authuser/permit_group.html'
    
class PermitPage(TablePage):
    class PermitSort(RowSort):
        names=['name']
        chinese_words=['name']
        # def get_query(self, query):
            # if self.sort_str:
                # ls=self.sort_str.replace('name','converted').split(',')
                # ls=self.sort_str.split(',')
                # if 'name' in ls:
                    # query= query.extra(select={'converted': 'CONVERT(name USING gbk)'},order_by=['converted'])
                    
                # return query.order_by(*ls)
            # else:
                # return query
            
           
            
        
    class PermitTable(ModelTable):
        model=PermitModel
        exclude=['group']
    
        def dict_row(self, inst):
            return {'permit' :permit_to_text( inst.permit)}
            
    PermitTable.sort=PermitSort
    tableCls=PermitTable
    template='authuser/permit_table.html'
    

class GroupGroup(TabPage):
    tabs=[{'name':'assem','label':'用户权限组','page_cls':GroupAssemPage,'suffix':''},
          {'name':'prim','label':'可用权限','page_cls':PermitPage,'suffix':''},
          ]
    def __init__(self, request):
        super(self.__class__,self).__init__(request)
        

class PermitFormPage(FieldsPage):
    class PermitForm(ModelFields):
        class Meta:
            model=PermitModel
            exclude=[]
        
        def get_context(self):
            ctx = super(self.__class__,self).get_context()
            # ctx['permits']=self.instance.permit
            
            # group = self.instance
            # if hasattr(group,'permitmodel') and group.permitmodel.permit:
                # ctx['permits']=json.loads(group.permitmodel.permit) #[{'model':x.model,'permit': json.loads(x.permit)} for x in self.instance.per.all()]
            # else:
                # ctx['permits']={}
            ctx['permit_heads']=self.permit.get_heads()

            return ctx
        def clean_name(self):
            name = self.cleaned_data.get('name')
            if 'name' in self.changed_data and PermitModel.objects.filter(name=name).exists():
                raise forms.ValidationError(_('permit name has been exist'))
            else:
                return name
        def clean_permit(self):
            permit= self.cleaned_data.get('permit')
            dc={}
            for perm in permit_list:
                if isinstance(perm,dict):
                    dc[perm['name']]=perm
                else:
                    dc[model_to_name(perm)]=perm
             
            out_permit={}
            for k,v in permit.items():
                permit_content=dc.get(k,None)
                if not permit_content:
                    continue
                if isinstance(permit_content,dict):
                    names_permit=map(lambda x :x['name'],permit_content['fields'])
                    out_permit[k]=[x for x in v if x in names_permit]
                else:
                    fields_cls = model_dc.get(permit_content).get('fields')
                    fields = fields_cls(crt_user=self.crt_user,nolimit=True).fields
                    names = fields.keys()
                    names_permit=[x+'__read' for x in names]
                    names_permit.extend([x+'__write' for x in names])
                    names_permit.extend(['can__log','can__create','can__delete'])
                    out_permit[k]=[x for x in v if x in names_permit]
            return out_permit
            #for 
            #for head in heads:
                #if 
            
            
    template='authuser/permit_form.html'
    fieldsCls=PermitForm
    ajax_scope=ajax.get_global()
    
class UserFields(ModelFields):
    class Meta:
        model=User
        fields=['username','first_name','is_active','is_staff','is_superuser','email','groups']
        
    def dict_head(self, head):
        if head['name']=='groups':
            head['editor']='field_multi_chosen'
        return head

class UserTable(ModelTable):
    model=User
    include=['username','groups','first_name','is_active','is_staff','is_superuser','email',]
    
    def get_heads(self):
        heads=super(UserTable,self).get_heads()
        for head in heads:
            if head['name']=='username':
                head['label']='账号'
        return heads
    
    #def get_rows(self):
        #rows=super(UserTable,self).get_rows()
        #for row in rows:
            #row['groups']=[group.name for group in Group.objects.filter(pk__in=row.get('groups'))]
        #return rows
    
    def dict_row(self, inst):
        return {
            'groups':';'.join([g.name for g in inst.groups.all()])
        }
        

class UserTablePage(TablePage):
    #template='authuser/user_table.html'
    tableCls=UserTable

class UserFormPage(FieldsPage):
    template='authuser/user_form.html'
    fieldsCls=UserFields

model_dc[Group]={'fields':GroupFormPage.GroupForm}
model_dc[User]={'fields':UserFields}
model_dc[PermitModel]={'fields':PermitFormPage.PermitForm}


page_dc.update({'user':UserTablePage,
                'user.edit':UserFormPage,
                'group':GroupTablePage,
                'group.edit':GroupFormPage,
                
                'permit.edit':PermitFormPage,
                # 'group.assem.edit':AssemGroupPage,
                
                'group_human':GroupGroup,
                'group_human.edit':AssemGroupPage})

permit_list.append(Group)
permit_list.append(User)
permit_list.append({'name':'myauth','label':'账号管理','fields':[
    {'name':'modify_other_pswd','label':'修改所有人密码','type':'bool'},]
})

