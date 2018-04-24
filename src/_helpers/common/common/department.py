# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from django.utils.translation import ugettext as _
from django.db import models
from .dir_man import DirMan
from helpers.director.shortcut import ModelFields
from helpers.director.model_validator import has_str

class DepartmentBase(models.Model):
    name=models.CharField(_('department name'),max_length=500,default='new department',validators=[has_str])
    par = models.ForeignKey('self',verbose_name=_('parent department'),blank=True,null=True,related_name='childs')
    detail=models.TextField(verbose_name=_('detail'),blank=True)
    par_chain=models.CharField('parent chain',max_length=200,blank=True)

    def __unicode__(self):
        return self.name
    def __init__(self,*args,**kw):
        super(DepartmentBase,self).__init__(*args,**kw)
        self._org_par=self.par

    def save(self, *args,**kw):   
        rt= super(DepartmentBase,self).save(*args,**kw)
        if self._org_par !=self.par or not self.par_chain:
            self._org_par=self.par
            self.update_parent_chain()  
        return rt
    
    def update_parent_chain(self):
        par =self.par
        ls=[self.pk]
        while par:
            ls.append(par.pk)
            par=par.par
        ls=reversed([str(x) for x in ls])
        self.par_chain='.'.join(ls)
        self.save()
        for depart in self.childs.all():
            depart.update_parent_chain() 
    
    class Meta:
        abstract = True
    
def get_admin(Department):
    class DepartmentForm(ModelFields):
        class Meta:
            model=Department
            exclude=['par']
            
    class DepartmentPage(object):
        template='common/department.html'
        def __init__(self,request):
            self.request=request
            
        def get_context(self):
            departform = DepartmentForm(crt_user=self.request.user)
            self.ctx={
                #'app':'',
                'heads':departform.get_heads(),
                'can_edit':departform.permit.can_add(),
                #'work_editable':bool( departform.permit.changeable_fields()),
                #'work_can_add':departform.permit.can_add(),
                #'dir_heads':indexform.get_heads(),
                #'dir_editable':bool(indexform.permit.changeable_fields()),
                #'dir_can_add':indexform.permit.can_add(),
            }
            return self.ctx    
        
    engin_dict={
        'department':DepartmentPage,
    }
    return locals()