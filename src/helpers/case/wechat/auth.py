# encoding:utf-8
from __future__ import unicode_literals
from models import CustomerModel,User
from django.contrib.auth import authenticate

class WeChatAuth(object):
    def authenticate(self, openid=None):
        if openid:
            cus = CustomerModel.get_or_add(openid=openid)
            return cus.user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None 