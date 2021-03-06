
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from ..models import TbUserex
from django.utils import timezone
from django.shortcuts import redirect

class PasswordExpire(MiddlewareMixin):

    def process_request(self, request):
        if request.get_full_path() in ['/accounts/pswd','/d/ajax']:
            return 
        if request.user and request.user.is_authenticated():
            inst,_ = TbUserex.objects.get_or_create(userid= request.user.pk)
            if not inst.passwordexpiretime or inst.passwordexpiretime < timezone.now():
                return redirect('/accounts/pswd')
  
    

        
        
