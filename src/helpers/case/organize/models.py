# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from helpers.director.model_validator import has_str
from .config import config

GEN=(
    ('male',_('male')),
    ('femal',_('femal'))
    )

class BasicInfo(models.Model):
    name = models.CharField(_('name'), max_length=50, blank=True)
    age = models.CharField(_('age'), max_length=50, blank=True)
    head = models.CharField(_('head image'),max_length=200,blank=True,default='/static/res/image/user.jpg')
    id_number=models.CharField(_('id  number'),max_length=200,blank=True)
    address=models.CharField(_('address'),max_length=500,blank=True)
    gen = models.CharField(_('gen'),max_length=30,blank=True,choices=GEN)
    phone = models.CharField(_('phone'),max_length=100,blank=True)


    def __unicode__(self):
        return self.name
    
    def save(self, **kw):
        super(BasicInfo,self).save(**kw)
        if hasattr(self,'employee') and self.employee.user:
            self.employee.user.first_name=self.name
            self.employee.user.save()
    class Meta:
        verbose_name=_("Employee Basic info Table")


class Department(models.Model):
    name=models.CharField(_('department name'),max_length=500,default='new department',validators=[has_str])
    par = models.ForeignKey('self',verbose_name=_('parent department'),blank=True,null=True,related_name='childs')
    detail=models.TextField(verbose_name=_('detail'),blank=True)
    par_chain=models.CharField('parent chain',max_length=200,blank=True)

    class Meta:
        verbose_name=_("Department Table")
        
    def __unicode__(self):
        return self.name
    
    def __init__(self,*args,**kw):
        super(Department,self).__init__(*args,**kw)
        self._org_par=self.par

    def save(self, *args,**kw):   
        rt= super(Department,self).save(*args,**kw)
        if self._org_par !=self.par or not self.par_chain:
            self._org_par=self.par
            self.update_parent_chain()  
        return rt
    
    def update_parent_chain(self):
        par =self.par
        ls=[self.pk]
        while par:
            ls.append(par.pk)
            par=par.par
        ls=reversed([str(x) for x in ls])
        self.par_chain='.'.join(ls)
        self.save()
        for depart in self.childs.all():
            depart.update_parent_chain() 
    
    def is_par(self,depart):
        par = depart.par
        while par:
            if par==self:
                return True
            else:
                par=par.par
        return False

MANAGE_EVENT=(
    ('normal_work','普通工作'),
    ('importent_work','重要工作'),
    # ('small_money','小额花费')
)

class DepartManage(models.Model):
    depart=models.OneToOneField(Department,verbose_name=_('department'),blank=True,null=True)
    recv_event=models.CharField(_('recive pop event'),max_length=500,blank=True) # ,choices=MANAGE_EVENT

class Employee(models.Model):
    user = models.ForeignKey(User,verbose_name=_('account'), blank=True, null=True)
    eid=models.CharField(_('employee id'),max_length=30,blank=True)    
    baseinfo=models.OneToOneField(BasicInfo,verbose_name=_('basic info'),blank=True,null=True)
    position = models.CharField(_('job position'),max_length=100,blank=True)
    #depart=models.ForeignKey(Department,verbose_name=_('department'),blank=True,null=True,on_delete=models.SET_NULL)
    depart=models.ManyToManyField(Department,verbose_name=_('department'),blank=True,null=True)
    

    class Meta:
        verbose_name=_('Employee info Table')
        
    def __unicode__(self):
        if self.baseinfo:
            return self.baseinfo.name
        else:
            return self.eid  
            
    def save(self, *args,**kw):
        super(Employee,self).save()
        if not self.eid:
            temp='%s%0'+config['empid_number_length']+'d'
            self.eid= temp%(config['empid_prefix'],self.pk)
            self.save()

class WorkPermitModel(models.Model):
    """
    记录同一个员工，在不同部门的不同权限
    """
    depart=models.ForeignKey(Department,verbose_name=_('department'),blank=True,null=True)
    group=models.ManyToManyField(Group,verbose_name=_('group'),blank=True,null=True)
    emp=models.ForeignKey(Employee,verbose_name=_('employee'),blank=True,null=True)
    
    

class EmployeeData(models.Model):
    emp=models.OneToOneField(Employee,verbose_name=_('employee'),blank=True,null=True)
    content=models.TextField(verbose_name=_('content'),blank=True)
    
class ConcernDepartModel(models.Model):
    """
    关注的下级部门
    """
    user=models.ForeignKey(User,verbose_name=_('account'),blank=True,null=True)
    departs=models.ManyToManyField(Department,verbose_name=_('department'),blank=True,null=True)
    
