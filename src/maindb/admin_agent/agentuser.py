from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, RowFilter, RowSort, RowSearch
from ..models import TbAccount
from django.db import connections
from django.utils import timezone

class AgentUser(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '代理用户'
    
    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid']
        
        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')
            search_args['_start_createtime'] = search_args.get('_start_createtime', def_start)
            search_args['_end_createtime'] = search_args.get('_end_createtime', def_end)
            return search_args 
        
        
        class filters(RowFilter):
            range_fields = ['createtime']
            
            def dict_head(self, head): 
                if head['name'] == 'createtime':
                    head['label'] = '产生时间'
                return head
        
        class sort(RowSort):
            names = ['TotalLostAmount', 'SumLostAmount', 'SumBonusAmount']
        
        class search(RowSearch):
            names = ['NickName']
            
        
        def __init__(self, *args, **kws): 
            super().__init__(*args, **kws)
            
            """
            @AccountID INT,    --用户编号  
            @PageIndex INT =1,    --页码   默认1  
            @PageSize INT =10,    --页条数 默认10  
            @BeginDate DATE=NULL,   --查询开始时间 默认上月今天  
            @EndDate DATE=NULL,   --查询结算时间 默认今天  
            @NickName VARCHAR(20) =NULL --帐号查询昵称 默认全部  
            """
            
            sql_args = {
                'AccountID': self.search_args.get('accountid', 0), 
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'BeginDate': self.search_args.get('_start_createtime', ''),
                'EndDate': self.search_args.get('_end_createtime', ''),
                'NickName': '',
            }
            
            sql = "exec dbo.SP_AgentUser %(AccountID)s,%(PageIndex)s,%(PageSize)s,'%(BeginDate)s','%(EndDate)s','%(NickName)s'" \
                % sql_args
            
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                #cursor.commit()
                self.set1 =  cursor.fetchall() 
                cursor.nextset()
                self.sub_level = []
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    self.sub_level.append(dc)
        
        def getExtraHead(self): 
            return [
                {'name': 'TotalLostAmount', 'label': 'TotalLostAmount',}, 
                {'name': 'SumActive', 'label': 'SumActive',}, 
                {'name': 'Phone', 'label': 'Phone',}, 
                {'name': 'NickName', 'label': 'NickName',}, 
                {'name': 'BonusRate', 'label': 'BonusRate',}, 
                {'name': 'VIPLv', 'label': 'VIPLv',}, 
                {'name': 'SumLostAmount', 'label': 'SumLostAmount',}, 
                {'name': 'SumBonusAmount', 'label': 'SumBonusAmount',}, 
                {'name': 'SumAmount', 'label': 'SumAmount',}, 
                {'name': 'SumRechargeAmount', 'label': 'SumRechargeAmount',}, 
                {'name': 'TotalActive', 'label': 'TotalActive',}, 
                {'name': 'SumTurnover', 'label': 'SumTurnover',}, 
                {'name': 'CreateTime', 'label': 'SumRechargeAmount',}, 
            ]
        def get_rows(self):
            for row in self.sub_level:
                row['accountid'] = row['AccountID']
                
            return self.sub_level
        
        def getRowPages(self): 
            if self.sub_level:
                total = self.sub_level[0]['Total']
            else:
                total = 0
                
            return {
                'crt_page':self.search_args.get('_page', 1),
                'total':total,
                'perpage':self.search_args.get('_perpage', 20)
                }
            
        

director.update({
    'AgentUser': AgentUser.tableCls,
})

page_dc.update({
    'AgentUser': AgentUser,
})