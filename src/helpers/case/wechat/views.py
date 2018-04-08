# encoding:utf-8
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import redirect
import json
from .wepay.jsapi import JSApiWePay
from .wepay.appapi import APPApiWePay
from .fuwu import FuWuHao

def pay_replay(request):
    pay = JSApiWePay()
    xml_str = pay.reply(request)
    return HttpResponse(xml_str,content_type="text/xml")

def wepay_make_order(request):
    """
    GET:
    jsapi: /wechat/pay/new_order?pay_type=jsapi&openid=oIvmdwi8HWePf8rXFDA-jOpQL5uE
    appapi:/wechat/pay/new_order?pay_type=app
    """
    pay_type=request.GET.get('pay_type')
    if pay_type=='jsapi':
        pay = JSApiWePay()
        dc = pay.make_order(request)
    elif pay_type=='app':
        pay=APPApiWePay()
        dc=pay.make_order(request)
    return HttpResponse(json.dumps(dc),content_type="application/json") 

def recv_code_fuwu(request):
    fuwu=FuWuHao()
    fuwu.rec_code(request)
    return redirect(fuwu.next_url)

def test_view(request):
    """
    其他模块调用服务号登录，就是从这里开始。
    """
    fuwu=FuWuHao()
    url = fuwu.get_redirect_url(request)
    print(url)
    return redirect(url)

def user_info(request):
    if request.user.is_authenticated():
        return HttpResponse(request.user.username)
    else:
        return HttpResponse('not login')