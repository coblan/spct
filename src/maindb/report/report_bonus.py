from helpers.director.shortcut import TablePage,PlainTable,page_dc,director,has_permit
from django.db import connections
from django.utils import timezone
from maindb.models import TbMerchants
from django.core.exceptions import PermissionDenied

class ReportBonusPage(TablePage):
    def get_label(self):
        return '活动统计'
    
    def check_permit(self):
        if not has_permit(self.crt_user,'report.reportBonus'):
            raise PermissionDenied('没有权限访问改页面')
                
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(PlainTable):
        
        def get_heads(self):
            return [
                {'name':'CategoryID','label':'种类ID','editor':'com-table-span'},
                {'name':'CategoryName','label':'种类','editor':'com-table-span','width':150},
                {'name':'Amount','label':'金额','editor':'com-table-span','width':150},
            ]
        
        @classmethod
        def clean_search_args(cls, search_args):
            now = timezone.now()
            if not search_args.get('_start_createtime') and not search_args.get('_end_createtime'):
                search_args['_start_createtime'] = now.strftime('%Y-%m-%d 00:00:00')
                search_args['_end_createtime'] = now.strftime('%Y-%m-%d 23:59:59')
            elif not  search_args.get('_start_createtime'):
                search_args['_start_createtime'] = search_args.get('_end_createtime')[:11]+'00:00:00'
            elif not  search_args.get('_end_createtime'):
                search_args['_end_createtime'] = search_args.get('_start_createtime')[:11]+'23:59:59'
            return search_args
            
        def get_rows(self):
            # EXEC SP_Report_Bonus '2020-09-04','2020-09-04 23:59:59',NULL--开始时间,结束时间,MerchantId
            
            start = self.search_args.get('_start_createtime')
            end = self.search_args.get('_end_createtime')
            merchant = self.search_args.get('merchant')
            sql_args ={
                'start':start,
                'end':end,
                'merchant': merchant if merchant else 'NULL',
            }
            
            sql = r"EXEC SP_Report_Bonus '%(start)s','%(end)s',%(merchant)s" \
                      % sql_args
            data_rows = []
            self.total=0
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    data_rows.append(dc)
            self.total = len(data_rows)
            return data_rows
        
        
        
        def getRowFilters(self):
            return [
                {'name':'merchant','label':'商户','editor':'com-filter-select','options':[
                    {'value':x.pk ,'label':str(x)} for x in TbMerchants.objects.all()
                    ]},
                {'name':'createtime','label':'发放时间','editor':'com-filter-datetime-range'},
            ]

director.update({
    'report-bonus':ReportBonusPage.tableCls,
})

page_dc.update({
    'report-bonus':ReportBonusPage
})