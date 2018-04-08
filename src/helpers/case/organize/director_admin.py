# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import

from helpers.director.container import evalue_container
from helpers.director.admin import UserFields,User,UserFormPage
from helpers.director.engine import and_list
from helpers.director.shortcut import FormPage,TablePage,ModelFields,ModelTable,page_dc,model_dc,permit_list,TabGroup,has_permit
from helpers.director.db_tools import to_dict
from django.contrib import admin
from .models import Employee,BasicInfo,Department,WorkPermitModel
from django.contrib.auth.models import User
from django.db.models import Q
from .pages.myinfo import EmployeeSelf
from .pages.baseinfo import BaseinfoItem,BasicInfoFields
from .pages.department import DepartmentGroup
from .pages.empoyee_permit import EmployePermitTab
from django.conf import settings
from helpers.ex import locate

class EmployeeFields(ModelFields):
    
    class Meta:
        model=Employee
        exclude=['baseinfo']
    
    #def get_row(self):
        #row = super(EmployeeFields,self).get_row()
        #if 'depart' in row.keys() and self.instance.depart:
            #row['depart_obj']={'pk':self.instance.depart.pk,'name':self.instance.depart.name}
        #return row
    
    def dict_head(self, head):
        if head['name']=='eid':
            head['readonly']=True
        return head
    
    def dict_options(self):
        users =list(User.objects.filter(employee=None))
        if self.instance.user:
            users.append(self.instance.user) 
        
        user_options=[{'value':None,'label':'---'}]
        options=[{'value':user.pk,'label':unicode(user)}for user in users]
        options=sorted(options,cmp=lambda x,y: cmp(x['label'],y['label']) )
        user_options.extend(options)
        return {
            'user':user_options,
            #'depart':[],
        }
    
class EmployeeItem(FieldsPage):
    template=''
    fieldsCls=EmployeeFields
    
    def __init__(self, request):
        pk= request.GET.get('pk')
        if pk:
            self.employee=Employee.objects.get(pk=pk) 
        else:
            self.employee=Employee()
        self.fields=self.fieldsCls(instance= self.employee,crt_user=request.user)
        self.ctx=self.fields.get_context() 
    
    def get_label(self):
        try:
            # emp=Employee.objects.get(pk=self.pk)
            return '%s的工作信息'%(self.employee.baseinfo.name if self.employee.baseinfo else '未命名')
        except Employee.DoesNotExist:
            return '新建员工'
        # 
    def get_template(self, prefer=None):
        if prefer=='f7':
            return 'organize/employee_form_f7.html'
        if prefer=='wx':
            return 'organize/employee_form_wx.html'
        else:
            return 'organize/employee_form.html'


class EmployeeSelfWorkinfo(EmployeeItem):
    template='organize/employee_self_f7_workinfo.html'
    def __init__(self, request):
        self.employee=request.user.employee_set.first()
        self.fields=self.fieldsCls(instance= self.employee,crt_user=request.user,nolimit=True)
        self.ctx=self.fields.get_context()   
    def get_template(self, prefer=None):
        return self.template

class EmployeeSelfBaseinfo(BaseinfoItem):
    def __init__(self, request):
        self.request=request
        emp=request.user.employee_set.first()
        if not hasattr(emp,'baseinfo'):
            base=BasicInfo.objects.create()
            emp.baseinfo=base
            emp.save()
        else:
            base=emp.baseinfo
        self.emp=emp
        self.fields=self.fieldsCls(instance= base,crt_user=request.user)
        self.permit=self.fields.permit
        self.ctx=self.fields.get_context()
        
        # heads=self.ctx['heads']
        # if not has_permit(request.user,"self_admin.modify_self_info"):
            # for head in heads:
                # head['readonly']=True
    
    def get_template(self, prefer=None):
        return 'organize/employee_self_f7_baseinfo.html'

class UserTab(UserFormPage):
    template=''
    fieldsCls=UserFields
    def __init__(self, request):
        self.request=request
        pk= self.request.GET.get('pk')
        emp=Employee.objects.get(pk=pk)
        user,c=User.objects.get_or_create(employee__id=pk)
        if c:
            emp.user=user
            emp.save()
        self.emp=emp
        self.fields=self.fieldsCls(instance= user,crt_user=request.user)
        self.ctx=self.fields.get_context() 
    
    def get_template(self, prefer=None):
        if prefer=='f7':
            return 'f7/tabgroup.html'
        else:
            return 'authuser/user_form_tab.html'
    def get_label(self):
        name = self.emp.baseinfo.name if self.emp.baseinfo else 'unnamed employee'
        return '%s的账号信息'%name

