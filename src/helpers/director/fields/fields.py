# encoding:utf-8
from __future__ import unicode_literals
from django import forms
from ..model_func.dictfy import form_to_head,to_dict,delete_related_query,model_to_name,from_dict,name_to_model,field_map
from django.http import Http404
import json
from django.db import models
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from ..base_data import model_dc
import base64
from django.db import models
from ..access.permit import ModelPermit
from ..models import LogModel

#def save_row(row,user,request):
    #for k in row: # convert model instance to pk for normal validation
        #if isinstance(row[k],models.Model):
            #row[k]=row[k].pk
    
    #model= name_to_model(row['_class'])
    #fields_cls = model_dc.get(model).get('fields')
    
    #kw=request.GET.dict()
    #fields_obj=fields_cls(row,crt_user=user,**kw)
    #if fields_obj.is_valid():
        #fields_obj.save_form()
        #return fields_obj.get_row()
    #else:
        #raise ValidationError(fields_obj.errors)

def clean_dict(dc,model):
    model_name = model_to_name(model)
    for k,v in dc.items():
        if not k.startswith('_'):
            field_path = model_name+'.'+k
            if field_map.get(field_path):
                map_cls = field_map[field_path]
                field = model._meta.get_fields()
                dc[k]=map_cls().from_dict(v,model._meta.get_field(k)) 
    return dc

