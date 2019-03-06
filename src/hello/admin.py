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
        # {"RegNum": 1, "BetNum": 232, "SumBetAmount": "180123", "SumPrizeAmount": "140617", "SumLostAmount": "49071"}
        today_heads = [
            {'name': 'RegNum', 'label': '注册人数',}, 
            {'name':'BetUserNum','label':'投注人数'},
            {'name': 'BetNum', 'label': '注单数',}, 
            {'name': 'SumBetAmount', 'label': '投注金额',}, 
            {'name': 'SumPrizeAmount', 'label': '派彩金额',}, 
            {'name': 'SumLostAmount', 'label': '亏盈金额',},
            
        ]
        
        trend = [
            {'key': '7','label': '投注人数', }, 
            {'key': '1','label': '投注', }, 
            {'key': '2','label': '派奖', }, 
            {'key': '3','label': '流水', }, 
            {'key': '4','label': '平台亏盈',}, 
            {'key': '5','label': '充值', }, 
            {'key': '6','label': '提现', }, 
            
        ]
        
        sql = "exec  SP_TodayStatistics"
        today_row = {} 
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
   
            row =  list(cursor)[0]  # 统计数据只有一行
            for col_data, col in zip(row, cursor.description):
                head_name = col[0]
                today_row[head_name] = col_data
        return {
            'today_heads': today_heads,
            'today_row': today_row,            
            'trend_list': trend,
            
        }
    
@director_view('trend_data')
def trend_data(key): 
    sql = "exec SP_TrendChart %s" % key
    rows = []
    with connections['Sports'].cursor() as cursor:
        cursor.execute(sql)
        for par in cursor:
            rows.append({'time': par[0], 'amount': round(par[1], 2), })
    return rows


page_dc.update({
    'home':Home
})