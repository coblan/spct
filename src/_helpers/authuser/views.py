# encoding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from helpers.func.network.ajax_router import ajax_router
# Create your views here.

@ensure_csrf_cookie
def login(request):
    if request.method=='GET':
        next_url=request.GET.get('next','/')
        dc={
            'next':next_url,
            'regist_url':reverse('regist'),
            
        }
        return render(request,'authuser/login.html',context=dc)
  
    elif request.method=='POST':
        return ajax_router(request,auth_ajax.get_globe())
    
@ensure_csrf_cookie
def regist_user(request):
    if request.method=='GET':
        
        heads= form_to_head(AuthForm())
        for head in heads:
            if head.get('name') in ['password','pas2']:
                head['type']='password'
        dc={
            'login_url':reverse('login'),
            'heads':json.dumps( heads )
        }
        return render(request,'authuser/regist.html',context=dc)
    elif request.method=='POST':
        return ajax_router(request,auth_ajax.get_globe()) 


def logout(request):
    next = request.GET.get('next','/')
    next=urllib.unquote(next)
    auth.logout(request)
    return redirect(next) 

@ensure_csrf_cookie
@login_required
def change_pswd(request):
    pk = request.GET.get('uid')
    if pk:
        name=User.objects.get(pk=pk).username
    else:
        pk = request.user.pk
        name=request.user.username
        
    if request.method=='GET':
        dc={
            'login_url':reverse('login'),
            'username':name,
            'uid':pk
        }        
        return render(request,'authuser/changepswd.html',context=dc)
    elif request.method=='POST':
        #try:
        return ajax_router(request,auth_ajax.get_globe())  
        #except UserWarning as e:
            #return HttpResponse(json.dumps({'status':'fail','msg':str(e)}),content_type="application/json")
            

def trival(request):
    pass

def forget(request):
    return render(request,'authuser/forget.html')