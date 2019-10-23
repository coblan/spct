from helpers.authuser.forms import LoginForm
from helpers.director.shortcut import director_view,get_request_cache
from .models import TbUserex,TbBackendwhiteip,TbBackendloginlog,TbIpdata
from django.utils import timezone
from .redisInstance import redisInst6
from helpers.authuser.validate_code import code_and_url
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
import json
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from .riskcontrol.white_ip_rangelist import ip2num
from django.conf import settings
import re

import logging
general_log = logging.getLogger('general_log')

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
        if  not loger.check_ip():
            raise UserWarning('访问地址不在可用范围')
        
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
    
    def check_ip(self):
        ip = self.get_ip()
        general_log.info('ip=%s 登录'%ip)
        if not getattr(settings,'ADMIN_USER_CHECK_IP',False):
            return True
        else:
            ipnum = ip2num(ip)
            return TbBackendwhiteip.objects.filter(startipnum__lte=ipnum,endipnum__gte=ipnum,iswork=True).exists()
    
    def get_ip(self):
        request = get_request_cache()['request']
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip
    
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
            self.request.session['auto_login'] = False
        else:
            self.request.session['auto_login'] = True
            self.request.session.set_expiry(settings.LOGIN_SPAN) # 2小时过期
            
        auth.login(self.request, user)
        redisInst6.delete(self.count_key)
        redisInst6.delete(self.code_key)
        ip = self.get_ip()
        ipnum = ip2num(ip)
        inst = TbIpdata.objects.filter(sartipnum__lte=ipnum,endipnum__gte = ipnum).first()
        if inst:
            area = inst.area
        else:
            area = ''
        TbBackendloginlog.objects.create(userid=user.pk,username=user.username,ipaddress=ip,area=area)
        
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
        if not changer.check_code():
            return changer.wrap_fail_info({
                'errors':{'validate_code':['验证码错误']}
            })
        
        if not re.search( '^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$',row.get('first_pswd') ) :
            return changer.wrap_fail_info({
                'errors':{'first_pswd':['密码必须为8到16位的字母与数字的组合!']}
            })
        
        infoerror= changer.get_info_error(row)
        if infoerror:
            return changer.wrap_fail_info({
                'errors':infoerror
            })

        else:
            userinfo,_ = TbUserex.objects.get_or_create(userid=changer.user.pk)      
            used_passwd= []
            if userinfo.usedpassword:
                used_passwd = json.loads(userinfo.usedpassword)
                for old_ps in used_passwd:
                    if check_password(row.get('first_pswd'),old_ps):
                        return changer.wrap_fail_info({
                            'errors':{'first_pswd':['新密码已经被使用过']}
                        })
            changer.user.set_password(row.get('first_pswd'))
            changer.user.save()
            userinfo.passwordexpiretime = timezone.now() + timezone.timedelta(days=settings.LOGIN_PSWD_EXPIRE)
            used_passwd.append(changer.user.password)
            if len(used_passwd )>3:
                userinfo.usedpassword=json.dumps(used_passwd[-4:-1])
            else:
                userinfo.usedpassword=json.dumps(used_passwd)
            userinfo.save()
            
            changer.after_change()
            return {'success':True}
            
        
    def wrap_fail_info(self,infodc):
        if not redisInst6.get(self.count_key) :
            redisInst6.set(self.count_key,1,ex=60*60*2)
        else:
            old_value = redisInst6.get(self.count_key) 
            redisInst6.set(self.count_key,int(old_value)+1,ex=60*60*2)
            
        if int( redisInst6.get(self.count_key) ) >5:
            code,url = code_and_url()
            redisInst6.set(self.code_key,code,ex=60*3)
            infodc.update( {'validate_img':url} )
        infodc.update({
            'success':False
        })
        return infodc
        
    
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
    
    def get_info_error(self,row):
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