# encoding:utf-8
from __future__ import unicode_literals

class FieldsPage(object):
    template=''
    fieldsCls=''
    ajax_scope={}
    ex_js=[]
    ex_css=[]
    def __init__(self,request):
        if not self.fieldsCls:
            for k,v in self.__class__.__dict__.items():
                if inspect.isclass(v) and issubclass(v,ModelFields):
                    self.fieldsCls = v
                    break            
        
        self.request=request
        #self.pk=request.GET.get('pk')
        self.fields = self.fieldsCls.parse_request(request) # (pk=self.pk,crt_user=request.user,request=request)

        
    
    def get_template(self,prefer=None): 
        if self.template:
            return self.template
        elif prefer=='f7':
            return 'f7/fields.html'
        else:
            return 'director/fields.html'
    
    def get_context(self):
        self.ctx=self.fields.get_context()
        self.ctx['ex_js']=self.ex_js
        self.ctx['ex_css'] = self.ex_css        
        self.ctx['app']=self.fieldsCls._meta.model._meta.app_label
        # self.ctx['page_label'] =self.get_label()
        return self.ctx
    
    def get_label(self):
        return  unicode(self.fields.instance)  #'编辑表单'  
    
