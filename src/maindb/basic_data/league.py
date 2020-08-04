from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, ModelFields, \
    RowSort, RowSearch, field_map, model_to_name,SelectSearch
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.model_func.field_procs.dotStrArray import DotStrArrayProc
from helpers.director.table.table import RowFilter
from helpers.director.access.permit import can_write
import json
from maindb.models import TbTournament, TbMarkets,TbMatch
from maindb.redisInstance import redisInst
from  maindb.rabbitmq_instance import notifyAdjustOddsBase,notifyLeagueGroup
from django.utils import timezone
from helpers.director.access.permit import has_permit

class League(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '联赛资料'

    class tableCls(ModelTable):
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime',]
        pop_edit_fields = ['tournamentid']
        fields_sort = ['sport','tournamentid', 'tournamentname','tournamentnamezh', 'isrecommend','issubscribe', 'openlivebet','disableparlay', 'weight','ticketdelay','sort', 'typegroupswitch',
                       'adjusttemplate','liveadjusttemplateid','handicapcount','group','minmatchshowhours']

        # hide_fields = ['tournamentid']

        def getExtraHead(self):
            return [{'name': 'openlivebet', 'label': '走地', 'editor': 'com-table-bool-shower'}]

        def inn_filter(self, query):
            if self.is_export_excel:
                query =  query.using('Sports_nolock')
            if self.kw.get('group_id'):
                return query.filter(group_id = self.kw.get('group_id'))
            else:
                return query
            
        def dict_head(self, head):
            dc = {
                'tournamentid': 120,
                'categoryid': 100,
                'tournamentname': 250,
                'tournamentnamezh':250,
                'createtime': 120,
                'typegroupswitch': 300,
                'oddsadjustment' :100,
                'oddsadjustmax' :120,
                'baseticketeamout':100,
                'handicapcount':140,
                'adjusttemplate':130,
                'liveadjusttemplateid':130,
                'minmatchshowhours':150,
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
            ops =[]
            super_ops = super().get_operation()
            for op in super_ops:
                if op['name'] =='add_new':
                    ops.append(op)
                    
            #if can_write(self.model,self.crt_user):
            ops +=  [
                {'fun':'selected_set_and_save','label':'订阅','editor':'com-op-btn',
                 'confirm_msg':'确认订阅这些联赛?',
                 'row_match':'many_row','pre_set':'rt={issubscribe:1}',
                 'visible':'issubscribe' in self.permit.changeable_fields()
                 },
                {'fun':'selected_set_and_save','label':'取消订阅','editor':'com-op-btn',
                 'confirm_msg':'确认取消订阅这些联赛?',
                 'row_match':'many_row','pre_set':'rt={issubscribe:0}',
                 'visible':'issubscribe' in self.permit.changeable_fields()
                 },
                {'fun':'selected_set_and_save','label':'走地','editor':'com-op-btn',
                 'confirm_msg':'确认开启这些联赛的走地?',
                 'row_match':'many_row','pre_set':'rt={closelivebet:0}',
                 'visible':'closelivebet'in self.permit.changeable_fields()},
                {'fun':'selected_set_and_save','label':'取消走地','editor':'com-op-btn',
                  'confirm_msg':'确认关闭这些联赛的走地?',
                 'row_match':'many_row','pre_set':'rt={closelivebet:1}',
                 'visible':'closelivebet'in self.permit.changeable_fields()},
                {'fun':'selected_set_and_save','label':'推荐','editor':'com-op-btn',
                  'confirm_msg':'确认推介这些联赛?', 
                  #'after_save':'ex.director_call("notify_tournament_recommend",{rows:scope.rows})',
                 'row_match':'many_row','pre_set':'rt={isrecommend:1}',
                 'visible':'isrecommend'in self.permit.changeable_fields()},
                {'fun':'selected_set_and_save','label':'取消推荐','editor':'com-op-btn',
                  'confirm_msg':'取消推介这些联赛?',
                 'row_match':'many_row','pre_set':'rt={isrecommend:0}',
                 'visible':'isrecommend'in self.permit.changeable_fields()},
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
                #{'label':'推介','editor':'com-op-btn','row_match':'many_row',
                 #'action':''' if(scope.ps.check_selected(scope.head)){ cfg.confirm("确定推介联赛?").then(()=>{
                 #scope.selected.forEach(item=>{item.isrecommend=true}) ; return ex.director_call("save_rows",{rows:})}) }'''}
                ]
            return ops

        class sort(RowSort):
            names = ['sort','weight','ticketdelay','handicapcount','tournamentid','group','adjusttemplate','liveadjusttemplateid']
            
            def get_query(self, query):
                qstr =''
                if self.sort_str .endswith('group'):
                    qstr = 'group__groupname'
                elif self.sort_str .endswith('adjusttemplate'):
                    qstr = 'adjusttemplate__templatename'
                elif self.sort_str .endswith('liveadjusttemplateid'):
                    qstr = 'liveadjusttemplateid__templatename'
                if qstr and self.sort_str.startswith('-'):
                    qstr = '-' + qstr
                    
                if qstr:
                    query = query.order_by(qstr)
                else:
                    query= super().get_query(query)
                return query
            

        class search(SelectSearch):
            names = ['tournamentname', 'tournamentid']

        class filters(RowFilter):
            names = ['issubscribe','sport','isrecommend','adjusttemplate','group']
            def getExtraHead(self): 
                return [
                    {'name': 'openlivebet',
                     'placeholder': '走地',
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
    readonly = ['source']
    
    
    def dict_head(self, head):
        if head['name'] == 'tournamentid':
            head['readonly']=True
        if head['name'] == 'typegroupswitch':
            head['options'] = [{'value': str(x.marketid), 'label': x.marketnamezh, } for x in
                               TbMarkets.objects.filter(enabled=1)]
        if head['name']=='weight':
            head['fv_rule']='range(0~500)'
            
        if head['name'] in [ 'oddsadjustment','oddsadjustmax']:
            head['fv_rule']='range(0~0.99);digit(2)'
            #head['fv_rule']='digit(2);range(0~1,false)'
        if head['name'] =='handicapcount':
            head['fv_rule'] = 'integer(+);range(1~6)'
        if head['name'] =='minmatchshowhours':
            head['fv_rule'] = 'range(0~100)'
            head['suffix'] = '小时'
        return head

    def clean_save(self):
        if 'isrecommend' in self.changed_data:
            if self.cleaned_data.get('isrecommend'):
                if TbTournament.objects.filter(isrecommend = True).count() >=6:
                    raise UserWarning('最多只能推介6个联赛')
        
        if 'issubscribe' in self.changed_data:
            ishiddern =  not bool( self.cleaned_data.get('issubscribe') )
            TbMatch.objects.filter(tournamentid=self.instance.tournamentid,matchdate__gte=timezone.now() ).update(ishidden=True)
        #if not self.instance.pk:
        if self.is_create:
            self.instance.tournamentid = self.get_new_tournament_id()
            self.instance.uniquetournamentid = self.instance.tournamentid
            self.instance.categoryid = 0
            self.instance.oddsadjustment = 0
            self.instance.oddsadjustmax= 0
            self.instance.baseticketeamout = 0
            
            
    def after_save(self):
        if self.is_create:
            redisInst.delete('tournament:')
    
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
        
        #if 'handicapcount' in self.changed_data or 'minodds' in self.changed_data:
            #notifyHandicapcount(json.dumps([self.instance.tournamentid]))
        if 'group' in self.changed_data or 'handicapcount' in self.changed_data or 'minodds' in self.changed_data:
            notifyLeagueGroup(json.dumps({'type':2,'id':self.instance.tournamentid}))
        
    def get_new_tournament_id(self):
        lastone = TbTournament.objects.order_by('-tournamentid').first() 
        return max([1*1000*1000,lastone.tournamentid]) +1
    
    def dict_row(self, inst): 
        return {
            'openlivebet': not inst.closelivebet,
            'tournamentid': inst.tournamentid or self.get_new_tournament_id()
        }

    class Meta:
        model = TbTournament
        exclude = ['categoryid', 'uniquetournamentid', 'createtime', 'specialcategoryid',
                   'oddsadjustment','oddsadjustmax','baseticketeamout',]

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
