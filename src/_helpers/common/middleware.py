# encoding:utf-8
"""
"""
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User

def session_to_user(session_id):
    sess = SessionStore(session_key=session_id)
    pk = sess.get('_auth_user_id')
    return User.objects.get(pk=pk)

class GeneralProcess(object):
    def process_request(self,request):
        session_id=request.GET.get('_user_session')
        if not session_id:
            session_id=request.GET.get('user_session')  # 为了兼容，暂时支持老的user_session 参数
        if session_id:
            request.COOKIES['sessionid']=session_id
            # user=session_to_user(session_id)
            # request.user=user
        #return request

    #def process_response(self,request, response):
        #url=request.get_full_path()
        #if hasattr(response,'content'):
            #content=response.content
            #if not re.search('application/json',response.get('Content-Type','')):
                #content= response.get('Content-Type') + ';Len:%s'%len(content)            
        #else:
            #content='response no content property'
        #status_code=response.status_code
        
       
        #log.info('Url:{url}\nStatus_code:{status_code}\nContent:{content}'.format(url=url,content=content,status_code=status_code))
        #return response