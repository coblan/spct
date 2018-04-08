from __future__ import unicode_literals
from django.db import models

class WebPage(models.Model):
    name=models.CharField('name',max_length=300,blank=True)
    temp=models.CharField('template',max_length=300,blank=True)
    label=models.CharField('label',max_length=300,blank=True)
    status=models.CharField('status',max_length=100,blank=True)
    content=models.TextField(verbose_name='content',blank=True)
    
