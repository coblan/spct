# encoding:utf-8

from __future__ import unicode_literals

from .model_admin.fields import ModelFields
from .model_admin.tabel import ModelTable
from .pages import FormPage,TablePage
from .model_admin.base import model_dc,permit_list,page_dc

def regist_director(name='',src_model=None,prefix_list=[]):
    """
    name和prefix_list二选一，有name时优先用name
    @name:一般是 模块名.表明
    @prefix_list : 名字列表
    
    之所以用prefix_list，因为有时需要生成pc和移动两个 model manage 页面，这是就需要传入pc和移动的 prefix list，会生成两个
    
    return：返回一个字典，page_dc.update(dc)，就注册了。
    """
    class ThisForm(ModelFields):
        class Meta:
            model=src_model
            exclude=[]
    class ThisFormPage(FieldsPage):
        fieldsCls=ThisForm
    
    class ThisTable(ModelTable):
        model=src_model
        exclude=[]
    
    class ThisTablePage(TablePage):
        tableCls=ThisTable
    
    dc={}
    if name:
        dc[name]=ThisTablePage
        dc[name+'.edit']=ThisFormPage
    else:
        for prefix in prefix_list:
            dc[prefix]=ThisTablePage
            dc[prefix+'.edit']=ThisFormPage
    
    model_dc[src_model]={'fields':ThisForm}
    permit_list.append(src_model)
    page_dc.update(dc)
    return dc
