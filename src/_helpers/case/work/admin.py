# encoding:utf-8

from __future__ import unicode_literals
from __future__ import absolute_import
from django.contrib import admin
from .models import Work,WorkRecord,Index
from helpers.director.shortcut import page_dc,FormPage,\
     TablePage,ModelTable,ModelFields,model_dc,RowFilter,permit_list,has_permit,ModelPermit,PageNum
     
from django import forms
from .pages.work_list import WorkListPage,WorkListFormPage
from .models import Department
from helpers.director.db_tools import to_dict
from helpers.case.organize.workpermit import DepartModelPermit
from django.core.exceptions import PermissionDenied
from helpers.case.organize.valid_depart import ValidDepart



# class DepartWorkTablePageMixin(object):
    # """tablepage mixin"""
    # def get_allowed_depart(self,employee,user):
        # return True
    
    # def get_context(self):
        # ctx=super(DepartWorkTablePageMixin,self).get_context()
        # employee=self.crt_user.employee_set.first()
        # allowed_departs=self.get_allowed_depart(employee,self.crt_user)
        # if not allowed_departs:
            # raise PermissionDenied,'no deparment allowed'
        # ctx['depart_list']=[{'pk':x.pk,'label':unicode(x)} for x in allowed_departs]
        
        # if self.request.GET.get('_depart'):
            # depart= Department.objects.get(pk=self.request.GET.get('_depart'))
            # if depart in allowed_departs:
                # ctx['crt_depart']=depart.pk
        # else:
            # ctx['crt_depart']=allowed_departs[0].pk
        # return ctx  
    
# Register your models here.
class IndexForm(ModelFields):
    class Meta:
        model=Index
        fields=['name']

class WorkForm(ModelFields):
    class Meta:
        model=Work
        exclude=['par']
    

    
    def get_heads(self):
        heads= super(WorkForm,self).get_heads()
        for head in heads:
            if head.get('name')=='desp_img':
                head['type']='picture'
                head['config']={
                    'crop':True,
                'aspectRatio': 1,
                'size':{'width':250,'height':250}
                }
        return heads

class WorkFormPage(FieldsPage):
    fieldsCls=WorkForm

class WorkIdexForm(ModelFields):
    class Meta:
        model=Index
        exclude=['par']
        
class WorkIndexFormPage(FieldsPage):
    fieldsCls=WorkIdexForm
    
class WorkTable(ModelTable):
    model=Work
    def dict_row(self, inst):
        rt_dc={}
        if inst.desp_img:
            rt_dc['desp_img']='<img src="%s" width="30"/>'%inst.desp_img
        if inst.par:
            rt_dc['par']=unicode(inst.par)
        return rt_dc

class WorkTablePage(TablePage):
    tableCls=WorkTable

# class DepartWorkFromMixin(object):
    # def __init__(self,*args,**kw):
        # self.request=kw.pop('request',None)
        # super(DepartWorkFromMixin,self).__init__(*args,**kw)
        

class WorkRecordForm(ModelFields):
    class Meta:
        model=WorkRecord
        exclude=[]
    
    @classmethod
    def parse_request(cls, request):
        pk=request.GET.get('pk')
        depart_pk = request.GET.get('_depart')
        return cls(pk=pk,crt_user=request.user,depart_pk=depart_pk) 
    
    def custom_permit(self):
        employee=self.crt_user.employee_set.first()

        self.valid_depart= WorkCheckValidDepart(employee,self.kw.get('depart_pk'))
        self.permit=DepartModelPermit(WorkRecord,employee, self.valid_depart.get_crt_depart())    
    #@classmethod
    #def parse_request(cls, request):
        #pk=request.GET.get('pk')
        #depart_pk = request.GET.get('_depart')
        #return cls(pk=pk,crt_user=request.user,depart_pk=depart_pk) 
    
    #def custom_permit(self):
        #employee=self.crt_user.employee_set.first()
        #if self.kw.get('depart_pk'):
            #self.valid_depart= WorkCheckValidDepart(employee,self.kw.get('depart_pk'))
            #self.permit=DepartModelPermit(WorkRecord,employee, self.valid_depart.get_crt_depart())
        #else:
            #return super(WorkRecordForm,self).custom_permit()
        
    def get_heads(self):
        heads= super(WorkRecordForm,self).get_heads()
        for head in heads:
            if head.get('name')=='desp_img':
                head['type']='picture'
                head['config']={
                    'crop':True,
                'aspectRatio': 1,
                'size':{'width':250,'height':250}
                }
            elif head['name']=='finish_time':
                head['type']='date'            
        return heads  

    def clean(self):
        cleaned_data = super(WorkRecordForm,self).clean()
        if not has_permit(self.crt_user,'workrecord.check_all'):
            if self.instance.status!='waiting': 
                raise forms.ValidationError('you have no permition to edit this workrecord again')
    
    def save_form(self):
        rt=super(WorkRecordForm,self).save_form()
        if self.instance.status=='pass':
            checker= self.crt_user.employee_set.first()
            self.instance.checker= checker 
            self.instance.save()
        return rt
    #def can_access(self):
        #access = super(WorkRecordForm,self).can_access()
        #if not has_permit(self.crt_user,'workrecord.check_all'):
            #if self.instance.status!='waiting':

    #def clean(self,*args,**kw):
        #cleaned_data = super(WorkRecordForm, self).clean()
        #if not cleaned_data.get('tmp') and not cleaned_data.get('work'):
            #self.add_error('work', '当非临时工作时，必须选择工时种类')



