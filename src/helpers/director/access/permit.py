# encoding:utf-8
"""
>>>director/permit.rst>
=========
permit
=========

添加权限
========
添加特殊权限::

    permit_list.append({'name':'workload','label':'人员负荷','fields':[
        {'name':'view_all_task','label':'查看所有负荷','type':'bool'},
        {'name':'sp2','label':'工作统计','type':'bool'}
    ]})

添加数据库表权限::

    permit_list.append(WorkModel)

判断权限
========
判断特殊权限::

    has_permit(user,'view_all_task')

判断数据库表权限::

    Permit(model,user).changeable_fields() ...

<<<<
"""

from __future__ import unicode_literals
from ..model_func.dictfy import model_to_name
from django.apps import apps
import json
from django.db import models
from ..base_data import model_dc,permit_list

def has_permit(user,name):
    """
    special.sp1
    """
    cls,perm=name.split('.')
    if user.is_superuser:
        if perm.startswith('-'):
            return False
        else:
            return True  
        
    for permit_dc in user_permit_dc(user):
        sp_permit_list= permit_dc.get(cls,[])
        if perm in sp_permit_list:
            return True        
    #for group in user.groups.all():
            #if hasattr(group,'permitmodel'):
                #permit_dc = json.loads( group.permitmodel.permit )
                #sp_permit_list= permit_dc.get(cls,[])
                #if perm in sp_permit_list:
                    #return True
    return False


def user_permit_dc(user):
    for group in user.groups.all():
        for permit_dc in group_permit(group):
            yield permit_dc

def group_permit(group):
    for permit in group.permitmodel_set.all():
        yield permit.permit

def group_has_permit(group,name):
    """
    判断一个组是否具备name权限。
    @name:package.permit_name
    """
    cls,perm=name.split('.')
    for permit_dc in group_permit(group):
        sp_permit_list= permit_dc.get(cls,[])
        if perm in sp_permit_list:
            return True   
    return False




class ModelPermit(object):
    """
    以json的形式存储于permitModel数据库
    
    [{'model':'app.App',}]
    
    @nolimit ,有时需要跨越 权限，操作某个数据表，就加上 nolimit=True
    """
    def __init__(self,model,user=None,nolimit=False):
        self.user=user
        if isinstance(model,(str,unicode)):
            model=apps.get_model(model)
        elif isinstance(model,models.Model):
            model=model.__class__
        self.model = model
        self.permit_list=[]
        self.nolimit=nolimit
        
        self._read_perm_from_db()
    
    def _read_perm_from_db(self):
        model_name = model_to_name(self.model)

        if not self.user:
            self.permit_list=[]
            return
        # 每次请求，大概率上，会获取permit_dc很多次，所以这里缓存在user上，减少读取数据库
        if not hasattr(self.user,'permit_dc_list'):
            self.user.permit_dc_list=list(user_permit_dc(self.user))
        for permit_dc in self.user.permit_dc_list:
            permit= permit_dc.get(model_name,[])
            self.permit_list.extend(permit)            
        #for group in self.user.groups.all():
            #if hasattr(group,'permitmodel'):
                #permits = json.loads( group.permitmodel.permit )
                #permit= permits.get(model_name,[])
                #self.permit_list.extend(permit)
        self.permit_list=list(set(self.permit_list))
            #setattr(self.user,'_permit_list.%s'%model_name,self.permit_list)
    
    def get_heads(self):
        """
        这个函数好像只被 group admin 用了下,返回所有注册了的model的权限备选head信息。
        """
        ls=[]
        for v in permit_list:
            if not isinstance(v,dict) and issubclass(v,models.Model):

                ls.append({'name':model_to_name(v),
                           'label': unicode(v._meta.verbose_name),
                           # 'label': v._meta.app_label+'.'+ unicode(v._meta.verbose_name), # 因为翻译的缘故，有时是 __proxy__函数，所以必须 unicode处理一下
                           'type':'model',
                           'fields':model_permit_info(v,self.user)})
        
        for v in permit_list:
            if isinstance(v,dict):
                ls.append(v)
        return ls
    
    def get_rows(self):
        pass
    
    def can_add(self):
        if self.nolimit or self.user.is_superuser:
            return True
        else:
            return 'can__create' in self.permit_list

    def can_del(self):
        if self.nolimit or self.user.is_superuser:
            return True
        else:
            return 'can__delete' in self.permit_list
    def can_log(self):
        if self.nolimit or self.user.is_superuser:
            return True
        else:
            return 'can__log' in self.permit_list        
    
    def can_access(self):
        if self.nolimit or self.user.is_superuser:
            return True
        elif self.readable_fields() or self.changeable_fields():
            return True
        else:
            return False

    def readonly_fields(self):
        if self.nolimit or self.user.is_superuser:
            return []
        else:
            return [x for x in self.readable_fields() if x not in self.changeable_fields()]
    
    def all_fields(self):
        ls=[]
        for field in self.model._meta.get_fields():
            if isinstance(field,models.Field):
                ls.append(field.name)   
        return ls
    
    def readable_fields(self):
        if self.nolimit or self.user.is_superuser:
            return self.all_fields()
        else:
            ls=[]
            for perm in self.permit_list:
                if perm.endswith('__read'):
                    ls.append(perm[0:-6])
            return list(set(ls))  
    
    def changeable_fields(self):
        if self.nolimit or self.user.is_superuser:
            return self.all_fields()
            #return self.model._meta.get_all_field_names()
        else:
            ls = []
            for perm in self.permit_list:
                if perm.endswith('__write'):
                    ls.append(perm[0:-7])
            return list(set(ls))



