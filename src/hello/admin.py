from django.contrib import admin

# Register your models here.
from helpers.director.shortcut import TablePage,ModelTable,page_dc,FieldsPage,ModelFields,model_dc
#from orgmodel.models import Exceptions

#class ExceptionsPage(TablePage):
    #class tableCls(ModelTable):
        #model=Exceptions
        #exclude=[]

#class ExceptionsFormPage(FieldsPage):
    #class fieldsCls(ModelFields):
        #class Meta:
            #model = Exceptions
            #exclude=[]

#model_dc[Exceptions]={'fields':ExceptionsFormPage.fieldsCls}

#page_dc.update({
    #'orgmodel.exception':ExceptionsPage,
    #'orgmodel.exception.edit':ExceptionsFormPage
#})

class Home(object):
    template='hello/home.html'
    def __init__(self,request, engin):
        pass
    def get_context(self):
        return {}

page_dc.update({
    'home':Home
})