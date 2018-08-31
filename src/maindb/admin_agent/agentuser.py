from helpers.director.shortcut import ModelTable, TablePage, page_dc, director
from ..models import TbAccount
from django.db import connections


class AgentUser(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '代理用户'
    
    class tableCls(ModelTable):
        model = TbAccount
        exclude = []
        
        def get_rows(self):
            """
            @AccountID INT,    --用户编号  
            @PageIndex INT =1,    --页码   默认1  
            @PageSize INT =10,    --页条数 默认10  
            @BeginDate DATE=NULL,   --查询开始时间 默认上月今天  
            @EndDate DATE=NULL,   --查询结算时间 默认今天  
            @NickName VARCHAR(20) =NULL --帐号查询昵称 默认全部  
            """
            sql = "exec dbo.SP_AgentUser %(AccountID)s,%(PageIndex)s,%(PageSize)s,%(BeginDate)s,%(EndDate)s,'%(NickName)s'" \
                % {'AccountID': 0, 
                    'PageIndex': 1,
                    'PageSize': 20,
                    'BeginDate': "'2018-08-01'",
                    'EndDate': "'2018-08-31'",
                    'NickName': '',}
            cursor = connections['Sports'].cursor()
            cursor.execute(sql)
            cursor.commit()
            set1 = list(cursor)
            cursor.nextset()
            set2 = list(cursor)
            
        

director.update({
    'AgentUser': AgentUser.tableCls,
})

page_dc.update({
    'AgentUser': AgentUser,
})