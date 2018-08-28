from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, ModelFields, \
     RowSort, RowSearch, field_map, model_to_name
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.model_func.field_procs.dotStrArray import DotStrArrayProc

from maindb.models import TbTournament, TbOddstypegroup

class League(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '联赛管理'
    
    class tableCls(ModelTable):
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime']
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
               'typegroupswitch': 300,
            }
            if head['name'] in dc:
                head['width'] = dc.get(head['name'])
                
            if head['name'] == 'typegroupswitch':
                
                head['options'] = [{'value': str(x.oddstypegroup), 'label': x.oddstypenamezh,} for x in TbOddstypegroup.objects.all()]
            return head
        
        def get_operation(self): 
            return []
        
        class sort(RowSort):
            names = [ 'sort']
        
        class search(RowSearch):
            names = ['tournamentname', 'tournamentid']
            

class LeagueForm(ModelFields):
    readonly = [ 'tournamentid']
    def dict_head(self, head): 
        if head['name'] == 'typegroupswitch':
            head['options'] = [{'value': str(x.oddstypegroup), 'label': x.oddstypenamezh,} for x in TbOddstypegroup.objects.all()]
        return head
    
    class Meta:
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime']
    

field_map.update({
    'maindb.tbtournament.issubscribe': IntBoolProc,
    'maindb.tbtournament.typegroupswitch': DotStrArrayProc,
})


director.update({
    'match.league': League.tableCls,
    'match.league.edit': LeagueForm,
})

page_dc.update({
    'match.league': League,
})