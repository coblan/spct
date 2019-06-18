from helpers.director.shortcut import ModelTable,TablePage,director,page_dc,RowFilter,RowSort
from maindb.models import TbTrendstatistics

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
                     'rechargeusernum','betnum',]
        
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