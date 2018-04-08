# encoding:utf-8

import json
from .models import WorkPermitModel
from helpers.director.model_admin.permit import ModelPermit,has_permit
from helpers.director.db_tools import model_to_name

class DepartModelPermit(ModelPermit):
    """
    相对于父类，ModelPermit增加了一个department参数。如果不传入department，会自动提取雇员从属的第一个部门。注意：这里的user必须是employee。
    """
    def __init__(self,model,employee,department=None,nolimit=False):
        self.employee= employee
        if not department:
            department=self.employee.depart_set.first()
        self.department=department        
        super(DepartModelPermit,self).__init__(model,employee.user,nolimit=False)
        
        
    def _read_perm_from_db(self):
        model_name = model_to_name(self.model)
        workpermit= self.employee.workpermitmodel_set.filter(depart=self.department).first()
        if not workpermit:
            self.permit_list=[]
        else:
            for group in workpermit.group.all():
                if hasattr(group,'permitmodel'):
                    permits = json.loads( group.permitmodel.permit )
                    permit= permits.get(model_name,[])
                    self.permit_list.extend(permit)
            self.permit_list=list(set(self.permit_list))   
    
def has_depart_permit(employee,name,depart):
    if employee.user.is_superuser:
        return True
    depart_permit = employee.workpermitmodel_set.filter(depart=depart).first()
    if not depart_permit:
        return False
    cls,perm=name.split('.')
      
    for group in depart_permit.group.all():
        if hasattr(group,'permitmodel'):
            permit_dc = json.loads( group.permitmodel.permit )
            sp_permit_list= permit_dc.get(cls,[])
            if perm in sp_permit_list:
                return True
    return False        
    