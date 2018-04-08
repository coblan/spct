# encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from .dictfy import name_to_model,model_dc
from django.core.exceptions import ValidationError

def permit_save_model(user,row,**kw):
    for k in row: # convert model instance to pk for normal validation
        if isinstance(row[k],models.Model):
            row[k]=row[k].pk
            
    model= name_to_model(row['_class'])
    fields_cls = model_dc.get(model).get('fields')

    fields_obj = fields_cls(row,crt_user=user,**kw)
    if fields_obj.is_valid():
        fields_obj.save_form()
        return fields_obj
    else:
        raise ValidationError(fields_obj.errors)
    
