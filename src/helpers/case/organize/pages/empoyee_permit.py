# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelFields,FormPage,ModelPermit,model_dc
from ..models import WorkPermitModel,Employee
from helpers.director.db_tools import to_dict
from django.contrib.auth.models import Group

class EmployePermitTab(FieldsPage):
    template=''

    def __init__(self, request):
        self.request=request
        pk= self.request.GET.get('pk')
        self.emp=Employee.objects.get(pk=pk)
        out=[]
        for depart in self.emp.depart.all():
            permit,c = WorkPermitModel.objects.get_or_create(emp=self.emp,depart=depart)
            out.append({'groups':[to_dict(x) for x in permit.group.all()],
                        'depart':to_dict(permit.depart)})
        groups=[to_dict(x) for x in Group.objects.all()] #.filter(name__startswith='depart.')] 
        self.ctx={
            'permits':out,
            'groups':groups
        }
    
    
    def get_context(self):
        ##if self.fieldsCls:
        
        self.ctx['can_add']=True
        self.ctx['can_del']=True   
        self.ctx['can_log']=True
        
        perm = ModelPermit(WorkPermitModel,self.request.user)
        if perm.changeable_fields():
            self.ctx['can_edit']=True
        else:
            self.ctx['can_edit']=False
        
        self.ctx['app']='organize'
        #self.ctx['page_label'] =self.get_label()
        return self.ctx    
    
    def get_template(self, prefer=None):
        if prefer=='f7':
            return 'organize/employee_permit_f7.html'
        else:
            return 'organize/employee_permit.html'
    
    def get_label(self):
        return '%s的工作权限'% unicode(self.emp)
 
    


class WorkPermiForm(ModelFields):
    class Meta:
        model=WorkPermitModel
        exclude=[]
        
model_dc[WorkPermitModel]={'fields':WorkPermiForm}