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
                {'name':'xxx','label':'bbb'}
            ]
        
        def get_rows(self):
            return []
        
        def get_dato_from_db(self):
            sql_args={
                'NickName':self.search_args.get('NickName'),
                
            }
            sql = r"exec dbo.SP_RelevantUser %%s,%(AccountID)s,'%(StartTime)s','%(EndTime)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s','%(SortWay)s','%(AccountType)s'" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql, [nickname])
                set0 = cursor.fetchall()
                self.total = set0[0][0]   
                

director.update({
    'ReleventUser':ReleventUserPage.tableCls
})

page_dc.update({
    'ReleventUser':ReleventUserPage
})