
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from ..models import TbMerchants
from django.utils import timezone
from django.shortcuts import redirect
from helpers.director.shortcut import has_permit
from hello.merchant_user import get_user_merchant 

class MerchantInfo(MiddlewareMixin):

    def process_request(self, request):
        if has_permit(request.user,'-i_am_merchant'):
            request.user.merchant = TbMerchants.objects.get(id = request.user.userprofile.merchantid )
        else:
            request.user.merchant = None
  
