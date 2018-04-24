# encoding:utf-8
"""
>->helper/middleware>

RequestMiddleware
    追踪所有请求，主要用于追踪json数据。
    如果遇到json，原样返回json数据，日志会记录所有信息。
    其他类型的信息，只会显示长度信息
<-<
"""
import re
import logging
log = logging.getLogger('all_request')


class RequestMiddleware(object):
    #def process_request(self,request):
        #return request

    def process_response(self,request, response):
        url=request.get_full_path()
        if hasattr(response,'content'):
            content=response.content
            if not re.search('application/json',response.get('Content-Type','')):
                content= response.get('Content-Type','no content-type') + ';Len:%s'%len(content)            
        else:
            content='response no content property'
        status_code=response.status_code
        
       
        log.info('Url:{url}\nStatus_code:{status_code}\nContent:{content}'.format(url=url,content=content,status_code=status_code))
        return response