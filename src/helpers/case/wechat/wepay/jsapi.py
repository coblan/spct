# encoding:utf-8
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
import hashlib
import requests
import xmltodict
import random
import time

# proxy = {'https': '127.0.0.1:8087'} 

class JSApiWePay(object):
    """
    生成订单
    ==========
    make_order函数，生成订单
    
    为了引入自定义逻辑，重载:
        def order_create(self,wxorder)
    
    响应微信服务器
    ==============
    reply函数，响应微信服务器
    
    为了自定义逻辑，重载:
        def order_confirmed(self,wxorder):
    """
    APPID=''
    APPSECRET=''
    
    MACHID=''
    APISECERT=''
    WXOrderModel=''

    def __init__(self):
        self.replay_url=reverse('wepay_relay')
    
    def order_create(self,wxorder):
        """
        从self.request里面获取必要信息，将wxorder的信息填写完整
        @必须添加的项
        wxorder.total_fee = 100 # 单位分
  
        """
        wxorder.trade_type = 'JSAPI' 
        wxorder.save()
    
    def make_order(self,request):
        self.request=request
        self.ip=request.META['REMOTE_ADDR']
        self.pay_type=request.GET['pay_type']
        self.openid=request.GET['openid']
        self.reply_full_url=r'%(scheme)s://%(host)s%(path)s'%({'scheme':request.scheme,'host':request.get_host(),'path':self.replay_url})
        
        params= self.make_param()
        resp =self.unify_order(params)
        dc =self.fetch_order_args(resp)
        return dc
        
    
    def make_param(self):
        """
        微信统一下单
        
        params = {
            'appid' : setting.WXPAY_APPID,
            'mch_id' : setting.WXPAY_MACHID,
            'device_info' : 'WEB',
            'nonce_str' : str(int(time.time())),
            'body' : self.meal['meal_name'],
            'detail': self.meal['meal_desc'],
            'out_trade_no' : self.orderno,
            'fee_type' : 'CNY',
            'total_fee' : int(float(self.meal['meal_nowprice'])*100),
            'spbill_create_ip' : (self.request_ip and self.request_ip) or '127.0.0.1',
            'notify_url' : setting.WXPAY_NOTIFY,
            'trade_type' : 'APP'
        }
        """ 


        wxorder = self.WXOrderModel.objects.create()
        self.order_create(wxorder)
        param={
            'appid':self.APPID,
            'mch_id':self.MACHID,
            'device_info' : 'WEB',
            'nonce_str':self.get_nonce_str(),
            'body':wxorder.detail,
            'detail':wxorder.detail,
            'out_trade_no':wxorder.no,
            'fee_type':'CNY',
            'total_fee' : wxorder.total_fee,
            'spbill_create_ip' : self.ip,
            'notify_url':self.reply_full_url,
            'trade_type':wxorder.trade_type,
            'openid':self.openid,
        }
        return param    
    def unify_order(self,params):
        if not 'sign' in params.keys():
            params['sign'] = self.params_sign(params)
        postdata='<xml>'
        for k,v in params.items():
            if v:
                postdata+='<{key}>{value}</{key}>\n'.format(key=k,value=v)
        postdata+='</xml>'
        
        resp = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder',data=postdata.encode('utf-8'))
        
        #ToDo 判断是否是正确的XML，如果是，才继续解析
        resp =xmltodict.parse(resp.content).get('xml')
        return resp
    
    def fetch_order_args(self, resp):
        """
        从微信返回参数中提取 参数给前端，jsapi用
        """
        #resp['code'] = 1
        #resp['msg'] = resp.get('return_msg')      
        #resp['ret'] = (resp.get('return_code') == 'SUCCESS' and 1) or 0
        ret={
            'msg':resp.get('return_msg'),
             }
        
        if resp.get('return_code')!='SUCCESS':
            order_args={}
        else:
            order_args={
                'appId' : self.APPID,
                'package' : 'prepay_id=%s'%resp.get('prepay_id'),
                'nonceStr' : self.get_nonce_str(),
                'timeStamp' : str(int(time.time())),
                'signType':'MD5',
            }
            order_args['paySign']=self.params_sign(order_args)
        ret['order_args'] = order_args        
        return ret
    
    def order_confirmed(self,wxorder):
        """
        根据 wxorder的信息，填写其他相关的数据表，然后保存这些信息。
        """
        pass
    
    def reply(self,request):
        """"""
        self.request=request
        
        notify_data = xmltodict.parse( request.body).get('xml')
        sign=notify_data.pop('sign')
        local_sign=self.params_sign(notify_data)
        ret={
            'return_code':'FAIL',
            'return_msg':'参数错误或缺少参数！'
        }
        if local_sign!=sign:
            ret={
                'return_code':'FAIL',
                'return_msg':'签名失败'
            }            
        elif notify_data.get('return_code')=='SUCCESS':
            self.makesure_order(notify_data)
            ret={
                'return_code':'SUCCESS',
                'return_msg':'OK'
            }
        xml_str='<xml>'
        for k,v in ret.items():
            xml_str+='<{key}><![CDATA[{value}]]></{key}>'.format(key=k,value=v)
        xml_str+='</xml>'
        return xml_str
    
    #def process_order_resp(self,resp):
        #return resp
    
    def makesure_order(self,data):
        """
        微信服务器确认订单支付后，会调用到这个函数
        
        微信可能同时多次通知，为了避免创建多个order，所以加上.原子锁
        """
        no=data.get('out_trade_no')
        with transaction.atomic():
            wxorder = self.WXOrderModel.objects.select_for_update().get(no=no)
            if wxorder.confirmed:
                # 已经生成了内部订单，表示微信已经返回过结果了
                return 
            wxorder.confirmed=True
            wxorder.transaction_id=data.get('transaction_id')
            wxorder.time_end=data.get('time_end')
            #wxorder.total_fee=data.get('total_fee')
            wxorder.openid=data.get('openid')
            wxorder.trade_type=data.get('trade_type')
            wxorder.result_code=data.get('result_code')
            
            if data.get('result_code')=='SUCCESS':
                # get_or_create 是原子操作
                # 避免由于异步问题，造成创建多个order的情况
                
                if wxorder.total_fee <= data.get('total_fee') :
                    wxorder.pay='payed'
                    self.order_confirmed(wxorder)
                else:
                    wxorder.pay='no_enogh_mony'
                
            wxorder.save()
    
    def get_nonce_str(self,length=15):
        a='abcdefghijklmnopqrstuvwxyz'
        a+=a.upper()
        return ''.join([random.choice(a) for i in range(length)])
        
    
    def params_sign(self,params):
        sign_str = ''
        for k,v in sorted(params.items(),key=lambda p:p[0]):
            if v:
                sign_str += '{key}={value}&'.format(key=k,value=v)
        sign_str = sign_str + 'key=' + self.APISECERT
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()    
        

