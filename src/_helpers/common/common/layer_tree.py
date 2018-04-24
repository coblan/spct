# encoding:utf-8

from helpers.director.shortcut import ModelPermit
from helpers.director.db_tools import to_dict,model_to_name,from_dict
from django.core.exceptions import PermissionDenied

"""
>5>comp/catalog.rst>
后端
======
源文件:helpers.commmon.dir_man.py

catalog管理的后台逻辑。一般情况下是后台一个dir数据表，一个item数据表。DirMan类要求：dir和item表中，以外键形式指向dirparent，字段名为 **par**。
DirMan不需要继承，只需要实例化，即可使用。

使用步骤:

1. 构建views函数::

    from helpers.common.dir_man import DirMan
    from .models import Work,Index
    import inspect
    # Create your views here.
    
    def dir_man(request):
        manager=DirMan(Index, Work)
        scope= dict(inspect.getmembers(manager,inspect.ismethod))
        return jsonpost(request, scope)
        
2. 完成url.py路由::

    url(r'^dir_mana',workload_view.dir_man),

这样，前端可以通过改地址，与后端函数群进行通信。
<-<
"""

class LayerTree(object):
    def __init__(self,model):
        self.model=model
        
    def dir_data(self,root,par,user):
        """
        @root: 自定义
        @par: to_dict 对象
        
        return :{'parent':[],'items':[]}
        
        items 是 to_dict对象，为每个对象添加_type 属性，定义前段使用的显示
        """
        if '_class' not in root.keys():
            root=from_dict(root,model=self.model)
        else:
            root=from_dict(root)
        
        parents=[]
        if not par.get('pk',None):
            items=[to_dict(x) for x in self.model.objects.filter(par=None)]
            par=root
        else:
            par=from_dict(par)
            items=[to_dict(x) for x in self.model.objects.filter(par=par)]
        
        crt_par=par
        while True:
            parents.append(crt_par)
            if root.pk == crt_par.pk:
                break
            crt_par=crt_par.par
            if not crt_par or not crt_par.pk or crt_par==root:
                break    
            
        find=False
        for par in parents:
            if unicode(par.pk)==root.pk:
                find=True
            elif par.pk is None and root.pk is None:
                find=True
                
        if not find:
            parents.append(root)
        parents.reverse()
        
        return {
            'parents':[to_dict(x)  for x in parents],
            'items':items,
        }
    
    def item_create(self,user,par=None):
        if not ModelPermit(self.model,user).can_add():
            raise PermissionDenied,'not permit create %s'%model_to_name(self.model)
        
        par = from_dict(par,model=self.model)
        if not par or not par.pk:
            i = self.model.objects.create()
        else:
            i = self.model.objects.create( par=par)
        return to_dict(i)
    

    
    def items_paste(self,rows,par,user):
        """粘贴 dir 和 item """
        par = from_dict(par,model=self.model)
        if not par.pk:
            par=None
        # if par and par.pk:
            # par_inst=self.model.objects.get(pk=par)
        # else:
            # par_inst=None
        for row in rows:
            inst = from_dict(row)
            if 'par' in  ModelPermit(inst,user).changeable_fields():
                inst.par=par
                inst.save()
            else:
                raise PermissionDenied,'can not modify par of %s'% model_to_name(inst)
        return {'status':'success'}
     
    def item_del(self,rows,user):
        """ 删除 dir 和 item """
        for row in rows:
            inst=from_dict(row)
            if ModelPermit(inst,user).can_del():
                inst.delete()
            else:
                raise PermissionDenied,'can not delete %s'% model_to_name(inst)
        return {'status':'success'}    