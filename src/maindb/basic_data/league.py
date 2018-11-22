from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, ModelFields, \
    RowSort, RowSearch, field_map, model_to_name
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.model_func.field_procs.dotStrArray import DotStrArrayProc
from helpers.director.table.table import RowFilter

from maindb.models import TbTournament, TbOddstypegroup
from maindb.redisInstance import redisInst


class League(TablePage):
    template = 'jb_admin/table_new.html'

    def get_label(self):
        return '足球联赛资料'

    class tableCls(ModelTable):
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime']
        pop_edit_field = 'tournamentid'
        fields_sort = ['tournamentid', 'tournamentname', 'issubscribe', 'openlivebet', 'sort', 'typegroupswitch']

        # hide_fields = ['tournamentid']

        def getExtraHead(self):
            return [{'name': 'openlivebet', 'label': '走地', 'editor': 'com-table-bool-shower'}]

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
                head['options'] = [{'value': str(x.oddstypegroup), 'label': x.oddstypenamezh, } for x in
                                   TbOddstypegroup.objects.all()]
            return head

        def dict_row(self, inst):
            return {
                'openlivebet': not bool(inst.closelivebet)
            }

        def get_operation(self):
            return []

        class sort(RowSort):
            names = ['sort']

        class search(RowSearch):
            names = ['tournamentname', 'tournamentid']

        class filters(RowFilter):
            names = ['issubscribe',]
            def getExtraHead(self): 
                return [
                    {'name': 'openlivebet','label': '走地',
                     'editor': 'com-filter-select',
                     'options': [
                         {'value': 0, 'label': '关闭',}, 
                         {'value': 1, 'label': '开启',}
                        ],}
                ]
            
            def clean_query(self, query): 
                if self.kw.get('openlivebet') !=  None:
                    query = query.filter( closelivebet = not self.kw['openlivebet'] )
                return query



class LeagueForm(ModelFields):
    readonly = ['tournamentid']

    def dict_head(self, head):
        if head['name'] == 'typegroupswitch':
            head['options'] = [{'value': str(x.oddstypegroup), 'label': x.oddstypenamezh, } for x in
                               TbOddstypegroup.objects.all()]
        return head


    def save_form(self):
        super().save_form()
        if 'closelivebet' in self.changed_data:
            if self.instance.closelivebet == 0:
                redisInst.delete(
                    'Backend:league:closelivebet:%(tournamentid)s' % {'tournamentid': self.instance.tournamentid})
            else:
                redisInst.set('Backend:league:closelivebet:%s' % self.instance.tournamentid, 1)
    
    def dict_row(self, inst): 
        return {
            'openlivebet': not inst.closelivebet,
        }

    class Meta:
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime']


field_map.update({
    'maindb.tbtournament.issubscribe': IntBoolProc,
    'maindb.tbtournament.closelivebet': IntBoolProc,
    'maindb.tbtournament.typegroupswitch': DotStrArrayProc,
})

director.update({
    'match.league': League.tableCls,
    'match.league.edit': LeagueForm,
})

page_dc.update({
    'league': League,
})
