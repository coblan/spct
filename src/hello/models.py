from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    merchantid = models.IntegerField(verbose_name='商户ID',null=True,blank=True) 
    