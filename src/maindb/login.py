from helpers.authuser.forms import LoginForm
from helpers.director.shortcut import director_view,get_request_cache
from .models import TbUserex
from django.utils import timezone
from .redisInstance import redisInst6
from helpers.authuser.validate_code import code_and_url

#@director_view('do_login')
def custome_do_login(username,password,auto_login=False):
    request = get_request_cache()['request']
    form=LoginForm({'username':username,'password':password})
    
    code_key = 'user_%s_validate_code'%username
    if  redisInst6.get(code_key):
        if redisInst6.get(code_key) != row.validate_code:
            code,url = code_and_url()
            redisInst6.set(code_key,code,ex=60*3)
            return {'success':True,'msg':'验证码错误','validate_img':url}

    count_key = 'user_%s_login_count'%username
    if form.is_valid():
        #user= auth.authenticate(username=username,password=password)
        if not auto_login:
            request.session.set_expiry(0)
        auth.login(request, form.instance)
        
        redisInst6.delete(count_key)
        redisInst6.delete(code_key)
        return {'success':True,'token':request.session.session_key}
    else:
        dc ={}
        if not redisInst6.get(count_key) :
            redisInst6.set(count_key,1,ex=60*60*2)
        else:
            old_value = redisInst6.get(count_key) 
            redisInst6.set(count_key,old_value+1,ex=60*60*2)
            
        if redisInst6.get(count_key) :#>5:
            code,url = code_and_url()
            redisInst6.set(code_key,code,ex=60*3)
            dc.update( {'success':False,'validate_img':url} ) 
        dc.update({
            'errors':form.errors
        })
        return dc
    
    
    #exinfo , _ = TbUserex.objects.get_or_create(userid=user.pk)
          #if not exinfo.passwordexpiretime or timezone.now() > exinfo.passwordexpiretime:
            #pass