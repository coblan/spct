# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.db_tools import from_dict,permit_save_model
from .models import WorkPermitModel,Employee,EmployeeData,ConcernDepartModel
import json

#from .models import Department
#from helpers.common.layer_tree import LayerTree
#import inspect
#from helpers.director.port import jsonpost


def get_global():
    return globals()

def save_self_info(base_info,user):
    """
    **这个函数没用了，现在直接调用的 save 函数**  准备删除
    员工保存自身基本信息
    """
    
    instance = from_dict(base_info)
    permit_save_model(user,instance)
    # instance.save()
    if getattr(instance,'employee',None) is None:
        emp =user.employee_set.first()
        emp.baseinfo=instance
        emp.save()
    elif instance.employee and instance.employee.user==user:
        instance.save()
    else:
        return {'status':'error','msg':'base info not match with current user'}
    return {"status":'success'}

def save_workpermit(permits,emp_pk,user):
    employee=Employee.objects.get(pk=emp_pk)
    for permit in permits:
        depart=from_dict(permit.get('depart'))
        wp=WorkPermitModel.objects.get(emp=employee,depart=depart)
        groups=[from_dict(x) for x in permit.get('groups') if x]
        #for group in groups:
            #wp.group.add(group)
        #for group in wp.groups.all():
            #if group not in groups:
                #wp.groups.remove(group)
        wp.group=groups
        wp.save()
    return {'status':'success'}

def save_emplyee_data(data_key,content,user):
    emp = user.employee_set.first()
    if not hasattr(emp,'employeedata'):
        EmployeeData.objects.create(emp=emp,content='{}')
    dc=json.loads(emp.employeedata.content)
    dc[data_key]=content
    emp.employeedata.content=json.dumps(dc)
    emp.employeedata.save()
    return {'status':'success'}


def save_concern_depart(depart,user):
    depart=from_dict(depart)
    concern,_ = ConcernDepartModel.objects.get_or_create(user=user)
    if depart not in  concern.departs.all():
        concern.departs.add(depart)
    return {'status':'success'}

def rm_concern_depart(depart,user):
    depart=from_dict(depart)
    concern,_ = ConcernDepartModel.objects.get_or_create(user=user) 
    concern.departs.remove(depart)
    return {'status':'success'}
