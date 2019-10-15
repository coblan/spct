from helpers.authuser.forms import LoginForm
from helpers.director.shortcut import director_view,get_request_cache
from .models import TbUserex
from django.utils import timezone
from .redisInstance import redisInst6
from helpers.authuser.validate_code import code_and_url
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect

class Login(object):
   
    @staticmethod
    @director_view('do_login')
    def run(row):
        try:
            user = User.objects.get(username=row.get('username'))
            inst,_ = TbUserex.objects.get_or_create(userid= user.pk)
            if not inst.passwordexpiretime or inst.passwordexpiretime < timezone.now():
                return {'success':False,'action':'cfg.toast("用户密码已经过期，请重新设置密码");setTimeout(function(){location="/accounts/pswd?username=%s"},2000)'%row.get('username')}
        except User.DoesNotExist:
            pass
            #return {'success':False,'errors':{'username':['用户名不存在']}}
        loger = Login(row)
        if not loger.check_code():
            code,url = code_and_url()
            redisInst6.set(loger.code_key,code,ex=60*3)
            return {'success':False,'errors':{'validate_code':['验证码错误']},'validate_img':url}
        rt= loger.check_and_login()
        return rt
        
    
    def __init__(self,row):
        self.request = get_request_cache()['request']
        self.row = row
        
        self.code_key = 'user_%(username)s_validate_code'%self.row
        self.count_key = 'user_%(username)s_login_count'%self.row
    
    def check_code(self):
       
        if  redisInst6.get(self.code_key):
            if  redisInst6.get(self.code_key).lower() != self.row.get('validate_code').lower():
                return False
        return True
    
    def check_and_login(self):
        form=LoginForm({'username':self.row.get('username'),'password':self.row.get('password')})
        if form.is_valid():
            user= auth.authenticate(username=self.row.get('username'),password=self.row.get('password'))
            return self.login(user)
        else:
            return self.export_error(form.errors)
    
    def login(self,user):
        if not self.row.get('auto_login'):
            self.request.session.set_expiry(0)
        auth.login(self.request, user)
        
        redisInst6.delete(self.count_key)
        redisInst6.delete(self.code_key)
        return {'success':True,'token':self.request.session.session_key}
        
    
    def export_error(self,errors):
        dc ={}
        if not redisInst6.get(self.count_key) :
            redisInst6.set(self.count_key,1,ex=60*60*2)
        else:
            old_value = redisInst6.get(self.count_key) 
            redisInst6.set(self.count_key,int(old_value)+1,ex=60*60*2)
            
        if int( redisInst6.get(self.count_key) ) >5:
            code,url = code_and_url()
            redisInst6.set(self.code_key,code,ex=60*3)
            dc.update( {'success':False,'validate_img':url} ) 
        dc.update({
            'errors':errors
        })
        return dc
    

class ChangePswdLogic(object):
    @staticmethod
    @director_view('authuser.changepswd')
    def changepswd(row):
        changer = ChangePswdLogic(row)
        if changer.check_code():
            return changer.gen_code()
        
        infoerror= changer.get_info_error()
        if infoerror:
            dc = changer.export_code()
            dc.update({'success':False,'errors':infoerror})
            return dc
        else:
            changer.user.set_password(row.get('first_pswd'))
            changer.user.save()
            changer.after_change()
            return {'success':True}
        
        
    
    def __init__(self,row):
        self.request = get_request_cache()['request']
        self.row = row
        try:
            self.user = User.objects.get(username =row.get('username'))
        except User.DoesNotExist:
            raise UserWarning('用户名不存在')
        
        self.code_key = 'user_%(username)s_validate_code'%self.row
        self.count_key = 'user_%(username)s_login_count'%self.row
    
    def check_code(self):
        if  redisInst6.get(self.code_key):
            if not self.row.get('validate_code') or  redisInst6.get(self.code_key).lower() != self.row.get('validate_code').lower():
                return False
        return True

    def gen_code(self):
        code,url = code_and_url()
        redisInst6.set(self.code_key,code,ex=60*3)
        return {'success':False,'errors':{'validate_code':['验证码错误']},'validate_img':url}
    
    def get_info_error(row):
        errors ={}
        if row.get('first_pswd')!=row.get('second_pswd'):
            errors.update(
                {'second_pswd':['second password not match']}
            )
        elif not row.get('first_pswd'):
            errors.update(
                {'first_pswd':['must input password']}
            )
    
        try:
            md_user= User.objects.get(username =row.get('username'))
        except User.DoesNotExist:
            raise UserWarning('用户名不存在')
        if md_user.check_password(row.get('old_pswd')):
            pass 
        else:
            errors.update(
                {'old_pswd':['当前密码不匹配']}
            )
       
        return errors
    
    def export_code(self):
        dc ={}
        if not redisInst6.get(self.count_key) :
            redisInst6.set(self.count_key,1,ex=60*60*2)
        else:
            old_value = redisInst6.get(self.count_key) 
            redisInst6.set(self.count_key,int(old_value)+1,ex=60*60*2)
            
        if int( redisInst6.get(self.count_key) ) >5:
            code,url = code_and_url()
            redisInst6.set(self.code_key,code,ex=60*3)
            dc.update( {'validate_img':url} ) 
        return dc
    
    def after_change(self):
        redisInst6.delete(self.count_key)
        redisInst6.delete(self.code_key)

    
#@director_view('authuser.changepswd')
#def changepswd(row):
    #if row.get('first_pswd')!=row.get('second_pswd'):
        #return  {'errors':{'second_pswd':['second password not match']}}
    #elif not row.get('first_pswd'):
        #return {'errors':{'first_pswd':['must input password']}}
    #try:
        #md_user= User.objects.get(username =row.get('username'))
    #except User.DoesNotExist:
        #raise UserWarning('用户名不存在')
    #if md_user.check_password(row.get('old_pswd')):
        #md_user.set_password(row.get('first_pswd'))
        #md_user.save()
        #dc={'status':'success'}
    #else:
        #dc={'errors':{'old_pswd':['当前密码不匹配']}}

    #return dc