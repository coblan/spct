# encoding:utf-8
from __future__ import unicode_literals
from ..fields.fields import ModelFields
from ..fields.fieldspage import FieldsPage
from django.contrib.auth.models import Group
import json


class AssemGroupFields(ModelFields):

    class Meta:
        model=Group
        fields=['name',]
    
    def get_heads(self):
        heads=super(AssemGroupFields,self).get_heads()
        group_options=[{'value':g.pk,'label':g.name} for g in Group.objects.exclude(name__startswith='assem')]
        heads.append({'name':'child_group','label':'备选权限组','type':'tow_col','options':group_options})
        return heads
    
    def get_row(self):
        row=super(AssemGroupFields,self).get_row()
        group = self.instance
        if hasattr(group,'permitmodel') and group.permitmodel.permit:
            row['child_group']=json.loads(group.permitmodel.permit) #[{'model':x.model,'permit': json.loads(x.permit)} for x in self.instance.per.all()]
        else:
            row['child_group']=[]  
        return row
    
    def get_context(self):
        ctx = super(AssemGroupFields,self).get_context()
        

        return ctx
    
    
class AssemGroupPage(FieldsPage):
    template='authuser/group_assem_form.html'
    fieldsCls=AssemGroupFields
    