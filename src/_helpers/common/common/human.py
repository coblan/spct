# encoding:utf-8

from __future__ import unicode_literals

from django.contrib.auth.models import User,Group
from django.db import models
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelFields

# Create your models here.

GEN=(
    ('male',_('male')),
      ('femal',_('femal'))
      )
     
class HumanInfo(models.Model):
    name = models.CharField(_('name'), max_length=50, blank=True)
    age = models.CharField(_('age'), max_length=50, blank=True)
    head = models.CharField(_('head image'),max_length=200,blank=True,default='/static/res/image/user.jpg')
    id_number=models.CharField(_('id  number'),max_length=200,blank=True)
    address=models.CharField(_('address'),max_length=500,blank=True)
    gen = models.CharField(_('gen'),max_length=30,blank=True,choices=GEN)
    phone = models.CharField(_('phone'),max_length=100,blank=True)
    
      
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name=_('basic info')
        abstract = True



def get_admin(BasicInfo):
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
        
    return locals()