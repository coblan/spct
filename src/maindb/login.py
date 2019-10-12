from helpers.authuser.forms import LoginForm
from helpers.director.shortcut import director_view,get_request_cache
from .models import TbUserex
from django.utils import timezone
from .redisInstance import redisInst6
from helpers.authuser.validate_code import code_and_url
from django.contrib import auth
from django.contrib.auth.models import User

class Login(object):
   
    @staticmethod
    @director_view('do_login')
    def run(row):
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
    

@director_view('authuser.changepswd')
def changepswd(row):
    if row.get('first_pswd')!=row.get('second_pswd'):
        return  {'errors':{'second_pswd':['second password not match']}}
    elif not row.get('first_pswd'):
        return {'errors':{'first_pswd':['must input password']}}
        
    md_user= User.objects.get(pk=row.get('uid'))
    if md_user.check_password(row.get('old_pswd')):
        md_user.set_password(row.get('first_pswd'))
        md_user.save()
        dc={'status':'success'}
    else:
        dc={'errors':{'old_pswd':['old password not match']}}

    return dc