#def get_order(appid,mch_id,body,detail,out_trade_no,total_fee,spbill_create_ip,notify_url,trade_type='JSAPI',nonce_str=None,
              #fee_type='CNY',device_info='WEB',**kw):
    #"""
    #微信统一下单
    
    #params = {
        #'appid' : setting.WXPAY_APPID,
        #'mch_id' : setting.WXPAY_MACHID,
        #'device_info' : 'WEB',
        #'nonce_str' : str(int(time.time())),
        #'body' : self.meal['meal_name'],
        #'detail': self.meal['meal_desc'],
        #'out_trade_no' : self.orderno,
        #'fee_type' : 'CNY',
        #'total_fee' : int(float(self.meal['meal_nowprice'])*100),
        #'spbill_create_ip' : (self.request_ip and self.request_ip) or '127.0.0.1',
        #'notify_url' : setting.WXPAY_NOTIFY,
        #'trade_type' : 'APP'
    #}
    #"""
    #params={
        #'appid' : appid,
        #'mch_id' : mch_id,
        #'device_info' : device_info,
        #'nonce_str' : nonce_str if nonce_str else str(int(time.time())),
        #'body' : body,
        #'detail': detail,
        #'out_trade_no' : self.orderno,
        #'fee_type' : fee_type,
        #'total_fee' : total_fee,
        #'spbill_create_ip' : spbill_create_ip,
        #'notify_url' : notify_url,
        #'trade_type' : trade_type        
    #}
    #params.update(kw)
    #if not 'sign' in params.keys():
        #params['sign'] = wx_params_sign(params)
    
    ##postdata = '''
            ##<xml>
                ##<appid>{appid}</appid>
                ##<mch_id>{mch_id}</mch_id>
                ##<device_info>{device_info}</device_info>
                ##<nonce_str>{nonce_str}</nonce_str>
                ##<body>{body}</body>
                ##<detail>{detail}</detail>
                ##<out_trade_no>{out_trade_no}</out_trade_no>
                ##<fee_type>{fee_type}</fee_type>
                ##<total_fee>{total_fee}</total_fee>
                ##<spbill_create_ip>{spbill_create_ip}</spbill_create_ip>
                ##<notify_url>{notify_url}</notify_url>
                ##<trade_type>{trade_type}</trade_type>
                ##<sign>{sign}</sign>
            ##</xml>
        ##'''.format(**params)  
        
    #postdata='<xml>'
    #for k,v in params.items():
        #postdata+='<{key}>{value}</key>'.format(key=k,value=v)
    #postdata+='</xml>'
    
    #resp = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder',data=postdata)
    

    #def get_wx_order(self):
        #'''
            #微信统一下单
        #'''
        #params = {
            #'appid' : setting.WXPAY_APPID,
            #'mch_id' : setting.WXPAY_MACHID,
            #'device_info' : 'WEB',
            #'nonce_str' : str(int(time.time())),
            #'body' : self.meal['meal_name'],
            #'detail': self.meal['meal_desc'],
            #'out_trade_no' : self.orderno,
            #'fee_type' : 'CNY',
            #'total_fee' : int(float(self.meal['meal_nowprice'])*100),
            #'spbill_create_ip' : (self.request_ip and self.request_ip) or '127.0.0.1',
            #'notify_url' : setting.WXPAY_NOTIFY,
            #'trade_type' : 'APP'
        #}
        #params['sign'] = self.wx_params_sign(params)

        #postdata_tpl = '''
            #<xml>
                #<appid>%s</appid>
                #<mch_id>%s</mch_id>
                #<device_info>%s</device_info>
                #<nonce_str>%s</nonce_str>
                #<body>%s</body>
                #<detail>%s</detail>
                #<out_trade_no>%s</out_trade_no>
                #<fee_type>%s</fee_type>
                #<total_fee>%s</total_fee>
                #<spbill_create_ip>%s</spbill_create_ip>
                #<notify_url>%s</notify_url>
                #<trade_type>%s</trade_type>
                #<sign>%s</sign>
            #</xml>
        #'''

        #postdata = postdata_tpl % (params['appid'],params['mch_id'],params['device_info'],params['nonce_str'],
                                   #params['body'],params['detail'],params['out_trade_no'],params['fee_type'],params['total_fee'],
                                   #params['spbill_create_ip'],params['notify_url'],params['trade_type'],params['sign'])


        #from tornado import httpclient
        #try:
            #url = 'api.mch.weixin.qq.com'
            #import httplib
            #conn = httplib.HTTPSConnection(host=url,port=443)
            #conn.request(url='/pay/unifiedorder',method='POST',body=postdata)
            #response = conn.getresponse()
