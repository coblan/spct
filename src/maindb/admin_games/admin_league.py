from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, ModelFields, RowSort, RowSearch
from ..models import TbTournament

class League(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '联赛管理'
    
    class tableCls(ModelTable):
        model = TbTournament
        exclude = []
        pop_edit_field = 'tournamentname'
    
        def inn_filter(self, query): 
            return query.order_by('-sort')
        
        def dict_head(self, head): 
            dc = {
                'tournamentid': 120,
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
    class Meta:
        model = TbTournament
        exclude = []
    

director.update({
    'match.league': League.tableCls,
    'match.league.edit': LeagueForm,
})

page_dc.update({
    'match.league': League,
})