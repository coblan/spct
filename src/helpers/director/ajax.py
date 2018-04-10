from .models import PermitModel
from .base_data import model_dc
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

import json

from helpers.func.network.download_response import downloadfy_response

from .model_func.wirtedb import permit_save_model
from .model_func.dictfy import name_to_model,model_to_name,to_dict
import io

def get_global():
    return globals()

def save(row,user,request):
    """
    """
    try:
        kw=request.GET.dict()
        field_obj = permit_save_model(user, row,**kw)
        dc = field_obj.get_row()
        return {'status':'success','row':dc}
    except ValidationError as e:
        return {'errors':dict(e)}

def get_row(model_name,pk=None,user=None,**kws):
    model = name_to_model(model_name)
    fields_cls = model_dc[model].get('fields')
    if pk:
        instance = model.objects.get(pk =pk)
        fields_obj = fields_cls(instance=instance,crt_user = user)
    elif kws:
        instance = model.objects.get(**kws)
        fields_obj = fields_cls(instance=instance,crt_user = user)
    else:
        fields_obj =fields_cls(crt_user = user)
    return fields_obj.get_row()

def get_rows(model_name,search_args,user):
    model = name_to_model(model_name)
    table_cls = model_dc[model].get('table')
    table_obj = table_cls.gen_from_search_args(search_args,user)
    return table_obj.get_data_context()
    

def del_rows(rows,user):
    for row in rows:
        model = name_to_model(row.get('_class'))
        fields_cls = model_dc.get(model).get('fields')
        fields_obj = fields_cls(row,crt_user=user)
        fields_obj.del_form()
   
    return rows

def save_group_permit(row,user):
    field_obj = permit_save_model(user, row)
    inst = field_obj.instance
    exist_permitmodel = row.get('permit',[])
    for ee  in inst.permitmodel_set.exclude(pk__in=exist_permitmodel):
        inst.permitmodel_set.remove(ee)
    
    
    
def download_permit(items):
    pk_list=items.split('-')
    pk_list=[x for x in pk_list if x ]
    out=[]
    for permit in PermitModel.objects.filter(pk__in=pk_list):
        out.append({'name':permit.name,'permit':permit.permit,'desp':permit.desp})

    return downloadfy_response(json.dumps(out), 'permits.json')

def upload_permit(request):
    fl = request.FILES['file']
    catch = io.BytesIO()

    for chunk in fl.chunks():
        catch.write(chunk) 
    data=catch.getvalue()
    permits = json.loads(data)
    
    for permit in permits:
        permit_obj,_=PermitModel.objects.get_or_create(name=permit['name'])
        permit_obj.permit=permit['permit']
        permit_obj.desp=permit['desp']
        permit_obj.save() 
    return {'status':'success'}

def download_group(items):
    pk_list=items.split('-')
    pk_list=[x for x in pk_list if x ]
    out=[]
    for gp in Group.objects.filter(pk__in=pk_list):
        out.append({'name':gp.name,'permit':[x.name for x in gp.permitmodel_set.all()]})

    return downloadfy_response(json.dumps(out), 'group.json')   

def upload_group(request):
    fl = request.FILES['file']
    catch = io.BytesIO()

    for chunk in fl.chunks():
        catch.write(chunk) 
    data=catch.getvalue()
    groups = json.loads(data)
    for gp in groups:
        gp_obj,_=Group.objects.get_or_create(name=gp['name'])
        permits=PermitModel.objects.filter(name__in=gp['permit'])
        gp_obj.permitmodel_set.add(*list(permits))
        gp_obj.save()
    return {'status':'success'}