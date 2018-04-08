# encoding:utf-8
from __future__ import unicode_literals
from helpers.func.collection.container import evalue_container
from helpers.func.collection.ex import findone

class TabPage(object):
    tabs=[]
    template=''
    page_label=''
    def __init__(self, request):
        self.request=request
        tab_name=request.GET.get('_tab')
        self.acture_tabs=self.get_tabs()
        self.tab_name = tab_name or self.acture_tabs[0].get('name')
        tab_dict=findone(self.acture_tabs,{'name':tab_name}) or self.acture_tabs[0]
        tab_page_cls= tab_dict.get('page_cls')
        self.tab_page = tab_page_cls(request)
        
        
    
    def get_template(self,prefer=None):
        if self.tab_page.template:
            return self.tab_page.template
        
        # 这里表示get_template方法不是继承而来的
        elif 'get_template' in self.tab_page.__class__.__dict__.keys()  and self.tab_page.get_template(prefer):
            return self.tab_page.get_template(prefer)
        elif self.template:
            return self.template
        elif prefer=='f7':
            return 'f7/tabgroup.html'
        elif prefer=='wx':
            return 'wx/tabgroup.html'
        else:
            return 'director/tabgroup.html'   
 
            
    def get_tabs(self):
        return evalue_container(self.tabs)
    
    def get_context(self):
        self.ctx={
            'tabs':[{'name':x['name'],'label':x['label'],'suffix':x.get('suffix','')} for x in self.acture_tabs],
            'crt_tab':self.tab_name,
        }        
        self.ctx.update(self.tab_page.get_context())
        return self.ctx
    
    def get_label(self):
        
        if hasattr(self.tab_page,'get_label'):
            return self.tab_page.get_label()
        elif self.page_label:
            return self.page_label
        else:
            return ''