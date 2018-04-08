from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DakaRecord(models.Model):
    user= models.ForeignKey(User,verbose_name='user',null=True,blank=True)
    create_time=models.DateTimeField(verbose_name='create time',auto_now=True)
    pos=models.CharField('position',max_length=800,blank=True)
    device=models.CharField('device',max_length=300,blank=True)
