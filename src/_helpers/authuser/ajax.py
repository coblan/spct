# encoding:utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib import auth 
from helpers.director.model_func.dictfy import from_dict
from .forms import AuthForm,LoginForm
from helpers.director.access.permit import has_permit

def get_global():
    return globals()


def logout(request):
    auth.logout(request)
    return {'status':'success'}


def do_login(username,password,request,auto_login=False):
    """
    登录函数：
    """
    form=LoginForm({'username':username,'password':password})
    
    if form.is_valid():
        user= auth.authenticate(username=username,password=password)
        if not auto_login:
            request.session.set_expiry(0)
        auth.login(request, user)
        return {'status':'success'}
    else:
        return {'errors':form.errors}

def do_login_old(username,password,request):
    """
    原来的登录函数
    """
    form=LoginForm({'username':username,'password':password})
    if form.is_valid():
        user= auth.authenticate(username=username,password=password)
        auth.login(request, user)
        return {'status':'success'}
    else:
        return {'errors':form.errors}
    #if user: 
        #if user.is_active:  
            #auth.login(request, user)
            #return {'status':'success'}
        #else:
            #raise UserWarning,'[do_login] user has been disabled'
    #else:
        #user=get_or_none(User,username=name)
        #if user:
            #raise UserWarning,'[do_login] user exist,but password not match'
        #else:
            #raise UserWarning,'[do_login] user not exist'
    #raise UserWarning,'[do_login] user or password not match'  

def registe(info):
    form = AuthForm(info)
    if form.is_valid(): 
        user=from_dict(form.cleaned_data,User)
        user.set_password(user.password)
        #user=User.objects.create_user(username=username,password=password)
        user.is_active=True
        user.save()
        return {'status':'success'}  
    else:
        return {'errors':form.errors}
    #try:
        #User.objects.get(username=username)
        #raise UserWarning,'[registe] username has exist'
    #except User.DoesNotExist:
        #user=User.objects.create_user(username=username,password=password)
        #user.is_active=True
        #user.save()
        #return {'status':'success'}
        #form=StudioForm(studio)
        #if form.is_valid():
            #studio.update(form.cleaned_data )
            #studio_obj=from_dict(studio)
            #studio_obj.save()
            #freeze_studio_with_celery(studio_obj)
            #return {'status':'success'}
        #else:
            #return {'errors':form.errors}

def changepswd(user,row):
    if row.get('first_pswd')!=row.get('second_pswd'):
        return  {'errors':{'second_pswd':['second password not match']}}
    elif not row.get('first_pswd'):
        return {'errors':{'first_pswd':['must input password']}}
        
    md_user= User.objects.get(pk=row.get('uid'))
    if user.is_superuser or has_permit(user,"myauth.modify_other_pswd")  or md_user.check_password(row.get('old_pswd')):
        md_user.set_password(row.get('first_pswd'))
        md_user.save()
        dc={'status':'success'}
    else:
        dc={'errors':{'old_pswd':['old password not match']}}

    return dc
    

