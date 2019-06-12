from helpers.director.shortcut import page_dc,PlainTable,director,RowFilter
from django.db import connections
from maindb.models import TbSporttypes
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class BetAnalysisPage(object):
    def __init__(self, request,engin):
        self.request = request
    
    def get_label(self):
        return '投注分析'
    
    def get_template(self):
        return 'jb_admin/live.html'
    
    def get_context(self):
        return {
            'editor':'com-live-block-tree-menu',
            'editor_label':'报表分类',
            'editor_ctx':{
                'menu':[
                    {'name':'ss','label':'中注率','open_editor':'live_table','open_ctx':WinbetRatio().get_head_context()},
                ]
            } 
        }

class WinbetRatio(PlainTable):
    
    def get_heads(self):
        heads = [
            {'name': 'CreateDate', 'label': '创建日期', 'width': 150,'editor':'com-table-span','show':'scope.ps.row_has_field("CreateDate")'},
            {'name': 'BeginDate', 'label': '开始日期', 'width': 150,'editor':'com-table-span','show':'scope.ps.row_has_field("BeginDate")'},
            {'name': 'EndDate', 'label': '结束日期', 'width': 150,'editor':'com-table-span','show':'scope.ps.row_has_field("EndDate")'},
            {'name':'Year','label':'年','width':120,'editor':'com-table-span','show':'scope.ps.row_has_field("Year")'},
            {'name':'Week','label':'周','width':120,'editor':'com-table-span','show':'scope.ps.row_has_field("Week")'},
            {'name':'Month','label':'月','width':120,'editor':'com-table-span','show':'scope.ps.row_has_field("Month")'},
            {'name':'Quarter','label':'季度','width':120,'editor':'com-table-span','show':'scope.ps.row_has_field("Quarter")'},
            
            {'name': 'UserTotal', 'label': '用户数量', 'width': 130,'editor':'com-table-span'},
            {'name': 'OrderCount', 'label': '注单数', 'width': 130,'editor':'com-table-span'},
            {'name': 'WinTotal', 'label': '赢单数量', 'width': 130,'editor':'com-table-span'},
            {'name': 'AllPerc', 'label': '中注率', 'width': 130,'editor':'com-table-span'},
            {'name': 'MPerc', 'label': '中位数', 'width': 130,'editor':'com-table-span'},
        ]
        return heads
    
    @classmethod
    def clean_search_args(cls, search_args):
        today = timezone.now()
        if not search_args.get('Date'):
            sp = timezone.timedelta(days=10)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')                
            search_args['_start_Date'] = search_args.get('_start_Date') or def_start
            search_args['_end_Date'] = search_args.get('_end_Date') or def_end
        #if not search_args.get('Week'):
            #pass
        
        #if not search_args.get('Month'):
            #pass
        
        if not search_args.get('Type'):
            search_args['Type'] = 0
  
        return search_args  
    
    def get_rows(self):
        Type = self.search_args.get('Type')
        if Type == 0:
            start = self.search_args.get('_start_Date')
            end = self.search_args.get('_end_Date')
        elif Type ==1:
            start = self.search_args.get('_start_Week')
            end = self.search_args.get('_end_Week')
            if not start or not end:
                raise UserWarning('必须填写开始周和结束周')
        elif Type == 2:
            start = self.search_args.get('_start_Month')
            end = self.search_args.get('_end_Month')
            if not start or not end:
                raise UserWarning('必须填写开始月和结束月')
            start += '-01'
            end = ( timezone.datetime.strptime(end,'%Y-%m') + relativedelta(months=1) - relativedelta(days=1) ) .strftime('%Y-%m-%d')
        sql_args={
            'BeginDate':start , #'2019-05-01',
            'EndDate':  end , #'2019-06-11',
            'Type': self.search_args.get('Type'),
            'SportID':self.search_args.get('SportID') or 0,
            'AccountID':self.search_args.get('AccountID') or 0,
            'PageIndex':self.search_args.get('_page') or 1,
            'PageSize': self.search_args.get('_perpage') or 20 ,#20,
        }
        sql = r"EXEC SP_Report_WinRate '%(BeginDate)s','%(EndDate)s',%(Type)s,%(SportID)s,%(AccountID)s,%(PageIndex)s,%(PageSize)s" \
                  % sql_args
        data_rows = []
        self.total=0
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
            #set0 = cursor.fetchall()
            #self.total = set0[0][0]
            for row in cursor:
                dc = {}
                for index, head in enumerate(cursor.description):
                    dc[head[0]] = row[index]
                data_rows.append(dc)
                self.total = dc.get('Total')
        return data_rows
    
    def getRowFilters(self):
        return [
             {'name':'AccountID','label':'账号ID','editor':'com-filter-text'},
             {'name':'Type','label':'报表类型','editor':'com-filter-select','required':True,'options':[
                 {'value':0,'label':'日报'},
                 {'value':1,'label':'周报'},
                 {'value':2,'label':'月报'},
                 #{'value':3,'label':'季报'},
                 #{'value':4,'label':'年报'},
                 ]},
             {'name':'SportID','label':'运动类型','editor':'com-filter-select','options':[{'value':x.sportid,'label':str(x)} for x in TbSporttypes.objects.filter(enabled=True)]},
             {'name':'Date','label':'日期','editor':'com-filter-date-range','show':'scope.ps.search_args.Type==0'},
             {'name':'Week','label':'周','editor':'com-filter-week-range','show':'scope.ps.search_args.Type==1'},
             {'name':'Month','label':'月份','editor':'com-filter-month-range','show':'scope.ps.search_args.Type==2'}
        ]
    
    def getRowPages(self):
        return {
            'crt_page': self.search_args.get('_page', 1),
            'total': self.total,
            'perpage': self.search_args.get('_perpage', 20)
        }
    
    #class filters(RowFilter):
        #names=['AccountID']
        #icontains=['AccountID']
        #def getExtraHead(self):
            #return [
                #{'name':'AccountID','label':'账号ID',},
            #]

#class WinbetRatioWeek(PlainTable):
    #def get_rows(self):
        #return [
        #]


director.update({
    'WinbetRatio':WinbetRatio,
})

page_dc.update({
    'bet_analysis':BetAnalysisPage,
})