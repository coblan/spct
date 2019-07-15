from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, ModelFields, \
    RowSort, RowSearch, field_map, model_to_name,SelectSearch
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.model_func.field_procs.dotStrArray import DotStrArrayProc
from helpers.director.table.table import RowFilter
from helpers.director.access.permit import can_write
import json
from maindb.models import TbTournament, TbMarkets
from maindb.redisInstance import redisInst
from  maindb.rabbitmq_instance import notifyAdjustOddsBase,notifyHandicapcount

class League(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '联赛资料'

    class tableCls(ModelTable):
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime']
        pop_edit_field = 'tournamentid'
        fields_sort = ['sport','tournamentid', 'tournamentname', 'isrecommend','issubscribe', 'openlivebet', 'weight','ticketdelay','sort', 'typegroupswitch',
                       'adjusttemplate']

        # hide_fields = ['tournamentid']

        def getExtraHead(self):
            return [{'name': 'openlivebet', 'label': '走地', 'editor': 'com-table-bool-shower'}]


        def dict_head(self, head):
            dc = {
                'tournamentid': 120,
                'categoryid': 100,
                'tournamentname': 250,
                'createtime': 120,
                'typegroupswitch': 300,
                'oddsadjustment' :100,
                'oddsadjustmax' :120,
                'baseticketeamout':100,
            }
            if head['name'] in dc:
                head['width'] = dc.get(head['name'])

            if head['name'] == 'typegroupswitch':
                head['options'] = [{'value': str(x.marketid), 'label': x.marketnamezh, } for x in
                                   TbMarkets.objects.filter(enabled=1)]
           
            return head

        def dict_row(self, inst):
            return {
                'openlivebet': not bool(inst.closelivebet)
            }

        def get_operation(self):
            if can_write(self.model,self.crt_user):
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
                    {'fun':'selected_set_and_save','label':'推荐','editor':'com-op-btn',
                      'confirm_msg':'确认推介这些联赛?', 
                      #'after_save':'ex.director_call("notify_tournament_recommend",{rows:scope.rows})',
                     'row_match':'many_row','pre_set':'rt={isrecommend:1}'},
                    {'fun':'selected_set_and_save','label':'取消推荐','editor':'com-op-btn',
                      'confirm_msg':'取消推介这些联赛?',
                     'row_match':'many_row','pre_set':'rt={isrecommend:0}'},
                    #{'label':'推介','editor':'com-op-btn','row_match':'many_row',
                     #'action':''' if(scope.ps.check_selected(scope.head)){ cfg.confirm("确定推介联赛?").then(()=>{
                     #scope.selected.forEach(item=>{item.isrecommend=true}) ; return ex.director_call("save_rows",{rows:})}) }'''}
                ]
            else:
                return []

        class sort(RowSort):
            names = ['sort']

        class search(SelectSearch):
            names = ['tournamentname', 'tournamentid']

        class filters(RowFilter):
            names = ['issubscribe','sport','isrecommend','adjusttemplate']
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
            head['options'] = [{'value': str(x.marketid), 'label': x.marketnamezh, } for x in
                               TbMarkets.objects.filter(enabled=1)]
        if head['name']=='weight':
            head['fv_rule']='range(0.001~500)'
            
        if head['name'] in [ 'oddsadjustment','oddsadjustmax']:
            head['fv_rule']='range(0~0.99);digit(2)'
            #head['fv_rule']='digit(2);range(0~1,false)'
        if head['name'] =='handicapcount':
            head['fv_rule'] = 'integer(+)'
        return head

    def clean_save(self):
        if 'isrecommend' in self.changed_data:
            if self.cleaned_data.get('isrecommend'):
                if TbTournament.objects.filter(isrecommend = True).count() >=6:
                    raise UserWarning('最多只能推介6个联赛')
    
    def save_form(self):
        super().save_form()
        if 'closelivebet' in self.changed_data:
            if self.instance.closelivebet == 0:
                redisInst.delete(
                    'Backend:league:closelivebet:%(tournamentid)s' % {'tournamentid': self.instance.tournamentid})
            else:
                redisInst.set('Backend:league:closelivebet:%s' % self.instance.tournamentid, 1)
        if any([x in self.changed_data for x in ['oddsadjustment','baseticketeamout','oddsadjustmax'] ] ): 
            dc ={
                'Type':1,
                'Ids':[self.instance.tournamentid]
            }
            notifyAdjustOddsBase(json.dumps(dc))
        
        if 'handicapcount' in self.changed_data:
            notifyHandicapcount(json.dumps([self.instance.tournamentid]))
        
        
    def dict_row(self, inst): 
        return {
            'openlivebet': not inst.closelivebet,
        }

    class Meta:
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime', 'specialcategoryid',
                   'oddsadjustment','oddsadjustmax','baseticketeamout']

#def notify_tournament_recommend(rows):
    #ls =[x['pk'] for x in rows]
    #msg = json.dumps(ls)
    #notifyTournameRecommond(msg)

field_map.update({
    'maindb.tbtournament.issubscribe': IntBoolProc,
    'maindb.tbtournament.closelivebet': IntBoolProc,
    'maindb.tbtournament.typegroupswitch': DotStrArrayProc,
})

director.update({
    'match.league': League.tableCls,
    'match.league.edit': LeagueForm,
    #'notify_tournament_recommend':notify_tournament_recommend,
})

page_dc.update({
    'league': League,
})
