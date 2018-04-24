# encoding:utf-8
from __future__ import unicode_literals
import inspect
import copy


"""
>->helpers/container.rst>
========
容器
========

evalue_container
-----------------
接收dict或者list对象，对里面的'visible'属性进行计算。
<-<

"""

def evalue_container(container,**kw):
    """
    use to evalue dict or list ,that has some callable element
    
    Example:
    dc={'name':lambda user:user.username}
    
    dc = evalue_container(dc,user=request.user)
    
    """
    if isinstance(container,dict):
        return evalue_dict(container,**kw)
    elif isinstance(container,(tuple,list)):
        return evalue_list(container,**kw)
    elif inspect.isfunction(container):
        args=inspect.getargspec(container).args
        real_kw={}
        for k,v in kw.items():
            if k in args:
                real_kw[k]=v
        return container(**real_kw)
    else:
        return container

def evalue_dict(dc,**kw):
    out_dc={}
    for k,v in dc.items():
        out_dc[k]=evalue_container(v,**kw)
    return out_dc

def evalue_list(ls,**kw):
    new_ls=[]
    for item in ls:
        # 如果不是 visible，就去掉该项，**连其他key对应的function都不要运行**
        tmp = copy.deepcopy(item)
        if isinstance(tmp,dict) and tmp.has_key('visible'):
            visible= tmp.get('visible')
            if inspect.isfunction(visible):
                visible=run_func(visible,**kw)
            if not visible:
                continue  
            tmp.pop('visible',None)
        tmp=evalue_container(tmp,**kw)
        new_ls.append(tmp)
    return new_ls

def run_func(func,**kw):
    args=inspect.getargspec(func).args
    real_kw={}
    for k,v in kw.items():
        if k in args:
            real_kw[k]=v  
    return func(**real_kw)

def find_one(collection,dc):
    for doc in collection:
        find=True
        for k,v in dc.items():
            if doc.get(k)!=v:
                find=False
        if find:
            return doc

def find_one_r(collection,dc):
    item=find_one(collection, dc)
    if item:
        return item
    else:
        for doc in collection:
            for k,v in doc.items():
                if isinstance(v,(list,tuple)):
                    item= find_one_r(v,dc)
                    if item:
                        return item
                