class EmpGroup(TabPage):
    tabs=[{'name':'emp','label':'员工','page_cls':EmployeeItem},
          {'name':'baseinfo','label':'基本信息','page_cls':BaseinfoItem,'visible':and_list([BasicInfo])},
          {'name':'user','label':'账号','page_cls':UserTab,'visible':and_list([User])},
          {'name':'permit','label':'工作权限','page_cls':EmployePermitTab,'visible':and_list(
              [WorkPermitModel])}]
    
    def get_tabs(self):
        emp_pk=self.request.GET.get('pk')
        tabs= self.tabs
        if not emp_pk:      # 没有emp_pk 表示是新建employee
            tabs= self.tabs[0:1]
        else:
            emp= Employee.objects.get(pk=emp_pk)
            if not emp.user:        # 没有账号时，不显示账号标签
                tabs=[x for x in tabs if x['name']!='user']
            
        tabs= evalue_container(tabs,user=self.request.user)
        return tabs

class EmployeeTable(ModelTable):
    model=Employee
    #exclude=['baseinfo']
    
    def dict_row(self, inst):
        dc={
            'user':unicode(inst.user),
            'baseinfo':unicode(inst.baseinfo),
            'head':inst.baseinfo.head if inst.baseinfo else '',
            'depart':','.join([unicode(x) for x in inst.depart.all()]),
        }
        return dc 

class EmployeeTablePage(TablePage):
    tableCls=EmployeeTable 
    
    def get_label(self):
        return '员工列表'
    
class EmployeeTablePageWX(EmployeeTablePage):
    template='organize/employee_table_f7.html'


class DepartmentForm(ModelFields):
    class Meta:
        model=Department
        exclude=['par','par_chain']
    
        
class DepartmentPage(object):
    template=''
    def __init__(self,request):
        self.request=request
        
    def get_context(self):
        departform = DepartmentForm(crt_user=self.request.user)
        self.ctx={
            #'app':'',
            'heads':departform.get_heads(),
            'can_edit':departform.permit.can_add(),
        }
        return self.ctx  
    def get_template(self,prefer=None):
        if prefer=='f7':
            return 'organize/department_f7.html'
        else:
            return 'organize/department.html'


class EmployeeSelfConcernDepart(object):
    def __init__(self, request):
        self.request=request
        emp=request.user.employee_set.first()
        depart_dc_list=[]
        user=request.user
        concern= user.concerndepartmodel_set.first()
        for depart in emp.depart.all():
            dc = to_dict(depart)
            dc['concern_subdepart']=[]
            if concern:
                dc['concern_subdepart']=[to_dict(x) for x in concern.departs.all() if depart.is_par(x)]
            depart_dc_list.append(dc)
        
        self.ctx={
            'departs':depart_dc_list
        }
    
    def get_context(self):
        return self.ctx
    
    def get_template(self, prefer=None):
        return 'organize/employee_self_concern_f7.html'
    
    def get_label(self):
        return "关注部门"

if  hasattr(settings,'EMPGROUP'):
    get_empgroup=settings.EMPGROUP
    EmpGroup=get_empgroup(**globals())



page_dc.update({
    'organize.employee':EmployeeTablePage,
    'organize.employee.edit':EmpGroup,
    'organize.department':DepartmentPage,
    'organize.department.edit':DepartmentGroup,
    
    
    'organize.employee.f7':EmployeeTablePageWX,
    'organize.employee.f7.edit':EmpGroup,
    'organize.employeeself.f7':EmployeeSelf, 
    
    'organize.employeeself.f7.workinfo':EmployeeSelfWorkinfo,
    'organize.employeeself.f7.baseinfo':EmployeeSelfBaseinfo,
    'organize.employeeself.f7.concern_depart':EmployeeSelfConcernDepart,
})

model_dc[Employee]={'fields':EmployeeFields}
# model_dc[Department]={'fields':DepartmentForm}
model_dc[BasicInfo]={'fields':BasicInfoFields}
permit_list.append(Employee)
permit_list.append(BasicInfo)
permit_list.append(Department)

# permit_list.append({'name':'self_admin','label':'人员信息设置','fields':[
    # {'name':'modify_self_info','label':'修改基本信息','type':'bool'}
# ]
# })
# permit_list.append(WorkPermitModel)
