from django.contrib import admin
from django.db import connections
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
        sql = "exec SP_TrendChart 1"
        rows = []
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
            for par in cursor:
                rows.append({'time': par[0], 'amount': par[1], })            
        return {
            'rows': rows,
        }

page_dc.update({
    'home':Home
})