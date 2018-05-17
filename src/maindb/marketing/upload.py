# encoding:utf-8
"""
该文件无用了。
"""
from __future__ import unicode_literals
import requests
from django.conf import settings

upload_url =settings.BANNER_UPLOAD_URL

def upload_banner(blob,ext):
    """
    blob:文件二进制
    ext:文件扩展名   .jpg
    """
    header={ 'Authorization': '76bbc167ed744ddd9d409b09705ddf13',
             'X-Extension':'.'+ext}
    
    #with open(r'D:\relay\images\变形jingang.jpg','rb') as f:
        #ss = f.read()
    
    rt = requests.post(upload_url,data=blob,headers=header)
    #print(rt.text)
    return rt.text