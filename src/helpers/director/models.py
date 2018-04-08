# encoding:utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from .model_func.jsonfield import JsonField


class LogModel(models.Model):
    at = models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User,verbose_name=_('operator'),blank=True,null=True)
    key =models.CharField('key',max_length=200,blank=True)
    kind = models.CharField(_('kind'),max_length=100,blank=True)
    detail =models.TextField(_('detail'),blank=True)
    
# class PermitGroup(models.Model):
    # name = models.CharField('权限组名称',max_length=300)
    # permit=models.ManyToManyField('PermitModel',verbose_name="权限")
    # desp=models.TextField(verbose_name="描述",blank=True)
    
class PermitModel(models.Model):
    name = models.CharField('权限名称',max_length=300)
    group = models.ManyToManyField(Group,verbose_name=_('user group'),blank=True,null=True)
    # group = models.OneToOneField(Group,verbose_name=_('user group'))
    # model = models.CharField('model',max_length=200, default='')
    permit = JsonField(verbose_name=_('user permit'),default={})
    desp=models.TextField(verbose_name="描述",blank=True)
    
    def __unicode__(self):
        return self.name




