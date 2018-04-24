# encoding:utf-8

from .models import WebPage
import json
import re

class Press(object):
    def __init__(self,name):
        self.name=name
        try:
            self.page = WebPage.objects.get(name=self.name)
            
        except WebPage.DoesNotExist:
            self.page=None  
    
    def get_context(self):
        if self.page:
            return {'ctx':json.loads(self.page.content),
                    'page_label':self.page.label}
        else:
            return {}
       
    def get_template(self):
        return self.page.temp
    

class EnginPress(Press):
    """
    用于direcotr.engine的page使用
    """
    def __init__(self,request):
        name = request.GET.get('_name')
        super(EnginPress,self).__init__(name)
        
    def get_template(self, prefer=None):
        temp=self.page.temp
        # if prefer=='wx':
            # mt = re.search('^(.*)(\.[^\.]+)',temp)
            # if mt:
                # return mt.group(1)+'_wx'+mt.group(2)
        return temp
    

    