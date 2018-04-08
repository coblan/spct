# encoding:utf-8
from django.db import models
from django.utils import timezone
import random
from django.contrib.auth.models import User

def get_no():
    a='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return timezone.now().strftime('%Y%m%d%H%M%S')+''.join(random.choice(a) for i in range(8))

class WXOrderBase(models.Model):

    no = models.CharField('内部微信订单号',max_length=300,blank=True)
    transaction_id=models.CharField('微信支付订单号',max_length=300,blank=True)
    time_end=models.CharField('支付完成时间',max_length=300,blank=True)
    total_fee=models.CharField('总金额',max_length=300,blank=True)
    openid=models.CharField('付款人openid',max_length=300,blank=True)
    trade_type=models.CharField('交易类型',max_length=300,blank=True)
    result_code=models.CharField('业务结果',max_length=300,blank=True)
    body=models.CharField('实际商品名称',max_length=300,blank=True)
    detail=models.TextField(verbose_name='详细',blank=True)
    create_time=models.DateTimeField(verbose_name='记录创建时间',auto_now_add=True,null=True)
    last_update_time=models.DateTimeField(verbose_name='记录最后修改时间',auto_now=True,null=True)
    pay=models.CharField('支付情况',max_length=100,blank=True)
    confirmed=models.BooleanField('是否确认',default=False)
    
    
    def __init__(self,*args,**kw):
        super(WXOrderBase,self).__init__(*args,**kw)
        if not self.no:
            self.no= 'WX'+get_no()
    
    class Meta:
        abstract=True
    

#class AccessToken(models.Model):
    #appid=models.CharField('appid',max_length=50,blank=True)
    #token=models.CharField('token',max_length=100,blank=True)
    #update_time=models.CharField('update time',max_length=50,blank=True)

class WxInfo(models.Model):
    user=models.ForeignKey(User,verbose_name='user',blank=True,null=True)
    openid=models.CharField('openid',max_length=30,unique=True)
    head=models.CharField('head',max_length=300,blank=True)
    nickname=models.CharField('nick name',max_length=200,blank=True)
    sex=models.CharField('sex',max_length=10,blank=True)
    province=models.CharField('province',max_length=50,blank=True)
    city=models.CharField('city',max_length=50,blank=True)
    country=models.CharField('country',max_length=50,blank=True)