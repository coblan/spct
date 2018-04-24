# encoding:utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.
EDITOR_TYPE=(
    ('blocktext','普通编辑器'),
    ('richtext','富文本编辑器'),
)

class KVModel(models.Model):
    key=models.CharField('key',max_length=500,blank=True)
    value=models.TextField(verbose_name='value',blank=True)
    editor_type=models.CharField('编辑器类型',max_length=30,default='blocktext',choices=EDITOR_TYPE)
