from django.contrib import admin
from django.db import connections
# Register your models here.
from helpers.director.shortcut import TablePage,ModelTable,page_dc,FieldsPage,ModelFields,model_dc, director_view
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
        statistic_items = [
            
        ]
        
        trend = [
            {'key': '1','label': '投注', }, 
            {'key': '2','label': '派奖', }, 
            {'key': '3','label': '流水', }, 
            {'key': '4','label': '平台亏盈',}, 
            {'key': '5','label': '充值', }, 
            {'key': '6','label': '提现', }, 
        ]
        
        sql = "exec  SP_TodayStatistics"
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
            today_static = {} 
            row =  list(cursor)[0]  # 统计数据只有一行
            for col_data, col in zip(row, cursor.description):
                head_name = col[0]
                today_static[head_name] = col_data
        return {
            'trend_list': trend,
            'today_static': today_static,
        }
        
        
        #sql = "exec SP_TrendChart 1"
        #rows = []
        #with connections['Sports'].cursor() as cursor:
            #cursor.execute(sql)
            #for par in cursor:
                #rows.append({'time': par[0], 'amount': par[1], })            
        #return {
            #'rows': rows,
        #}
    
    
@director_view('trend_data')
def trend_data(key): 
    sql = "exec SP_TrendChart %s" % key
    rows = []
    with connections['Sports'].cursor() as cursor:
        cursor.execute(sql)
        for par in cursor:
            rows.append({'time': par[0], 'amount': par[1], })
    return rows


page_dc.update({
    'home':Home
})