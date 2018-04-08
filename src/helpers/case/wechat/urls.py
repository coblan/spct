"""
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'pay/reply',views.pay_replay,name='wepay_relay'),
    url(r'pay/new_order',views.wepay_make_order),
    url(r'^rec_code$',views.recv_code_fuwu),
    
    url(r'^test$',views.test_view),
    url(r'^print_username/?$',views.user_info)
]