class WorkRecordFormPage(FieldsPage):
    fieldsCls=WorkRecordForm

class WorkPageNum(PageNum):
    perPage=5
    
class WorkRecordFilter(RowFilter):
    names=['status','work','ex_span']
    range_fields=[{'name':'create_time','type':'date'}]
    model=WorkRecord 

class WorkRecordTable(ModelTable):
    model=WorkRecord
    filters=WorkRecordFilter
    pagenator=WorkPageNum
    
    def custom_permit(self):
        employee=self.crt_user.employee_set.first()
        self.valid_depart= WorkCheckValidDepart(employee,depart_pk=self.kw.get('_depart'))
        self.permit=DepartModelPermit(WorkRecord,employee, self.valid_depart.get_crt_depart())

    
    def inn_filter(self, query):
        query =super(WorkRecordTable,self).inn_filter(query)
        depart_list=self.valid_depart.get_query_depart()
        return query.filter(check_depart__in=depart_list).order_by('-id')

    def dict_row(self,inst):
        dc={}
        if inst.work:
            dc.update({
                'work_desp_img': inst.work.desp_img,
                # 'work':unicode(inst.work),
                'work_span':inst.work.span,
            })
        if inst.checker:
            dc.update({
                'checker_name':unicode(inst.checker)
            })
        dc.update({
            # 'emp':unicode(inst.emp),
            'desp_img':inst.desp_img,            
        })
        return dc


class WorkCheckValidDepart(ValidDepart):
    data_key='work_check'
    def get_allowed_depart(self):
        allowed_depart=[]
        for depart in self.employee.depart.all():
            permit = DepartModelPermit(WorkRecord, self.employee, department=depart)
            if 'status' in permit.changeable_fields():
                allowed_depart.append(depart)
        return allowed_depart  

class WorkRecordTablePage(TablePage):
    tableCls=WorkRecordTable
    #def __init__(self,request):
        #self.request=request
        #self.table = self.tableCls.parse_request(request)
        #self.crt_user=request.user
        #employee=self.crt_user.employee_set.first()
        #self.valid_depart= WorkCheckValidDepart(employee,self.request.GET.get('_depart'))
        #self.permit=DepartModelPermit(WorkRecord,employee, self.valid_depart.get_crt_depart())
        
    def get_context(self):
        ctx = super(WorkRecordTablePage,self).get_context()
        ctx=self.table.valid_depart.get_context(ctx)
        return ctx
    
    def get_label(self):
        return '工作审批列表'
    
    #def get_cache_control(self):
        #return dict(max_age=3600)

class WorkRecordTablePageWX(WorkRecordTablePage):
    template='work/workrecord_f7.html'

    #template='workload/m_workrecord.html'

class WorkRecordFormPageWX(WorkRecordFormPage):
    template='work/workrecord_form_f7.html'

def pop_depart(depart,event):
    while depart.par:
        if depart.departmanage:
            events= depart.departmanage.recv_event.split(',')
            if event in events:
                return depart
        depart=depart.par
    return depart
        

class WRselfForm(ModelFields):
    readonly=['status']
    class Meta:
        model=WorkRecord
        exclude=['check_depart','depart']

    def custom_permit(self):
        employee=self.crt_user.employee_set.first()
        
        self.valid_depart= WRselfValidDepart(employee,self.kw.get('_depart'))
        self.permit=DepartModelPermit(WorkRecord,employee, self.valid_depart.get_crt_depart())

    def get_row(self):

        #if not self.instance.pk:
        # 员工创建新workrecord时，自动添加上
        emp=self.crt_user.employee_set.first()
        self.instance.emp= emp
        
        
        return super(WRselfForm,self).get_row()
     
    def get_heads(self):
        heads= super(WRselfForm,self).get_heads()
        for head in heads:
            if head.get('name')=='desp_img':
                head['type']='picture'
                head['config']={
                    'crop':True,
                'aspectRatio': 1,
                'size':{'width':250,'height':250}
                }
            elif head['name']=='finish_time':
                head['type']='date'
            elif head['name']=='emp':
                head['readonly']=True
                
        if self.instance.status =='pass':
            for head in heads:
                head['readonly']=True

        return heads 

    def save_form(self):
        rt = super(WRselfForm,self).save_form()
        depart=self.valid_depart.get_crt_depart()
        if depart:
            self.instance.depart=depart
            check_depart=pop_depart(depart,self.instance.sub_type)
            self.instance.check_depart=check_depart 
            self.instance.save()
        return rt
    

class WRselfFormPage(FieldsPage):
    template='work/workself_form_f7.html'
    fieldsCls=WRselfForm

