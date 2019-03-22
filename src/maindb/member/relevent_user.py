from helpers.director.shortcut import TablePage,PlainTable,page_dc,director
from django.db import connections
from .account import account_tab

class ReleventUserPage(TablePage):
    def get_label(self):
        return '关联用户'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_context(self):
        ctx = super().get_context()
        named_ctx =  account_tab(self)
        ctx['named_ctx'] = named_ctx
        
        return ctx
        
    
    class tableCls(PlainTable):
        def get_heads(self):
            return [
                {'name':'AccountID','label':'账号ID',
                 'editor':'com-table-switch-to-tab',
                 'ctx_name':'account_tabs',
                 'tab_name':'baseinfo'},              
                {'name':'NickName','label':'昵称','width':140},
                {'name':'Relevant','label':'关联条件','width':280},
                {'name':'Reason','label':'原因','width':220},
                
            ]
        
        def getRowFilters(self):
            return [
                {'name':'relevent','label':'查询条件','editor':'com-filter-select',
                 'options':[{'value':1,'label':'设备ID'},
                            {'value':2,'label':'IP地址'},
                            {'value':3,'label':'持卡人'}]}
            ]
            #return [
                    #{'name':'NickName','label':'昵称','editor':'com-filter-text'},
                    #{'name':'DeviceCode','label':'设备码','editor':'com-filter-text'},
                    #{'name':'IpAddress','label':'IP地址','editor':'com-filter-text'},
                    #{'name':'CardNo','label':'银行卡号','editor':'com-filter-text'},
                    #{'name':'CardOwner','label':'卡Owner','editor':'com-filter-text'},
                #]
                
        @classmethod
        def clean_search_args(cls, search_args):
            search_args['relevent'] = search_args.get('relevent') or 1
            return search_args
        
        def get_rows(self):
            rows = self.get_data_from_db()
            return rows
        
        def get_data_from_db(self):
            rows=[]
            nickname = self.search_args.get('NickName','')
            sql_args={
                'relevent':self.search_args.get('relevent',1)
                #'NickName':self.search_args.get('NickName',''),
                #'DeviceCode':self.search_args.get('DeviceCode',''),
                #'IpAddress':self.search_args.get('IpAddress',''),
                #'CardNo':self.search_args.get('CardNo',''),
                #'CardOwner':self.search_args.get('CardOwner',''),
            }
            
            sql = r"exec dbo.SP_RelevantUser %(relevent)s" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    dc['accountid']= dc['AccountID']
                    dc['_label']= dc['NickName']
                    rows.append(dc)  
            return rows
                  
                

director.update({
    'ReleventUser':ReleventUserPage.tableCls
})

page_dc.update({
    'ReleventUser':ReleventUserPage
})