class ModelFields(forms.ModelForm):
    """
    __init__函数，参数组合
    1. pk,crt_user 编辑，读取的时候
    2. instance,crt_user 编辑，读取的时候
    3. dc,crt_user 保存修改的时候。dc是新值组成的字典
    4. crt_user 新建的时候
    
    """
    readonly=[]
    field_sort=[]
    @classmethod
    def parse_request(cls,request):
        """
        传入参数的形式：
        row_search: key=value&..
        row_sort: _sort=key1,-key2
        page: _page=1
        row_filter:key=value&..
        """
        dc=request.GET.dict()
        pk=dc.pop('pk',None)
        return cls(pk=pk,crt_user=request.user,**dc) 
    
    def __init__(self,dc={},pk=None,crt_user=None,nolimit=False,*args,**kw):
        """
        调用情况：
        1. ajax save 时
        2. ajax get 时，获取数据，或者获取一个新的row数据。
        
        @dc: 当post save时 ,dc是前端传来的row字典
             当get 时，dc是前端传来的url参数，排除pk后的额外的字典
        """
        dc = clean_dict(dc, self._meta.model)
        if not crt_user:
            self.crt_user=dc.get('crt_user')
        else:
            self.crt_user = crt_user
        
        # if pk is None:
        if dc.get('pk'):
            pk=dc.get('pk')
        form_kw={}
        if 'instance' not in kw:
            if pk=='-1':
                form_kw['instance']=self._meta.model.objects.last()
            elif pk:
                try:
                    form_kw['instance']= self._meta.model.objects.get(pk=pk)
                except self._meta.model.DoseNotExist:
                    raise Http404('Id that you request is not exist')
            else:
                form_kw['instance'] = self._meta.model()
        else:
            form_kw['instance']=kw.pop('instance')
        self.nolimit = nolimit
        self.kw=dc.copy()
        self.kw.update(kw)

        super(ModelFields,self).__init__(dc,*args,**form_kw)
        self.custom_permit()
        self.pop_fields()
        self.init_value()
    
    def custom_permit(self):
        self.permit=ModelPermit(self.Meta.model,self.crt_user,nolimit=self.nolimit)
        
        
    def get_context(self):
        """
        """
        return {
            'heads':self.get_heads(),
            'row': self.get_row(),
            #'permit':self.get_permit(),
            'ops':self.get_operations(),
        }  
    def get_del_info(self):
        return {'%(model)s:%(inst)s <id=%(pk)s>'%{'model':self.instance.__class__.__name__,'inst':unicode(self.instance),'pk':self.instance.pk}:delete_related_query(self.instance)}
    
    def get_operations(self):
        ls=[]
        if self.permit.changeable_fields():
            ls.append({
                'name':'save','editor':'com-field-op-btn','label':'保存'
            })
        return ls
    
    def get_permit(self):
        permit_dc = {
            'can_add':self.permit.can_add(),
            'can_del':self.permit.can_del() ,
            'can_log':self.permit.can_log(),
            'can_edit':bool( self.permit.changeable_fields() )
        }

        return permit_dc
    
    def pop_fields(self):
        """
        pop some field out,this will be 
        """
        if self.nolimit or self.crt_user.is_superuser:
            return
        ls=[]
        ls.extend(self.permit.readable_fields())
        ls.extend(self.permit.changeable_fields())
        for key in dict(self.fields).keys():
            if key not in ls:
                self.fields.pop(key)
                
    
    def init_value(self):
        if self.instance.pk:
            for field in self.instance._meta.get_fields(): #get_all_field_names():
                f=field.name
                if f in self.fields:
                    value = getattr(self.instance,f)
                    if hasattr(value,'all'):
                        value=value.all()
                    self.fields[f].initial= value
    
    def get_heads(self):
        heads = form_to_head(self)
        for k,v in self.get_options().items():
            for head in heads:
                if head['name']==k:
                    head['options']=v
        #for k,v in self.get_input_type().items():
            #for head in heads:
                #if head['name']==k:
                    #head['type']=v
        for name in self.get_readonly_fields():
            for head in heads:
                if head['name']==name:
                    head['readonly']=True 
        for head in heads:
            self.dict_head(head)
        if self.field_sort:
            tmp_heads = []
            for k in self.field_sort:
                for head in heads:
                    if head['name'] == k:
                        tmp_heads.append(head)
                        
            return tmp_heads
        else:
            return heads
    
    def can_access(self):
        """
        used to judge if self.crt_user has right to access self.instance
        """
        if self.nolimit:
            return True
        if not self.instance.pk:
            if self.permit.can_add():
                return True
            else:
                return False
        else:
            return self.permit.can_access()
        # perm = self.instance._meta.app_label+'.change_'+self.instance._meta.model_name
        # return self.crt_user.has_perm(perm)
    

    
    def get_readonly_fields(self):
        ls=self.permit.readonly_fields()
        ls.extend(self.readonly)
        return ls
        # return []
    
    def get_row(self):
        """
        convert self.instance to dict.
        Note:Only convert Meta.fields ,not All fields
        """
        if not self.can_access():
            raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name
        #if self._meta.fields:
            #include = [x for x in self._meta.fields if x in self.fields]
        #else:
            #include= self.fields
            
        # self.fields 是经过 权限 处理了的。可读写的字段
        return to_dict(self.instance,filt_attr=self.dict_row,include=self.fields)

    def dict_row(self,inst):
        return {}
    
    def get_options(self):
        options=self.dict_options()
        
        for name,field in self.fields.items():
            if name in options.keys():
                continue
            if isinstance(field,forms.models.ModelMultipleChoiceField):
                options[name]=[{'value':x[0],'label':x[1]} for x in field.choices]
            elif isinstance(field,forms.models.ModelChoiceField):
                options[name]=[{'value':x[0],'label':x[1]} for x in list(field.choices)]
            #if options.get(name,None):
                #options[name]=self.sort_option(options[name])
            
        return options

    def dict_options(self):
        return {}
    
    def dict_head(self,head):
        return head      
    
    #def get_input_type(self):
        #types={}
        #return types
    
    def save_form(self):
        """
        call by model render engin
        """
        if not (self.nolimit or self.crt_user.is_superuser):
            #if self.instance.pk:
                #if not self.permit.changeable_fields():
                    #raise PermissionDenied,'you have no Permission changed %s'%self.instance._meta.model_name 
            #else:
            if not self.can_access():
                raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name  
            # table_perm = self.instance._meta.app_label+'.%s_'%op+self.instance._meta.model_name
            # if not self.crt_user.has_perm(table_perm):
                # raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name 
            # if not self.can_access_instance():
                # raise PermissionDenied,'you have no Permission access %s'%self.instance._meta.model_name  
            
            #model_str= unicode(self.instance)
            for data in self.changed_data:
                if data in self.get_readonly_fields():
                    #self.cleaned_data.pop(data)
                    #print("Can't change {data} of {model},I pop it".format(data=data,model=model_str))
                    raise PermissionDenied,"Can't change {data}".format(data=data)
        
        op=None
        if self.changed_data:
            op='change'
            detail=','.join(self.changed_data)
            
        if self.instance.pk is None:
            op='add'
            detail=''
            self.instance.save() # if instance is a new row , need save first then manytomany_relationship can create   
        
        for k,v in [(k,v) for (k,v) in self.cleaned_data.items() if k in self.changed_data]:
            #print((k,v))
            #if isinstance(v,unicode):
                #v=v.encode('utf-8')
                #print(('sss',v))
            setattr(self.instance,k,v)
        # print(repr(self.instance.name))
        # print('--------------')
        self.instance.save()
        # print('oooooooooooo')
        
        if op:
            log =LogModel(key='{model_label}.{pk}'.format(model_label=model_to_name(self.instance),pk=self.instance.pk),kind=op,user=self.crt_user,detail=detail)
            log.save()
            
        return self.instance
 
    
    def del_form(self):
        if self.permit.can_del():
            self.instance.delete()
        else:
            raise PermissionDenied('No permission to delete %s'%str(self.instance))
        # del_perm = self.instance._meta.app_label+'.del_'+self.instance._meta.model_name
        # if self.crt_user.has_perm(del_perm):
            # self.instance.delete()
    

    
    

class FieldsSet(object):
    template=''
    def __init__(self,pk=None,crt_user=None):
        self.pk=pk
        self.crt_user=crt_user
    
    def get_context(self):
        return {}
        


        