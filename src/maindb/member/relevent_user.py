from helpers.director.shortcut import TablePage,PlainTable,page_dc,director
from django.db import connections

class ReleventUserPage(TablePage):
    def get_label(self):
        return '相关用户'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(PlainTable):
        def get_heads(self):
            return [
                {'name':'AccountID','label':'账号ID'},
                {'name':'NickName','label':'昵称','width':140},
            ]
        
        def getRowFilters(self):
            return [
                    {'name':'NickName','label':'昵称','editor':'com-filter-text'},
                    {'name':'DeviceCode','label':'设备码','editor':'com-filter-text'},
                    {'name':'IpAddress','label':'IP地址','editor':'com-filter-text'},
                    {'name':'CardNo','label':'银行卡号','editor':'com-filter-text'},
                    {'name':'CardOwner','label':'卡Owner','editor':'com-filter-text'},
                ]
            
        
        def get_rows(self):
            rows = self.get_data_from_db()
            return rows
        
        def get_data_from_db(self):
            rows=[]
            nickname = self.search_args.get('NickName','')
            sql_args={
                'NickName':self.search_args.get('NickName',''),
                'DeviceCode':self.search_args.get('DeviceCode',''),
                'IpAddress':self.search_args.get('IpAddress',''),
                'CardNo':self.search_args.get('CardNo',''),
                'CardOwner':self.search_args.get('CardOwner',''),
            }
            sql = r"exec dbo.SP_RelevantUser %%s,'%(DeviceCode)s','%(IpAddress)s','%(CardNo)s','%(CardOwner)s'" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql, [nickname])
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        if head[0] not in ['AccountID','NickName']:
                            continue
                        dc[head[0]] = row[index]
                    rows.append(dc)  
            return rows
                  
                

director.update({
    'ReleventUser':ReleventUserPage.tableCls
})

page_dc.update({
    'ReleventUser':ReleventUserPage
})