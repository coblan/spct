import requests
import logging

log = logging.getLogger('task')

def send_message_password(phone, pswd): 
    url = 'http://192.168.40.137:5002/message/send'
    dc =  {
        "phone":phone,
        "message":"【飞球】您的新的登录密码是%(pswd)s。请尽快修改，如非本人操作，请忽略本短信" % {'pswd': pswd,}
       }
    
    headers = {
        'Authorization': '2D38A40CECD54A31AAAF210C85AEC0C0',
    }
    log.info('向%(phone)s发送重置密码短信'% {'phone': phone,})
    rt = requests.post(url, json = dc, headers = headers)
    log.debug('发送结果为:%s' % rt.text)

def send_message_fundspassword(phone, pswd): 
    url = 'http://192.168.40.137:5002/message/send'
    dc =  {
        "phone":phone,
        "message":"【飞球】您的新的资金密码是%(pswd)s。请尽快修改，如非本人操作，请忽略本短信" % {'pswd': pswd,}
       }
    headers = {
        'Authorization': '2D38A40CECD54A31AAAF210C85AEC0C0',
    } 
    log.info('向%(phone)s发送重置资金密码短信' % {'phone': phone,})
    rt = requests.post(url, json = dc, headers = headers)
    log.debug('发送结果为:%s' % rt.text)
    