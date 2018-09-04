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
            names = [ 'SumActive', 'SumLostAmount', 'SumBonusAmount', 'SumWithdrawalAmount', 'SumBetAmount', 'SumTurnover']
        
        class search(RowSearch):
            names = ['nickname']
            
        
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
            
            
            nickname = self.search_args.get('_q', '')
            par = self.search_args.get('_par', 0)

            if par and nickname:
                nickname = ''
                self.search_args['_q'] = ''
                
            order_by = self.search_args.get('_sort', '')

            if order_by.startswith('-'):
                order_by = order_by[1:] + ' DESC'
 
            sql_args = {
                'AccountID': self.search_args.get('accountid', par), 
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'BeginDate': self.search_args.get('_start_createtime', ''),
                'EndDate': self.search_args.get('_end_createtime', ''),
                'NickName': nickname,
                'OrderBy': order_by,
            }
            
            sql = "exec dbo.SP_AgentUser %(AccountID)s,%(PageIndex)s,%(PageSize)s,'%(BeginDate)s','%(EndDate)s','%(NickName)s','%(OrderBy)s'" \
                % sql_args
            
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                #cursor.commit()
                self.parent_agents = []
                for par in cursor:
                    self.parent_agents.append({'value': par[3], 'label': par[1],})
                self.parent_agents.append({'value': 0, 'label': '根用户',})
                self.parent_agents.reverse()

                cursor.nextset()
                self.child_agents = []
                for row in cursor:
                    dc = {}
                    for index, desp_item in enumerate(cursor.description):
                        head_name = desp_item[0]
                        dc[head_name] = row[index]
                    self.child_agents.append(dc)
                if self.child_agents:
                    row1 = self.child_agents[0]
                    footer = {}
                    for k, v in row1.items():
                        if k != 'Total' and k.startswith('Total'):
                            footer['Sum'+k[5:]] = v
                    self.footer = ['合计'] + self.footer_by_dict(footer)
            # 保持 _par参数为空状态，可以判断 前端操作是 搜索or点击
            self.search_args['_par'] =  0
                
        
        def dict_head(self, head): 
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-call-fun'
                head['fun'] = 'get_childs'
                head['field'] = 'accountid'
            return head
        
        def getExtraHead(self): 
            return [
                #{'name': 'TotalLostAmount', 'label': 'TotalLostAmount',}, 
                {'name': 'NickName', 'label': 'NickName',}, 
                {'name': 'Phone', 'label': 'Phone',}, 
                {'name': 'VIPLv', 'label': 'VIPLv',}, 
                {'name': 'BonusRate', 'label': 'BonusRate',}, 
                {'name': 'SumActive', 'label': '活跃用户',}, 
                {'name': 'SumLostAmount', 'label': 'SumLostAmount','width': 130,}, 
                {'name': 'SumBonusAmount', 'label': 'SumBonusAmount','width': 140,}, 
                {'name': 'SumBetAmount', 'label': 'SumBetAmount','width': 120,}, 
                {'name': 'SumRechargeAmount', 'label': 'SumRechargeAmount','width': 140,}, 
                {'name': 'SumWithdrawalAmount', 'label': '充值提现','width': 100,}, 
                {'name': 'SumTurnover', 'label': 'SumTurnover','width': 120,}, 
                {'name': 'CreateTime', 'label': 'CreateTime','width': 100,}, 
            ]
        def get_rows(self):
            for row in self.child_agents:
                row['accountid'] = row['AccountID']
                
            return self.child_agents
        
        
        def getRowPages(self): 
            if self.child_agents:
                total = self.child_agents[0]['Total']
            else:
                total = 0
                
            return {
                'crt_page':self.search_args.get('_page', 1),
                'total':total,
                'perpage':self.search_args.get('_perpage', 20)
                }
        
        #def get_context(self): 
            #ctx = super().get_context()
            #ctx['parents'] = self.parent_agents
            #return ctx
            
        def getParents(self): 
            return self.parent_agents
            
        

director.update({
    'AgentUser': AgentUser.tableCls,
})

page_dc.update({
    'AgentUser': AgentUser,
})