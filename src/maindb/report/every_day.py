from helpers.director.shortcut import ModelTable,TablePage,director,page_dc,RowFilter,RowSort
from maindb.models import TbTrendstatistics
from django.db.models import Sum,Q

class EveryDayReportPage(TablePage):
    def get_label(self):
        return '每日报表'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbTrendstatistics
        exclude =['tid','rescueamount','firstrechargeamount','secondrechargeamount','birthdayamount',
                  'deductionamount','ddditionamount','ebankamount','createtime']
        fields_sort=['starttime','userprofit','betamount','finishbetamount','betoutcome','bonusamount','turnover',
                     'rechargeamount','withdrawamount','activityamount','backendamount','betusernum','newusernum','withdrawusernum',
                     'rechargeusernum','betnum','loginusernum','rechargeonsignindaynum']
        
        def dict_row(self, inst):
            return {
                'userprofit': - inst.userprofit
            }
        
        def dict_head(self, head):
            width_dc={
                'finishbetamount':150,
            }
            if head['name'] in width_dc:
                head['width'] = width_dc.get(head['name'])
            else:
                head['width'] =120
                
            if head['name'] =='userprofit':
                head['editor'] = 'com-table-rich-span'
                head['class'] = 'scope.row[scope.head.name]<0?"everyday-warning":""'
                head['css'] = '.everyday-warning{background-color:green;color:white}'
            return head
        
        def get_operation(self):
            return [
                {'label':'导出excel','editor':'com-op-btn','action':'scope.ps.export_excel()'}
            ]
        
        def statistics(self, query):
            sum_list = ['betnum','betamount','finishbetamount','turnover','betoutcome','bonusamount','firstrechargeamount','secondrechargeamount',
                        'birthdayamount','backendamount','userprofit','activityamount','rechargeamount','withdrawamount','betusernum','newusernum','withdrawusernum','rechargeusernum',
                        'loginusernum','rechargeonsignindaynum']
            filters={}
            for item in sum_list:
                filters['total_%s'%item] = Sum(item)
          
            dc = query.aggregate(**filters)
            self.footer = {'_label':'合计'}
            for item in sum_list:
                if dc.get('total_%s'%item,None) is not None  and item == 'userprofit':
                    self.footer[item] = - dc.get('total_%s'%item)
                else:
                    self.footer[item] = dc.get('total_%s'%item)
                
            #dc = query.aggregate(total_betnum=Sum('betnum'),total_betamount=Sum('betamount'),total_finishbetamount=Sum('finishbetamount'),
                                 #total_turnover=Sum('turnover'),total_betoutcome=Sum('betoutcome'),total_bonusamount=Sum('bonusamount'),
                                 #total_firstrechargeamount=Sum('firstrechargeamount'))
            #mapper = {
                #'turnover': 'total_turnover'
            #}
            #for k in dc:
                #dc[k] = str(round(dc.get(k) or 0, 2))
            #self.footer = {'betnum':dc.get('total_betnum'),'betamount':dc.get('total_betamount'),'finishbetamount':dc.get('total_finishbetamount'),
                           #'turnover':dc.get('total_turnover'),'betoutcome':dc.get('total_betoutcome'),
                           #'bonusamount':dc.get('total_bonusamount'),'firstrechargeamount':dc.get('total_firstrechargeamount'),'_label':'合计'}
            return query
        
        class filters(RowFilter):
            range_fields=['starttime']
        
        class sort(RowSort):
            names = ['starttime','userprofit','betamount','finishbetamount','betoutcome','bonusamount','turnover',
                     'rechargeamount','withdrawamount','activityamount','backendamount','betusernum','newusernum','withdrawusernum',
                     'rechargeusernum','betnum',]

director.update({
    'everyday_report':EveryDayReportPage.tableCls,
})
      
page_dc.update({
    'everyday_report':EveryDayReportPage
})