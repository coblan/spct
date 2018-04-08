# encoding:utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import models
from helpers.director.model_validator import has_str
from django.utils import timezone
from helpers.case.organize.models import Employee,Department

class Index(models.Model):
    name=models.CharField('name',max_length=500,default='new index',validators=[has_str])
    par = models.ForeignKey('self',verbose_name='parent dir',blank=True,null=True,related_name='childs')
    
    def __unicode__(self):
        return self.name
    

WORK_STATUS=(
    ('pass','通过'),
    ('reject','未通过'),
    ('waiting','等待审核')
)

class Work(models.Model):
    par =models.ForeignKey(Index,verbose_name='目录',blank=True,null=True)
    name= models.CharField('名称',max_length=100,default='new work',validators=[has_str])
    span = models.FloatField('工时',default=0,help_text='单位(小时)')
    status=models.CharField('状态',max_length=20,choices=WORK_STATUS,default='waiting')
    tag = models.CharField('标签',max_length=500,blank=True)
    detail=models.TextField(verbose_name='详细',blank=True)
    desp_img=models.CharField('描述图片',max_length=300,blank=True)
    
    def __unicode__(self):
        return self.name

WORK_SUBMIT_TYPE=(
    ('normal_work','普通工作'),
    ('importent_work','重要工作'),
)

class WorkRecord(models.Model):
    work=models.ForeignKey(Work,verbose_name='工时名称',null=True)
    emp=models.ForeignKey(Employee,verbose_name='员工',blank=False,null=True)
    ex_span=models.FloatField('调整工时',default=0,help_text='单位(小时)，小数或整数')
    status=models.CharField('状态',max_length=20,choices=WORK_STATUS,default='waiting')
    short=models.CharField('简短描述',max_length=300,blank=True)
    detail=models.TextField(verbose_name='详细',blank=True)
    finish_time=models.CharField('完成时间',max_length=20,default='')
    create_time=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    desp_img=models.CharField('描述图片',max_length=300,blank=True)
    count=models.IntegerField(verbose_name='数量',default=1,help_text='整数')
    sub_type=models.CharField('提交类型',max_length=50,choices=WORK_SUBMIT_TYPE,default='normal_work')
    depart=models.ForeignKey(Department,verbose_name='从属部门',blank=True,null=True)
    check_depart=models.ForeignKey(Department,verbose_name='审核部门',blank=True,null=True,related_name='check_workrecord')
    checker=models.ForeignKey(Employee,verbose_name='审核人',blank=True,null=True,related_name='checked_workrecord')
    #tmp=models.BooleanField('临时工时',default=False)
    
    def __unicode__(self):
        if self.work:
            return '%(work)s_%(emp)s | %(finish_time)s'%{'work':self.work,'emp':self.emp,'finish_time':self.finish_time}
        else:
            return 'unnamed workrecord'
