from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, ModelFields, RowSort, RowSearch
from ..models import TbTournament

class League(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '联赛管理'
    
    class tableCls(ModelTable):
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'issubscribe', 'createtime']
        pop_edit_field = 'tournamentid'
        #hide_fields = ['tournamentid']
    
        def inn_filter(self, query): 
            return query.order_by('-sort')
        
        def dict_head(self, head): 
            dc = {
                'tournamentid': 120,
                'categoryid': 100,
                'tournamentname': 250,
               'createtime': 120,
            }
            if head['name'] in dc:
                head['width'] = dc.get(head['name'])
            return head
        
        def get_operation(self): 
            return []
        
        class sort(RowSort):
            names = [ 'sort']
        
        class search(RowSearch):
            names = ['tournamentname', 'tournamentid']
            

class LeagueForm(ModelFields):
    readonly = [ 'tournamentid']
    class Meta:
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'issubscribe', 'createtime']
    
    

director.update({
    'match.league': League.tableCls,
    'match.league.edit': LeagueForm,
})

page_dc.update({
    'match.league': League,
})