##           http_client = httpclient.HTTPClient()
##           response = http_client.fetch(host=url,url='/pay/unifiedorder',method='POST',body=postdata)
            #resp = xmltodict.parse(response.read())
            #resp = resp['xml']
            #self.resp['code'],self.resp['msg'] = 1,resp.get('return_msg')      
            #self.resp['ret'] = (resp.get('return_code') == 'SUCCESS' and 1) or 0
            #self.resp['data'] = self.wx_mobile_sign(resp)
            #if self.resp['ret']==1:
                #dmoney = float(self.meal['meal_price'])-float(self.meal['meal_nowprice'])
                #_orderctl.add_payorder(self.userid,self.orderno,self.productid,0,self.meal['meal_price'],dmoney,self.meal['meal_nowprice'],self.platform,self.meal['meal_name'])
        #except Exception ,ex:
            #logger.error('error in getwxorder:%s' % str(ex))
            #self.resp['code'],self.resp['msg'] = 3,str(ex)
        #self.send()

#def wx_params_sign(WXPAY_APISECERT,params):
    #sign_str = ''
    #for k,v in sorted(params.items(),key=lambda p:p[0]):
        #sign_str += '{key}={value}&'.format(key=k,value=v)
    #sign_str = sign_str + 'key=' + WXPAY_APISECERT
    #return hashlib.md5(sign_str).hexdigest().upper()