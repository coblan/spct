# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelFields,FormPage
from ..models import BasicInfo,Employee

class BasicInfoFields(ModelFields):

    class Meta:
        model=BasicInfo
        exclude=[]
        
    def get_heads(self):
        heads=super(BasicInfoFields,self).get_heads()
        for head in heads:
            if head.get('name')=='head':
                head['type']='picture'
                head['config']={
                'crop':True,
                'aspectRatio': 1,
                'size':{'width':250,'height':250}
            }
        return heads
    
    def save_form(self):
        #if not self.instance.pk or self.instance.employee.user==self.crt_user:
            #self.
        rt = super(self.__class__,self).save_form()
        if not hasattr(self.instance,'employee'): # baseinfo 不允许没有员工与之相关
            emp = self.crt_user.employee_set.first()
            emp.baseinfo=self.instance
            emp.save()
        return rt
    
class BaseinfoItem(FieldsPage):
    template=''
    fieldsCls=BasicInfoFields
    def __init__(self, request):
        self.request=request
        pk= self.request.GET.get('pk')
        emp=Employee.objects.get(pk=pk)
        base,c = BasicInfo.objects.get_or_create(employee__id=pk)
        if c:
            emp.baseinfo=base
            emp.save()
        self.emp=emp
        self.fields=self.fieldsCls(instance= base,crt_user=request.user)
        self.permit=self.fields.permit
        self.ctx=self.fields.get_context()
    
    def get_template(self, prefer=None):
        return None
    
    def get_label(self):
        if self.emp.baseinfo:
            return '%s的个人基本信息'%self.emp.baseinfo.name
        else:
            return '个人基本信息'
    