class WRselfTable(ModelTable):
    model=WorkRecord
    filters=WorkRecordFilter
    
    def custom_permit(self):
        employee=self.crt_user.employee_set.first()
        self.valid_depart= WRselfValidDepart(employee,self.kw.get('_depart'))
        self.permit=DepartModelPermit(WorkRecord,employee, self.valid_depart.get_crt_depart())   
        
    def inn_filter(self, query):
        query =super(WRselfTable,self).inn_filter(query)
        employee=self.crt_user.employee_set.first()
        valid_depart=WRselfValidDepart(employee,self.kw.get('_depart'))
        depart=valid_depart.get_crt_depart()
        # if self.kw.get('_depart'):
            # depart=Department.objects.get(pk=self.kw.get('_depart'))
        # else:
            # emp=self.crt_user.employee_set.first()
            # depart=emp.depart.first()
        return query.filter(emp__user=self.crt_user,depart=depart).order_by('-id')
    
    def dict_row(self, inst):
        return {
            'work': unicode(inst.work),
            'work_desp_img':inst.work.desp_img
        }

def get_depart_can_submit_work(employee):
    allowed_departs=[]
    for depart in employee.depart.all():
        permit = DepartModelPermit(WorkRecord, employee,department=depart)
        if permit.can_add():
            allowed_departs.append(depart)
    return allowed_departs
            

class WRselfValidDepart(ValidDepart):
    data_key='work_self'
    def get_allowed_depart(self):
        return get_depart_can_submit_work(self.employee)

class WRselfTablePage(TablePage):
    tableCls=WRselfTable
    template='work/workself_f7.html'
    
    def __init__(self,request):
        self.request=request
        self.table = self.tableCls.parse_request(request)
        self.crt_user=request.user
        employee=self.crt_user.employee_set.first()
        self.valid_depart=WRselfValidDepart(employee,self.request.GET.get('_depart'))
        self.permit= DepartModelPermit(WorkRecord,employee, self.valid_depart.get_crt_depart())
        
    def get_context(self):
        ctx=super(WRselfTablePage,self).get_context()
        ctx.update( self.valid_depart.get_context() )
        return ctx
    #def get_allowed_depart(self,employee,user):
        #return get_depart_can_submit_work(employee, user)
    # def get_context(self):
        # ctx=super(WRselfTablePage,self).get_context()
        # employee=self.crt_user.employee_set.first()
        # allowed_departs=[]
        # for depart in employee.depart.all():
            # permit = WorkModelPermit(WorkRecord, self.crt_user,department=depart)
            # if permit.can_add():
                # allowed_departs.append(depart)
        # if not allowed_departs:
            # raise PermissionDenied,'not deparment allowed'
        # ctx['depart_list']=[to_dict(x) for x in allowed_departs]
        
        # if self.request.GET.get('_depart'):
            # depart= Department.objects.get(pk=self.request.get('_depart'))
            # if depart in allowed_departs:
                # ctx['crt_depart']=to_dict(depart)
        # else:
            # ctx['crt_depart']=allowed_departs[0]
        # return ctx
    
    def get_label(self):
        emp=self.request.user.employee_set.first()
        return '%s的工作提交记录'% emp



class WorkIndex(object):
    template='work/workindex.html'
    def __init__(self,request):
        self.request=request

    def get_context(self):
        workform = WorkForm(crt_user=self.request.user)
        indexform=IndexForm(crt_user=self.request.user)
        self.ctx={
            'app':'workload',
            'heads':workform.get_heads(),
            'work_editable':bool( workform.permit.changeable_fields()),
            'work_can_add':workform.permit.can_add(),
            'dir_heads':indexform.get_heads(),
            'dir_editable':bool(indexform.permit.changeable_fields()),
            'dir_can_add':indexform.permit.can_add(),
        }
        return self.ctx


class WorkIndexWX(WorkIndex):
    template='work/workindex_f7.html'

permit_list.append(WorkRecord)
permit_list.append(Work)
permit_list.append(Index)
permit_list.append({'name':'work','label':'work.工作SP','fields':[
    {'name':'check_all','label':'审批工作','type':'bool'},
    {'name':'read_all','label':'查看工作','type':'bool'},
]})


model_dc[Work]={'fields':WorkForm}
model_dc[WorkRecord]={'fields':WorkRecordForm}
model_dc[Index]={'fields':IndexForm}

page_dc.update({
    'work.workindex':WorkIndex,
    'work.workindex.f7':WorkIndexWX,

    'work.work':WorkTablePage,   # 平铺的 work，而 workindex 树状的work 
    'work.work.wx':WorkTablePage,

    'work.work.edit':WorkFormPage,
    'work.work.f7.edit':WorkFormPage,
    'work.index.f7.edit':WorkIndexFormPage,

    'work.workrecord':WorkRecordTablePage,
    'work.workrecord.f7':WorkRecordTablePageWX,

    'work.workrecord.edit':WorkRecordFormPage,
    'work.workrecord.f7.edit':WorkRecordFormPageWX,

    'work.wkself.f7':WRselfTablePage,
    'work.wkself.f7.edit':WRselfFormPage,
    
    'work.worklist.f7':WorkListPage,
    'work.worklist.f7.edit':WorkListFormPage,
})