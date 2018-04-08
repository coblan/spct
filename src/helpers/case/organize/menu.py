# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.engine import BaseEngine,can_list,can_touch,fa,page
from .models import BasicInfo,Employee,Department

pc_menu={
    'label':'组织管理','icon':fa('fa-sitemap'),'visible':can_list((Employee,Department)),
        'submenu':[
                 {'label':'部门管理','url':page('organize.department'),'visible':can_touch(Department)},   
                 {'label':'员工名册','url':page('organize.employee'),'visible':can_touch(Employee)},
             ]    
}

wx_menu=[
    {'label':'员工','url':page('organize.employee.wx'),'icon':fa('fa-user-o fa-2x'),'visible':can_list([BasicInfo,Employee,Department])},
    {'label':'部门','url':page('organize.department'),'icon':fa('fa-sitemap fa-2x'),'visible':can_touch(
        Department)},    
]

f7_menu=[
    {'name':'organize_employee_f7','label':'员工','url':page('organize.employee.f7'),'icon':fa('fa-user-o fa-2x'),'visible':can_list([BasicInfo,Employee,Department])},
    {'name':'organize_department','label':'部门','url':page('organize.department'),'icon':fa('fa-sitemap fa-2x'),'visible':can_touch(
        Department)},    
]
