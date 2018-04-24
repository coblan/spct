# encoding:Utf-8
"""
这个文件不用了，所有功能往director.ajax转移。
========
这里的ajax函数是被所有由render生成的页面共用的。
如果TablePage或者FormPage的ajax_scope中有相同名字的函数，则优先调用。

"""
from __future__ import unicode_literals

from permit import ModelPermit
from base import model_dc
from ..model_func.dictfy import name_to_model,model_to_name,to_dict,permit_save_model
from fields import save_row
from django.core.exceptions import ValidationError
from ..models import PermitModel
from django.contrib.auth.models import Group,User
import json
#from base import model_dc,get_admin_name_by_model,del_row
from django.db import transaction

def model_perm(user,perm,model):
    validator = ModelPermit(model, user)
    return getattr(validator,perm)()



        
def save_fieldset(fieldset,save_step,user):
    out={}
    try:
        with transaction.atomic():
            for step in save_step:
                if step.get('save'):
                    name=step.get('save')

                    fieldset[name] = save_row(fieldset.get(name), user)
                    instance=fieldset[name]
                    perm=ModelPermit(instance,user)
                    dc =to_dict(instance,include=perm.readable_fields())
                    out[name]=dc              
                      
                if step.get('assign'):
                    fieldset[step['obj']] [step['assign']]=fieldset[step['value']]
        return {'status':'success','fieldset':out}
    except ValidationError as e:
        return {'errors':dict(e),'path':name+'.errors'}     
    




#def save_group_and_permit(row,permits,user): 
    #field_cls = model_dc.get(Group).get('fields')
    #group_form= field_cls(row, crt_user= user)
    #if group_form.is_valid():
        #group_form.save_form()
    #group = group_form.instance
    #if not hasattr(group,'permitmodel'):
        #PermitModel.objects.create(group=group)
    #group.permitmodel.permit=json.dumps(permits)
    #group.permitmodel.save()
    
    ## perm={'group':group_form.instance.pk,'permit':permits}
    ## perm_form = save_row(perm, user)
    #return {'status':'success'}