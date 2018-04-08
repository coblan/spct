# encoding:utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from . import human

from helpers.director.admin import UserFields,User,UserFormPage
from helpers.director.shortcut import FormPage,TablePage,ModelFields,TabGroup,ModelTable
from helpers.director.engine import and_list
from helpers.director.container import evalue_container
# Create your models here.
"""
employee
==========
雇员信息管理模块。包括一个Employee抽象model类，以及引入了一个human.HumanInfo类作为用户基本信息。使用时，需要继承Employee和HumanInfo类，
覆盖baseinfo字段。

emp_admin = get_admin(BasicInfo, EmployeeModel) ，这样将实例化的Model传递到本模块，返回的是一个字典。

get_admin示例::

    emp_admin = get_admin(BasicInfo, EmployeeModel)
    
    model_dc[BasicInfo]={'fields': emp_admin['BasicInfoFields']}
    model_dc[EmployeeModel]={'fields':emp_admin[ 'EmployeeFields']}
    
    permit_list.append(EmployeeModel)
    permit_list.append(BasicInfo)
    
    page_dc.update(emp_admin['engine_dict'])

"""

class Employee(models.Model):
    user = models.ForeignKey(User,verbose_name=_('account'), blank=True, null=True)
    #baseinfo=models.OneToOneField(human.HumanInfo,verbose_name=_('basic info'),blank=True,null=True)
    eid=models.CharField(_('employee id'),max_length=30,default='')
   
    def __unicode__(self):
        if self.baseinfo:
            return self.baseinfo.name
        else:
            return _('unnamed employee')
    
    class Meta:
        abstract = True



def get_admin( BasicInfo,
                    EmployeeModel):
   
    human_dc=human.get_admin(BasicInfo)
    BasicInfoFields=human_dc['BasicInfoFields'] 
    
    class EmployeeFields(ModelFields):
        
        class Meta:
            model=EmployeeModel
            exclude=['baseinfo']
        
        def dict_options(self):
            users =list(User.objects.filter(employeemodel=None))
            if self.instance.user:
                users.append(self.instance.user)            
            return {
                'user':[{'value':user.pk,'label':unicode(user)}for user in users]
            }
        

    class EmployeeItem(FieldsPage):
        template=''
        fieldsCls=EmployeeFields
        def get_template(self, prefer=None):
            return None
        def get_label(self):
            try:
                emp=EmployeeModel.objects.get(pk=self.pk)
                return '%s的工作信息'%(emp.baseinfo.name if emp.baseinfo else '未命名')
            except EmployeeModel.DoesNotExist:
                return '新建员工'
    
    class BaseinfoItem(FieldsPage):
        template=''
        fieldsCls=BasicInfoFields
        def __init__(self, request):
            self.request=request
            pk= self.request.GET.get('pk')
            emp=EmployeeModel.objects.get(pk=pk)
            base,c = BasicInfo.objects.get_or_create(employeemodel__id=pk)
            if c:
                emp.baseinfo=base
                emp.save()
            self.emp=emp
            self.fields=self.fieldsCls(instance= base,crt_user=request.user)
            self.ctx=self.fields.get_context()
        
        def get_template(self, prefer=None):
            return None
        
        def get_label(self):
            return '%s的个人基本信息'%self.emp.baseinfo.name
    
    
    class UserTab(UserFormPage):
        template=''
        fieldsCls=UserFields
        def __init__(self, request):
            self.request=request
            pk= self.request.GET.get('pk')
            emp=EmployeeModel.objects.get(pk=pk)
            user,c=User.objects.get_or_create(employeemodel__id=pk,defaults={'username':'_uid_%s'%pk})
            if c:
                emp.user=user
                emp.save()
            self.emp=emp
            self.fields=self.fieldsCls(instance= user,crt_user=request.user)
            self.ctx=self.fields.get_context() 
        
        def get_template(self, prefer=None):
            if prefer=='wx':
                return 'wx/tabgroup.html'
            else:
                return 'authuser/user_form_tab.html'
        def get_label(self):
            name = self.emp.baseinfo.name if self.emp.baseinfo else 'unnamed employee'
            return '%s的账号信息'%name
    
    class EmpGroup(TabPage):
        tabs=[{'name':'emp','label':'员工','page_cls':EmployeeItem},
              {'name':'baseinfo','label':'基本信息','page_cls':BaseinfoItem,'visible':and_list([BasicInfo])},
              {'name':'user','label':'账号','page_cls':UserTab,'visible':and_list([User])}]
        
        def get_tabs(self):
            emp_pk=self.request.GET.get('pk')
            if not emp_pk:      # 没有emp_pk 表示是新建employee
                tabs= self.tabs[0:1]
            else:
                
                tabs= self.tabs 
            tabs= evalue_container(tabs,user=self.request.user)
            return tabs

    class EmployeeTable(ModelTable):
        model=EmployeeModel
        #exclude=['baseinfo']
        
        def dict_row(self, inst):
            dc={
                'user':unicode(inst.user),
                'baseinfo':unicode(inst.baseinfo),
                'head':inst.baseinfo.head if inst.baseinfo else ''
            }
            return dc        
    
    class EmployeeTablePage(TablePage):
        tableCls=EmployeeTable 
        
        def get_label(self):
            return '员工列表'
        
    class EmployeeTablePageWX(EmployeeTablePage):
        template='common/m_emp_table.html'
    
    engine_dict={
        'employee':EmployeeTablePage,
        'employee.edit':EmpGroup,
        'employee.wx':EmployeeTablePageWX,
        'employee.wx.edit':EmpGroup,
    }
    
    return locals()