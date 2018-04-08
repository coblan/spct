# encoding:utf-8

from __future__ import unicode_literals

from helpers.director.shortcut import ModelTable,TablePage,FormPage,ModelFields,RowFilter
from ..models import WorkRecord
from helpers.case.organize.valid_depart import ValidDepart
from helpers.case.organize.workpermit import has_depart_permit
from helpers.director.db_tools import sim_dict
from helpers.case.organize.workpermit import DepartModelPermit


class WorkRecordFilter(RowFilter):
    names=['status','work','ex_span']
    range_fields=[{'name':'create_time','type':'date'}]
    model=WorkRecord 

class WorkList(ModelTable):
    """
    拥有 work.read_all 权限的人，查看本部门的所有工作列表
    """
    model=WorkRecord
    filters=WorkRecordFilter
    
    def inn_filter(self, query):
        employee=self.crt_user.employee_set.first()
        valid_depart=WorkReadValidDepart(employee,self.kw.get('_depart'))
        query_depart=valid_depart.get_query_depart()
        return query.filter(depart__in=query_depart).order_by('-id')
    
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
    
    # def dict_row(self, inst):
        # return {
            # 'emp':sim_dict(inst.emp.baseinfo),
            # 'work':unicode(inst.work),
            # 'depart':unicode(inst.depart)
        # }
  
  

    

class WorkReadValidDepart(ValidDepart):
    data_key='work_readall'
    
    def get_allowed_depart(self):
        allowed_depart=[]
        for depart in self.employee.depart.all():
            if has_depart_permit(self.employee, 'work.read_all', depart):
                allowed_depart.append(depart)
        return allowed_depart
    

class WorkListPage(TablePage):
    tableCls=WorkList
    template='work/work_list_f7.html'
    def get_context(self):
        ctx=super(WorkListPage,self).get_context()
        employee=self.request.user.employee_set.first()
        valid_depart=WorkReadValidDepart(employee,self.request.GET.get('_depart'))
        ctx=valid_depart.get_context(ctx)
        return ctx


class WorkListForm(ModelFields):
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
        
        self.valid_depart= WorkReadValidDepart(employee,self.kw.get('depart_pk'))
        self.permit=DepartModelPermit(WorkRecord,employee, self.valid_depart.get_crt_depart())
    
    def get_heads(self):
        heads=super(WorkListForm,self).get_heads()
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
            head['readonly']=True
        return heads

class WorkListFormPage(FieldsPage):
    fieldsCls=WorkListForm
    template='work/work_list_form_f7.html'


