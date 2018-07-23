from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowSearch, ModelFields, RowFilter

from ..models import TbLimit, TbMatches
from ..admin_riskcontrol.blanklist import AccountSelect

class TbLimitPage(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '最大赔付'  # maxpayout
    
    class tableCls(ModelTable):
        model = TbLimit
        exclude = []
        pop_edit_field = 'tid'
        
        class search(RowSearch):
            names = ['matchid']
            
class TbLimitForm(ModelFields):
    readonly = ['createtime', 'updatetime']
    class Meta:
        model = TbLimit
        exclude = []
    
    def dict_head(self, head):
        
        if head['name'] =='matchid':
            table_obj = MatchSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
            
        if head['name'] =='accountid':
            table_obj = AccountSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()  
            
        return head    

class MatchSelect(ModelTable):
    model = TbMatches
    include=['matchid','tournamentzh', 'team1zh', 'team2zh', 'matchdate']
    def dict_head(self, head):
        dc={
               'matchid':100,
               'tournamentzh': 150,
      
           }
        if dc.get(head['name']):
            head['width'] =dc.get(head['name'])
            
        if head['name']=='matchid':
            head['editor']='com-table-foreign-click-select'
        return head
    
    class search(RowSearch):
        names=['matchid', 'team1zh', 'team2zh']
        
    class filters(RowFilter):
        range_fields=['matchdate']
        

director.update({
    'sports.limit': TbLimitPage.tableCls,
    'sports.limit.edit': TbLimitForm,
    'sports.matchselect': MatchSelect,
})

page_dc.update({
    'sports.limit': TbLimitPage,
})