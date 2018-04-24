# encoding:utf-8

from django.db import models
import json
from django.forms import CharField

class JsonField(models.TextField):
    """
    默认值 default可以直接设置python对象，例如{},[]
    """
    def  from_db_value(self,value, expression, connection,ctx):
        return json.loads(value)
    
    def get_prep_value(self,value):
        return json.dumps(value)
    
    def to_python(self,value):
        # 当form.cleaned_data时，老是返回的是字符串。所以需要我转换一下，
        # 查询文档，说clean时有会调用该函数，结果没有调用。这个clean到时是不是form验证时的clean，不得而知。
        # 结果还是依靠下面的formfield成功验证，不把dict对象改成字符串。
        return value
    
    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': JsonFormField}
        defaults.update(kwargs)
        return super(self.__class__, self).formfield(**defaults)

class JsonFormField(CharField):
    """
    **可能** 是用于From类中，外部不要去调用。
    """
    def clean(self, value):
        return value