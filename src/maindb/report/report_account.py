# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowSort,RowFilter
from ..models import TbTicketmaster,TbAccount
from django.db.models.aggregates import Count,Sum
from django.db.models import F,ExpressionWrapper,FloatField
import decimal
from django.utils import timezone
from helpers.director.table.filter_adapter import datetime_range_adapter

class ReportAccout(TablePage):
    template='jb_admin/table.html'
    def get_label(self):
        return '账号统计'
    
    class tableCls(ModelTable):
        model=TbTicketmaster
        exclude=[]
        
        @classmethod
        def dict_search_args(cls,search_args):
            proc,show = ModelTable.dict_search_args(search_args)
            proc1,show1 = datetime_range_adapter(search_args, 'createtime', month=1)
            proc.update(proc1)
            show.update(show1)
            return proc,show
        
        def get_heads(self):
            heads= [
                {'name':'accountid__username','label':'用户','width':80},
                {'name':'accountid__amount','label':'用户余额','width':60},
                {'name':'accountid__tbwithdrawlimit__amount','label':'提款限额','width':30},
                {'name':'num_ticket','label':'投注数','width':60},
                {'name':'num_win','label':'中注数','width':60},
                {'name':'ratio','label':'中注比','width':60},
                {'name':'sum_money','label':'投注金额','width':60},
                {'name':'sum_outcome','label':'派彩金额','width':60},
                {'name':'sum_bonus','label':'红利','width':60},
                {'name':'sum_turnover','label':'流水','width':60},
                {'name':'profit','label':'平台盈亏','width':60},
            ]
            return heads
        
        def statistics(self, query): # tbwithdrawlimit  
            ss = query.defer("ticketid").values('accountid','accountid__tbwithdrawlimit__amount','accountid__username','accountid__amount')\
                .distinct()\
                .annotate(num_ticket=Count('ticketid'),num_win=Sum('winbet'),
                        sum_money=Sum('betamount'),sum_outcome=Sum('betoutcome'),
                        sum_bonus=Sum('bonus'),sum_turnover=Sum('turnover'))\
                .annotate(profit=F('sum_money')-F('sum_outcome'),
                          ratio=  ExpressionWrapper(F('num_win')*1.0 / F('num_ticket') , 
                                                   output_field=FloatField() ) )\
                .order_by('accountid__username')
            return ss
        
        def get_rows(self):
            rows = ModelTable.get_rows(self)
            for row in rows:
                for k,v in row.items():
                    if isinstance(v,decimal.Decimal):
                        row[k]=unicode(v)
                    elif k =='ratio':
                        row[k]=round(v*100,2)
            return rows
        
        def permited_fields(self):
            fields = ModelTable.permited_fields(self)
            fields.extend(['ratio','profit'])
            return fields
        
        class filters(RowFilter):
            range_fields=['createtime']
        
        class sort(RowSort):
            names=['ratio','profit']
            
        
    
director.update({
    'maindb.report.account':ReportAccout.tableCls
})
    
page_dc.update({
    'maindb.report.account':ReportAccout
})