from helpers.director.shortcut import page_dc,PlainTable,director,RowFilter,ModelTable
from django.db import connections
from maindb.models import TbSporttypes,TbTrendstatistics
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
        chart_ctx = BetCondition().get_head_context()
        chart_ctx.update({
            'content_editor':'com-bet-chart',
            'autoload':True
        })
        
        bet_week_chart = BetWeekChart().get_head_context()
        bet_week_chart.update({
            'content_editor':'com-bet-week-chart',
            'autoload':False
        })
        
        return {
            'editor':'com-live-block-tree-menu',
            'editor_label':'报表分类',
            'editor_ctx':{
                'menu':[
                    {'name':'ss','label':'中注率','open_editor':'live_table','open_ctx':WinbetRatio().get_head_context()},
                    {'name':'bbb','label':'用户活跃度统计','open_editor':'live_table','open_ctx':LoginNumer().get_head_context()},
                    {'name':'aaa','label':'投注概况','open_editor':'live_table_type','open_ctx': chart_ctx},
                    {'name':'cc','label':'投注总额-周推移','open_editor':'live_table_type','open_ctx':bet_week_chart},
                    {'name':'dd','label':'玩法统计','open_editor':'live_table','open_ctx':MarketAnalysis().get_head_context() },
                    {'name':'TournamentAnalysis','label':'联赛统计', 'open_editor':'live_table','open_ctx':TournamentAnalysis().get_head_context()  },
                    {'name':'ReportTicketState','label':'投注单状态分析', 'open_editor':'live_table','open_ctx':ReportTicketState().get_head_context()  }
                    #{'name':'ReportTicketState','label':'投注单状态汇总', 'open_editor':'live_table','open_ctx':ReportTicketState().get_head_context()  }
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
    



class LoginNumer(ModelTable):
    model = TbTrendstatistics
    include =['starttime','newusernum','betusernum','withdrawusernum','rechargeusernum',]
    selectable = False
    
    def dict_head(self, head):
        width_dc ={
            'starttime':150
        }
        if head['name'] in width_dc:
            head['width'] = width_dc.get(head['name'])
        return head
    
    class filters(RowFilter):
        range_fields=['starttime']
    

class BetCondition(ModelTable):
    model = TbTrendstatistics
    include =['starttime','betusernum','betnum','betamount','betoutcome','userprofit',]
    
    @classmethod
    def clean_search_args(cls, search_args):
        today = timezone.now()
        if not search_args.get('_start_starttime') or not search_args.get('_end_starttime'):
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')                
            search_args['_start_starttime'] = search_args.get('_start_starttime') or def_start
            search_args['_end_starttime'] = search_args.get('_end_starttime') or def_end
        if not search_args.get('Type'):
            search_args['Type'] = 0
  
        return search_args 
    
    def dict_row(self, inst):
        return {
            'userprofit':-inst.userprofit
        }
    
    class filters(RowFilter):
        range_fields=['starttime']

 
 
class BetWeekChart(PlainTable):
    def get_heads(self):
        return [
        ]
    
    @classmethod
    def clean_search_args(cls, search_args):
        #today = timezone.now()
        if not search_args.get('_start_week') or not search_args.get('_end_week'):
            raise UserWarning('必须选择开始周和结束周')
            #sp = timezone.timedelta(days=10)
            #last = today - sp
            #def_start = last.strftime('%Y-%m-%d')
            #def_end = today.strftime('%Y-%m-%d')                
            #search_args['_start_Date'] = search_args.get('_start_Date') or def_start
            #search_args['_end_Date'] = search_args.get('_end_Date') or def_end
        return search_args
    
    def get_rows(self):
        data_rows = []
        sql_args = {
            'start': self.search_args.get('_start_week'), #'2019-05-01',
            'end': self.search_args.get('_end_week') , # '2019-06-10'
        }
        #sql="""SELECT  SUM([BetAmount])  AS BetAmount, DATENAME(WEEK, StartTime) AS Week, YEAR(StartTime) AS Year
            #FROM    [dbo].[TB_TrendStatistics] WITH ( NOLOCK )
            #WHERE   [StartTime] BETWEEN '%(start)s' AND '%(end)s'
            #GROUP BY DATENAME(WEEK, StartTime), YEAR(StartTime)
            #ORDER BY Year , Week;""" % sql_args
        sql = """
        SELECT [Year],[Week],[a].[BetAmount]  FROM (
SELECT  SUM([BetAmount])  AS BetAmount, DATENAME(WEEK, StartTime) AS [Week], YEAR(StartTime) AS [Year],MIN([StartTime]) AS StartTime
FROM    [dbo].[TB_TrendStatistics] WITH ( NOLOCK )
WHERE   [StartTime] BETWEEN '%(start)s' AND '%(end)s'
GROUP BY DATENAME(WEEK, StartTime), YEAR(StartTime))a ORDER BY StartTime asc
        """% sql_args
        
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                dc = {}
                for index, head in enumerate(cursor.description):
                    dc[head[0]] = row[index]
                data_rows.append(dc)
        return data_rows
    def getRowFilters(self):
        return [
            {'name':'week','label':'周','editor':'com-filter-week-range'}
        ]

 
class MarketAnalysis(PlainTable):
    def get_heads(self):
        return [
            {'name':'SportNameZH','label':'体育类型','editor':'com-table-span'},
            {'name':'OddsKindType','label':'盘口','editor':'com-table-span'},
            {'name':'MarketNameZH','label':'玩法','editor':'com-table-span','width':120},
            {'name':'MarketID','label':'玩法ID','editor':'com-table-span'},
            {'name':'TicketCount','label':'注单数','editor':'com-table-span'},
            {'name':'TotalBetAmount','label':'总投注额','editor':'com-table-span','width':130},
            {'name':'TotalBetOutcome','label':'派奖额','editor':'com-table-span','width':120},
            {'name':'BetUserCount','label':'投注人数','editor':'com-table-span'},
            {'name':'AVGBetAmount','label':'平均注单额','editor':'com-table-span','width':140},
            {'name':'AVGBetCount','label':'平均注单数','editor':'com-table-span','width':140},
            {'name':'Profit','label':'毛利','editor':'com-table-span','width':150}
        ]
    
    @classmethod
    def clean_search_args(cls, search_args):
        today = timezone.now()
        if not search_args.get('_start_time') or not search_args.get('_end_time'):
            sp = timezone.timedelta(days=7)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d %H:%M:%S')
            def_end = today.strftime('%Y-%m-%d %H:%M:%S')                
            search_args['_start_time'] = search_args.get('_start_time') or def_start
            search_args['_end_time'] = search_args.get('_end_time') or def_end
  
        return search_args  
    
    def get_rows(self):
        data_rows = []
        try:
            accountid = int ( self.search_args.get('accountid') )
        except :
            accountid = 'null'
            
        sql_args = {
            'start': self.search_args.get('_start_time'), #'2019-05-01',
            'end': self.search_args.get('_end_time') , # '2019-06-10'
            'accountid':accountid
        }
        sql = r"EXEC SP_Report_MarketAnalysis '%(start)s','%(end)s',%(accountid)s" \
            % sql_args
        
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                dc = {}
                for index, head in enumerate(cursor.description):
                    dc[head[0]] = row[index]
                data_rows.append(dc)
        return data_rows
    
    def getRowFilters(self):
        return [
            {'name':'accountid','label':'账号ID','editor':'com-filter-text'},
            {'name':'time','label':'时间','editor':'com-filter-datetime-range'}
        ]

 
class TournamentAnalysis(PlainTable):
    @classmethod
    def clean_search_args(cls, search_args):
        today = timezone.now()
        if not search_args.get('_start_time') or not search_args.get('_end_time'):
            sp = timezone.timedelta(days=7)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d %H:%M:%S')
            def_end = today.strftime('%Y-%m-%d %H:%M:%S')                
            search_args['_start_time'] = search_args.get('_start_time') or def_start
            search_args['_end_time'] = search_args.get('_end_time') or def_end
        search_args [ 'sportID'] = search_args.get('sportID') or 1
        return search_args  
    
    def get_heads(self):
        return [
            {'name':'TournamentID','label':'联赛ID','editor':'com-table-span'},
            {'name':'TournamentNameZH','label':'联赛名','editor':'com-table-span','width':160},
            {'name':'TotalNum','label':'总场次','editor':'com-table-span'},
            {'name':'LiveNum','label':'走地场次','editor':'com-table-span'},
            {'name':'TotalBetAmount','label':'总投注额','editor':'com-table-span'},
            {'name':'TotalBetOutcome','label':'总派奖','editor':'com-table-span'},
            {'name':'TotalBonus','label':'总反水','editor':'com-table-span'},
            {'name':'OrderCount','label':'注单数','editor':'com-table-span'},
            {'name':'UserCount','label':'用户数','editor':'com-table-span'},
        ]
    def get_rows(self):
        data_rows = []
        
        sort_str = self.search_args.get('_sort')
        if sort_str:
            sort = "'%s'"%sort_str.lstrip('-')
            sortWay = "'DESC'" if sort_str.startswith('-') else "'ASC'"
        else:
            sort='NULL'
            sortWay='NULL'
            
        sql_args = {
            'start': self.search_args.get('_start_time'), #'2019-05-01',
            'end': self.search_args.get('_end_time') , # '2019-06-10'
            'sportID':self.search_args.get('sportID'),
            'sort': sort,
            'sortWay':sortWay
        }
        sql = r"EXEC SP_Report_TournamentAnalysis '%(start)s','%(end)s',%(sportID)s,%%s,%(sort)s,%(sortWay)s" \
            % sql_args
        
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql,[self.search_args.get('nickname'),])
            for row in cursor:
                dc = {}
                for index, head in enumerate(cursor.description):
                    dc[head[0]] = row[index]
                data_rows.append(dc)
        return data_rows
    
    def getRowFilters(self):
        return [
            {'name':'nickname','label':'用户昵称','editor':'com-filter-text'},
            {'name':'sportID','label':'体育类型','editor':'com-filter-select','required':True,'options':[{'value':x.sportid,'label':str(x)} for x in TbSporttypes.objects.filter(enabled=True)]},
            {'name':'time','label':'时间','editor':'com-filter-datetime-range'}
        ]
    
    def getRowSort(self):
        return   {
            'sortable': ['TotalNum','LiveNum','TotalBetAmount','TotalBetOutcome','TotalBonus','OrderCount','UserCount'],
        } 
 
class ReportTicketState(PlainTable):

    @classmethod
    def clean_search_args(cls, search_args):
        today = timezone.now()
        if not search_args.get('_start_time') or not search_args.get('_end_time'):
            sp = timezone.timedelta(days=10)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')                
            search_args['_start_time'] = search_args.get('_start_time') or def_start
            search_args['_end_time'] = search_args.get('_end_time') or def_end
  
        return search_args 
    
    def getRowFilters(self):
        return [
             {'name':'accountid','label':'账号ID','editor':'com-filter-text'},
             {'name':'sportID','label':'体育类型','editor':'com-filter-select','options':[{'value':x.sportid,'label':str(x)} for x in TbSporttypes.objects.filter(enabled=True)]},
            {'name':'time','label':'日期','editor':'com-filter-date-range'}
        ]
    
    def get_operation(self):
        return [
            {'name':'pp','label':'jjj','editor':'com-table-op-group-check','init_value':['ticketmaster_count','ticketmaster_amount','ticketmaster_count_ratio','ticketmaster_amount_ratio'],
             'action':'Vue.set(scope.ps.search_args,"showed_col",scope.value)','options':[
                {'value':'ticketmaster_count','label':'注单数量'},
                {'value':'ticketmaster_amount','label':'注单金额'},
                {'value':'ticketmaster_count_ratio','label':'注单数量占比'},
                {'value':'ticketmaster_amount_ratio','label':'注单金额占比'},
            ]}
        ]
    
    def get_heads(self):
        return [
            {'name':'CreateDate','label':'日期','editor':'com-table-span','fixed':True,'width':100},
            {'name':'Sport','label':'体育类型','editor':'com-table-span','fixed':True},
            {'name':'UserCount','label':'不重复投注人数','editor':'com-table-span','width':130},
            
            {'name':'ticketmaster_count','label':'注单数量','style':'.el-table thead.is-group th.ticketmaster_count-col{background-color:#3d8ebc;color:white;text-align:center}','class':'ticketmaster_count-col',
             'children':['SumCount','EarlyCount','LiveCount','MixtureCount','SingleCount','ParlayCount'],
             'show':' (!scope.ps.search_args.showed_col) || scope.ps.search_args.showed_col.indexOf(scope.head.name) != -1'},
            {'name':'SumCount','label':'注单数','editor':'com-table-span','sublevel':True},
            {'name':'EarlyCount','label':'早盘','editor':'com-table-span','sublevel':True},
            {'name':'LiveCount','label':'走地','editor':'com-table-span','sublevel':True},
            {'name':'MixtureCount','label':'混合','editor':'com-table-span','sublevel':True},
            {'name':'SingleCount','label':'单注','editor':'com-table-span','sublevel':True},
            {'name':'ParlayCount','label':'串关','editor':'com-table-span','sublevel':True},
            
             {'name':'ticketmaster_amount','label':'注单金额','style':'.el-table thead.is-group th.ticketmaster_amount-col{background-color:#48A66C;color:white;text-align:center}','class':'ticketmaster_amount-col',
              'children':['SumBetAmount','EarlyBetAmount','LiveBetAmount','MixtureBetAmount','SingleBetAmount','ParlayBetAmount'],
              'show':' (!scope.ps.search_args.showed_col) || scope.ps.search_args.showed_col.indexOf(scope.head.name) != -1'},
             {'name':'SumBetAmount','label':'注单金额','editor':'com-table-span','sublevel':True,'width':100},
             {'name':'EarlyBetAmount','label':'早盘','editor':'com-table-span','sublevel':True,'width':100},
             {'name':'LiveBetAmount','label':'走地','editor':'com-table-span','sublevel':True,'width':100},
             {'name':'MixtureBetAmount','label':'混合','editor':'com-table-span','sublevel':True,'width':100},
             {'name':'SingleBetAmount','label':'单注','editor':'com-table-span','sublevel':True,'width':100},
            {'name':'ParlayBetAmount','label':'串关','editor':'com-table-span','sublevel':True,'width':100},
            
             {'name':'ticketmaster_count_ratio','label':'注单数量占比','style':'.el-table thead.is-group th.ticketmaster_count_ratio-col{background-color:#F3B27C;color:white;text-align:center}','class':'ticketmaster_count_ratio-col',
              'children':['AverageCount','PrEarlyCount','PrLiveCount','PrMixtureCount','PrSingleCount','PrParlayCount'],
              'show':' (!scope.ps.search_args.showed_col) || scope.ps.search_args.showed_col.indexOf(scope.head.name) != -1'},
            {'name':'AverageCount','label':'人均','editor':'com-table-span','sublevel':True},
            {'name':'PrEarlyCount','label':'早盘','editor':'com-table-span','sublevel':True},
            {'name':'PrLiveCount','label':'走地','editor':'com-table-span','sublevel':True},
            {'name':'PrMixtureCount','label':'混合','editor':'com-table-span','sublevel':True},
            {'name':'PrSingleCount','label':'单注','editor':'com-table-span','sublevel':True},
            {'name':'PrParlayCount','label':'串关','editor':'com-table-span','sublevel':True},
            
            {'name':'ticketmaster_amount_ratio','label':'注单数量占比','style':'.el-table thead.is-group th.ticketmaster_amount_ratio-col{background-color:#5DECE2;color:white;text-align:center}','class':'ticketmaster_amount_ratio-col',
              'children':['AverageAmount','PrEarlyCount','PrLiveCount','PrMixtureCount','PrSingleCount','PrParlayCount'],
              'show':' (!scope.ps.search_args.showed_col) || scope.ps.search_args.showed_col.indexOf(scope.head.name) != -1'},
            {'name':'AverageAmount','label':'人均','editor':'com-table-span','sublevel':True},
            {'name':'PrEarlyAmount','label':'早盘','editor':'com-table-span','sublevel':True},
            {'name':'PrLiveAmount','label':'走地','editor':'com-table-span','sublevel':True},
            {'name':'PrMixtureAmount','label':'混合','editor':'com-table-span','sublevel':True},
            {'name':'PrSingleAmount','label':'单注','editor':'com-table-span','sublevel':True},
            {'name':'PrParlayAmount','label':'串关','editor':'com-table-span','sublevel':True},
            
        ]
    def get_rows(self):
        data_rows = []
        
        sort_str = self.search_args.get('_sort')
        if sort_str:
            sort = "'%s'"%sort_str.lstrip('-')
            sortWay = "'DESC'" if sort_str.startswith('-') else "'ASC'"
        else:
            sort='NULL'
            sortWay='NULL'
            
        sql_args = {
            'start': self.search_args.get('_start_time'), #'2019-05-01',
            'end': self.search_args.get('_end_time') , # '2019-06-10'
            'sportID':self.search_args.get('sportID',0),
            'AccountID':self.search_args.get('AccountID','null'),
        }
        sql = r"EXEC SP_Report_Ticket_State '%(start)s','%(end)s',%(sportID)s,%(AccountID)s" \
            % sql_args
        
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
            for row in cursor:
                dc = {}
                for index, head in enumerate(cursor.description):
                    dc[head[0]] = row[index]
                dc['CreateDate'] = dc.get('CreateDate').strftime('%Y-%m-%d')
                data_rows.append(dc)
        return data_rows
    
 

director.update({
    'WinbetRatio':WinbetRatio,
    'LoginNumer':LoginNumer,
    'BetCondition':BetCondition,
    'BetWeekChart':BetWeekChart,
    'MarketAnalysis':MarketAnalysis,
    'TournamentAnalysis':TournamentAnalysis,
    'ReportTicketState':ReportTicketState,
})

page_dc.update({
    'bet_analysis':BetAnalysisPage,
})