def model_permit_info(model,user):
    """
    返回model权限字段，现在应该是用来拼凑前端页面。该页面用于编辑用户的权限。
    
    [{u'name': u'task', u'label': u'\u6240\u5c5e\u4efb\u52a1'},]
    """

    fields_cls = model_dc.get(model).get('fields')
    fields_dc = fields_cls(crt_user=user).fields
    
    for field in model._meta.fields:
        if getattr(field,'auto_now',False):
            fields_dc[field.name]=field.verbose_name  
    ls= [] #[{'name':'id','label':'ID'}]
    for k,v in fields_dc.items():
        if isinstance(v,(str,unicode)):
            label=v
        elif hasattr(v.label,'title') and callable(v.label.title):
            label=v.label.title()
        else:
            label=v.label
        ls.append({'name':k,'label':label})
    return ls


def permit_to_text(permit):
    """
    把permit字典转换为人能够读的文字表述。现在用于显示在前端页面上。
    @permit:
    """
    out_dc={}
    model_dc={}
    sp_dc={}
    for k in permit_list:
        if isinstance(k,dict):
            sp_dc[k['name']]=k
        else:
            model_dc[model_to_name(k)]=k
            
            
    for k,v in permit.items():
        if k in model_dc:
            model = model_dc[k]
            dc = _get_model_permit_text(model,v)
        elif k in sp_dc:
            sp=sp_dc[k]
            dc = _get_sp_permit_text(sp,v)
        else:
            dc={}
        out_dc.update(dc)
    return out_dc

def _get_model_permit_text(model,v):
    key=unicode( model._meta.verbose_name )
    value=""
    value_list=[]
    if "can__log" in v:
        value_list.append("查看日志")
    if "can__create" in v:
        value_list.append("创建")
    if "can__delete" in v:
        value_list.append("删除")
    for field in model._meta.fields:
        name = field.name
        op=[]
        if "%s__read"%name in v:
            op.append('读')
        if "%s__write"%name in v:
            op.append("写")
        if op:
            op_str='/'.join(op)
            value_list.append("%s(%s)"%( unicode(field.verbose_name),op_str))
    if value_list:
        value=','.join(value_list)
    return {key:value}
        

def _get_sp_permit_text(sp,v):
    key=sp['label']
    value_list=[]
    for field in sp['fields']:
        if field['name'] in v:
            value_list.append(field['label'])
    return {key:','.join(value_list)}
    