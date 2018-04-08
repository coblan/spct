# encoding:utf-8
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from .models import Department,EmployeeData
import json
from helpers.director.db_tools import to_dict

def user_to_employee(user):
    if not hasattr(user,'employee_set'):
        raise PermissionDenied,'you are not employee'
    employee=user.employee_set.first()
    if not employee:
        raise PermissionDenied,'you are not employee'
    return employee

class ValidDepart(object):
    """
    
    data_key
      在EmployeeData数据表中，保存了员工的数据。其中就有对应各个页面的department筛选条件。data_key就是这些页面对应的数据key。每个页面
    的key都不同。
    
    """
    data_key=''
    
    @classmethod
    def parse_request(cls,request):
        employee=user_to_employee(request.user)
        depart_pk=request.GET.get('_depart')
        return cls(employee,depart_pk=depart_pk)
    
    def __init__(self,employee,depart_pk=None):
        self.employee=employee
        self.depart_pk=depart_pk
        if not self.employee:
            raise PermissionDenied,'Only employee allowd access deparment data'

    def get_query_depart(self):
        depart=self.get_crt_depart()
        concern=self.employee.user.concerndepartmodel_set.first()
        depart_list=[]
        if concern:
            depart_list= concern.departs.all()
            depart_list=filter(lambda x: x.par_chain.startswith(depart.par_chain),depart_list)
        if depart not in depart_list:
            depart_list.append(depart)
            
        return depart_list
    
    # def get_query_depart(self):
        # depart=self.get_crt_depart()
        # depart_list=[]
        # if hasattr(self.employee,'employeedata') and  self.employee.employeedata.content:
            # dc = json.loads(self.employee.employeedata.content)
            # pk_list = dc.get(self.data_key,[])
            # depart_list=[Department.objects.get(pk=x) for x in pk_list]
            # depart_list=filter(lambda x: x.par_chain.startswith(depart.par_chain),depart_list)
        # if depart not in depart_list:
            # depart_list.append(depart)
            
        # return depart_list
    
    
    def get_crt_depart(self):
        allowed_depart= self.get_allowed_depart()
        if not allowed_depart:
            raise PermissionDenied,'No Valid department'
        depart=None
        if self.depart_pk:
            for dep in allowed_depart:
                if unicode(dep.pk) ==self.depart_pk:
                    depart=dep
        else:
            depart=allowed_depart[0]
        
        if not depart:
            raise PermissionDenied,'No Valid department' 
        return depart

    def get_allowed_depart(self):
        """
        """
        return []
        # allowed_depart=[]
        # for depart in employee.depart.all():
            # permit = WorkModelPermit(WorkRecord, user, department=depart)
            # if 'status' in permit.changeable_fields():
                # allowed_depart.append(depart)
        # return allowed_depart   
    
    def get_context(self,ctx=None):
        ctx = ctx or {}
        allowed_departs=self.get_allowed_depart()
        ctx['depart_list']=[{'pk':x.pk,'label':unicode(x)} for x in allowed_departs]
        ctx['crt_depart']=to_dict( self.get_crt_depart())
        ctx['data_key']=self.data_key
        ctx['child_depart_list']=[to_dict(x) for x in self.get_query_depart()[:-1]]
        return ctx   
    
    