from django.shortcuts import render
from django.contrib.auth.models import User
from helpers.director.db_tools import model_to_head,to_dict
from .models import EmployeeModel,BasicInfo
from .admin import emp_admin
from django.contrib.auth.decorators import login_required
from helpers.director.engine import page
# Create your views here.


@login_required
def my_info(request):
    BasicInfoFields=emp_admin['BasicInfoFields']
    user= request.user
    ctx={}
    emp= EmployeeModel.objects.filter(user=request.user).first()
    if not emp:
        ctx['no_emp']=True
    else:
        bf=BasicInfoFields(instance=emp.baseinfo,crt_user=user,nolimit=True)
        ctx['base_heads']=bf.get_heads()
        ctx['base_row']=bf.get_row()
        ctx['root_page']=page('home.wx')('wx_engine')
    return render(request,'employee/my_info.html',context=ctx)