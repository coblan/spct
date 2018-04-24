# encoding:utf-8
from __future__ import unicode_literals
import employee

def get_admin(BasicInfo,
                    EmployeeModel):
    emp_admin=employee.get_admin(BasicInfo, EmployeeModel)
    
    class EmployeeItem(emp_admin['EmployeeItem']):
        template=''
    
    emp_admin['EmployeeItem']=EmployeeItem
    emp_admin['EmpGroup'].tabs[0]={'name':'emp','label':'员工','page_cls':EmployeeItem}
    return emp_admin
    