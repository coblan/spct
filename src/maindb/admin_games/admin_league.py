from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, ModelFields, RowSort, RowSearch
from ..models import TbTournament

class League(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '联赛管理'
    
    class tableCls(ModelTable):
        model = TbTournament
        exclude = ['tournamentid']
        pop_edit_field = 'tournamentname'
        #hide_fields = ['tournamentid']
    
        def inn_filter(self, query): 
            return query.order_by('-sort')
        
        def dict_head(self, head): 
            dc = {
                'tournamentid': 120,
                'categoryid': 100,
                'tournamentname': 140,
               'createtime': 120,
            }
            if head['name'] in dc:
                head['width'] = dc.get(head['name'])
            return head
        
        class sort(RowSort):
            names = ['createtime', 'sort']
        
        class search(RowSearch):
            names = ['tournamentname']
            

class LeagueForm(ModelFields):
    readonly = ['createtime']
    class Meta:
        model = TbTournament
        exclude = ['tournamentid']
    
    

director.update({
    'match.league': League.tableCls,
    'match.league.edit': LeagueForm,
})

page_dc.update({
    'match.league': League,
})