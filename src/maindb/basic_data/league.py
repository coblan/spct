from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, ModelFields, \
    RowSort, RowSearch, field_map, model_to_name,SelectSearch
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.model_func.field_procs.dotStrArray import DotStrArrayProc
from helpers.director.table.table import RowFilter

from maindb.models import TbTournament, TbOddstypegroup
from maindb.redisInstance import redisInst


class League(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '足球联赛资料'

    class tableCls(ModelTable):
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime']
        pop_edit_field = 'tournamentid'
        fields_sort = ['tournamentid', 'tournamentname', 'issubscribe', 'openlivebet', 'weight','sort', 'typegroupswitch']

        # hide_fields = ['tournamentid']

        def getExtraHead(self):
            return [{'name': 'openlivebet', 'label': '走地', 'editor': 'com-table-bool-shower'}]

        def inn_filter(self, query):
            return query.extra(
                where=["TB_SportTypes.source= TB_Tournament.source","TB_SportTypes.SportID=0"],
                tables=['TB_SportTypes']                
            )

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
            return [
                {'fun':'selected_set_and_save','label':'订阅','editor':'com-op-btn',
                 'confirm_msg':'确认订阅这些联赛?',
                 'row_match':'many_row','pre_set':'rt={issubscribe:1}'},
                {'fun':'selected_set_and_save','label':'取消订阅','editor':'com-op-btn',
                 'confirm_msg':'确认取消订阅这些联赛?',
                 'row_match':'many_row','pre_set':'rt={issubscribe:0}'},
                {'fun':'selected_set_and_save','label':'走地','editor':'com-op-btn',
                 'confirm_msg':'确认开启这些联赛的走地?',
                 'row_match':'many_row','pre_set':'rt={closelivebet:0}'},
                {'fun':'selected_set_and_save','label':'取消走地','editor':'com-op-btn',
                  'confirm_msg':'确认关闭这些联赛的走地?',
                 'row_match':'many_row','pre_set':'rt={closelivebet:1}'},
            ]

        class sort(RowSort):
            names = ['sort']

        class search(SelectSearch):
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
    readonly = ['tournamentid','source']

    def dict_head(self, head):
        if head['name'] == 'typegroupswitch':
            head['options'] = [{'value': str(x.oddstypegroup), 'label': x.oddstypenamezh, } for x in
                               TbOddstypegroup.objects.all()]
        if head['name']=='weight':
            head['fv_rule']='range(0.001~500)'
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
        exclude = ['categoryid', 'uniquetournamentid', 'createtime', 'specialcategoryid','source']


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
