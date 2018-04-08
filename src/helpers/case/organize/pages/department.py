# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelFields,FormPage,TabGroup,model_dc
from ..models import DepartManage,Department

class DepartmentForm(ModelFields):

    class Meta:
        model=Department
        exclude=['par','par_chain']
    
    
class DepartmentTab(FieldsPage):
    template=''
    fieldsCls=DepartmentForm
    # def __init__(self, request):
        # self.request=request
        # pk= self.request.GET.get('pk')
        # emp=Employee.objects.get(pk=pk)
        # base,c = BasicInfo.objects.get_or_create(employee__id=pk)
        # if c:
            # emp.baseinfo=base
            # emp.save()
        # self.emp=emp
        # self.fields=self.fieldsCls(instance= base,crt_user=request.user)
        # self.ctx=self.fields.get_context()
    
    def get_template(self, prefer=None):
        if prefer=='f7':
            return 'organize/department_form_f7.html'
        else:
            return 'director/tabgroup.html'
    
    # def get_label(self):
        # return '%s的个人基本信息'%self.emp.baseinfo.name

class DepartManageForm(ModelFields):
    readonly=['depart']
    class Meta:
        model=DepartManage
        exclude=[]
    
    def dict_head(self, head):
        if head['name']=='recv_event':
            head['type']='check_select'
        return head
    
    def dict_options(self):
        return {'recv_event':[
        {'value':'normal_work','label':'普通工作'},
        {'value':'importent_work','label':'重要工作'}
        ]}
    #def clean_recv_event(self):
        #data = self.cleaned_data['recv_event']
        #return data
        
    
    
        
class DepartManageTab(FieldsPage):
    template=''
    fieldsCls=DepartManageForm
    def __init__(self,request):
        self.request=request
        pk= self.request.GET.get('pk')
        depart=Department.objects.get(pk=pk)
        manage,c=DepartManage.objects.get_or_create(depart=depart)
        self.fields=self.fieldsCls(instance=manage,crt_user=request.user)
        self.ctx=self.fields.get_context()
        
        # department=Department.objects.get(pk=pk)
        # manage,c=DepartManage.get_or_create(depart=department)
        # if c:
            # de
        # user,c=User.objects.get_or_create(employee__id=pk)
        # if c:
            # emp.user=user
            # emp.save()
        # self.emp=emp
        # self.fields=self.fieldsCls(instance= user,crt_user=request.user)
        # self.ctx=self.fields.get_context()
    

class DepartmentGroup(TabPage):
    tabs=[{'name':'department','label':'基本信息','page_cls':DepartmentTab},
          {'name':'departmanage','label':'管理设置','page_cls':DepartManageTab}
          ]

    
    # def get_tabs(self):
        # emp_pk=self.request.GET.get('pk')
        # tabs= self.tabs
        # if not emp_pk:      # 没有emp_pk 表示是新建employee
            # tabs= self.tabs[0:1]
        # else:
            # emp= Employee.objects.get(pk=emp_pk)
            # if not emp.user:        # 没有账号时，不显示账号标签
                # tabs=[x for x in tabs if x['name']!='user']
            
        # tabs= evalue_container(tabs,user=self.request.user)
        # return tabs
    
model_dc[DepartManage]={'fields':DepartManageForm}
model_dc[Department]={'fields':DepartmentForm}