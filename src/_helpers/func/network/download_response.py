# encoding:utf-8
from __future__ import unicode_literals

from django.http import HttpResponse

def downloadfy_response(response_or_content,name):
    """
    @response_or_content : 使得内容，直接可以下载
    """
    if isinstance(response_or_content,HttpResponse):
        rs=response_or_content
    else:
        rs=HttpResponse(response_or_content)
    rs['Content-type'] = 'application/octet-stream'  # 'text/plain'
    rs['Content-Disposition'] = 'attachment; filename="{name}"'.format(name=name)
    return rs     
    
    