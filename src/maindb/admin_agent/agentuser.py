from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, RowFilter, RowSort
from ..models import TbAccount
from django.db import connections


class AgentUser(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '代理用户'
    
    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid']
        
        class filters(RowFilter):
            range_fields = ['produce_time']
        
        class sort(RowSort):
            names = ['TotalLostAmount', 'SumLostAmount', 'SumBonusAmount']
        
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
                'BeginDate': "'2018-08-01'",
                'EndDate': "'2018-08-31'",
                'NickName': '',
            }
            
            sql = "exec dbo.SP_AgentUser %(AccountID)s,%(PageIndex)s,%(PageSize)s,%(BeginDate)s,%(EndDate)s,'%(NickName)s'" \
                % sql_args
            
            cursor = connections['Sports'].cursor()
            cursor.execute(sql)
            cursor.commit()
            self.set1 =  cursor.fetchall() #list(cursor)
            cursor.nextset()
            self.sub_level = []
            for row in cursor.fetchall():
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