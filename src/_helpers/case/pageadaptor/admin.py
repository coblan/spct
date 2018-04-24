# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.shortcut import model_dc,page_dc,TablePage,ModelTable,FormPage,ModelFields
from models import WebPage
from .stencil import web_page_templates,regist
from pydoc import locate
from django.conf import settings
from get_page import EnginPress

#dir_engine=locate(settings.DIR_ENGINE)

class WebPageTable(ModelTable):
    model = WebPage
    include=['name','label','temp','status']    

class WebPageTablePage(TablePage):
    template='pageadaptor/page_table.html'
    tableCls=WebPageTable

class WebPageForm(ModelFields):
    class Meta:
        model=WebPage
        fields=['name','label','temp','status','content']
      
    def get_heads(self):
        heads=super(WebPageForm,self).get_heads()
        for head in list(heads):
            if head['name']=='temp':
                head['type']='sim_select' 
                head['options']=web_page_templates
            if head['name']=='status':
                head['type']='sim_select'
                head['options']=[
                    {'value':'active','label':'Active'},
                    {'value':'deactive','label':'Deactive'}
                ]
                head['default']='deactive'
            if head['name']=='content':
                heads.remove(head)
                
        return heads

class WebPageFormPage(FieldsPage):
    fieldsCls=WebPageForm
    template='pageadaptor/page_form.html'


model_dc[WebPage]={'fields':WebPageForm}
# model_page_dc['webpage']={'table':WebPageTablePage,'form':WebPageFormPage}
page_dc.update({
    'webpage':WebPageTablePage,
    'webpage.edit':WebPageFormPage,
})


page_dc.update({'press':EnginPress})
regist('pageadaptor/one_richtext.html','one rich text')
regist('pageadaptor/one_richtext_f7.html','one rich text F7')