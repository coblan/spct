from helpers.director.shortcut import TablePage,ModelTable,ModelFields,director,page_dc,field_map,model_to_name,\
     RowFilter,get_request_cache,RowSort
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from maindb.models import TbLeagueGroup,TbSetting,TbTournament,TbMarkets,TbLeaguegroupMarketweight
import json
from django.db.models import Count
from maindb.basic_data.league import League
from helpers.director.access.permit import can_touch
from maindb.rabbitmq_instance import notifyLeagueGroup


class LeagueGroupPage(TablePage):
    def get_label(self):
        return '联赛风控'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbLeagueGroup
        exclude = []
        #pop_edit_fields=['id']
        hide_fields=['riskleveldelay']
        
        def dict_head(self, head):
            width = {
                'groupname':200,
                'league_count':100,
                'reopenmarketsdelay':150,
            }
            if head['name'] in width:
                head['width'] = width[head['name']]
            if head['name'] == 'id':
                head['editor'] ='com-table-switch-to-tab'
                head['ctx_name'] = 'league_group_tabs'
                head['tab_name'] = 'baseinfo'
            return head
        
        def getExtraHead(self):
            if can_touch(TbTournament,self.crt_user):
                #table_ctx = League.tableCls().get_head_context()
                #table_ctx.update({
                    #'init_express':'scope.ps.search_args.group_id=scope.ps.par_row.pk;scope.ps.search()',
                    #'ops_loc':'bottom'
                #})
                #head = {'name':'league_count','label':'包含联赛数','editor':'com-table-click',
                 #'table_ctx':table_ctx,
                 #'action':'scope.head.table_ctx.par_row=scope.row;cfg.pop_vue_com("com-table-panel",scope.head.table_ctx)'
                 #}
                head = {'name':'league_count','label':'包含联赛数','editor':'com-table-switch-to-tab','ctx_name':'league_group_tabs','tab_name':'included_league'}
            else:
                head ={'name':'league_count','label':'包含联赛数','editor':'com-table-span'}
            return [
                {'name':'marketweight_count','label':'玩法权重数','editor':'com-table-switch-to-tab','ctx_name':'league_group_tabs','tab_name':'marketweight'},
                head,
            ]
        
        def inn_filter(self, query):
            return query.annotate(league_count=Count('tbtournament',distinct=True)).annotate(marketweight_count=Count('tbleaguegroupmarketweight',distinct=True))
        
        def dict_row(self, inst):
            return {
                'league_count':inst.league_count,
                'marketweight_count':inst.marketweight_count,
            }
        
        def get_head_context(self):
            ctx = super().get_head_context()
            named_ctx = get_request_cache()['named_ctx']
            named_ctx.update({
                'league_group_tabs':[
                    {'name':'baseinfo',
                     'label':'基本信息',
                     'com':'com-tab-fields-v1',
                     'init_express':'ex.vueAssign(scope.row,scope.vc.par_row)',
                     'fields_ctx':LeagureGroupForm().get_head_context() },
                    {'name':'marketweight',
                     'label':'玩法权重',
                     'com':'com-tab-table',
                     'pre_set':'rt={leaguegroup:scope.par_row.pk}',
                     'table_ctx':TbLeaguegroupMarketweightTable().get_head_context()},
                    {'name':'included_league',
                     'label':'包含联赛',
                     'com':'com-tab-table',
                     'pre_set':'rt={group:scope.par_row.pk}',
                     'table_ctx':League.tableCls().get_head_context()}
                ]
            })
            return ctx
        
        def get_operation(self):
            ops = super().get_operation()
            out_ops = []
            for op in ops:
                if op['name'] !='delete_selected':
                    out_ops.append(op)
            return out_ops
        
        class filters(RowFilter):
            names = ['enabled']

class LeagureGroupForm(ModelFields):
    hide_fields=['id']
    class Meta:
        model = TbLeagueGroup
        exclude =[]
    
    def dict_head(self, head):
        if head['name'] == 'riskleveldelay':
            head.update({
                'editor':'com-field-table-list',
                'fv_rule':'风控等级:key_unique(Level)',
                'fv_msg':'至少填写一项,且风控等级不能重复',
                'table_heads':[
                    {'name':'Level','label':'风控等级','editor':'com-table-pop-fields-local',
                     'inn_editor':'com-table-mapper','options':[
                        {'value':x["Level"],'label':x['Memo']} for x in json.loads( TbSetting.objects.get(settingname='RiskControlLevel').settingvalue)
                    ]},
                    {'name':'PossibleWinAmount','label':'可赢额'},
                    {'name':'DelaySec','label':'延迟秒数'},
                ],
                'fields_heads':[
                    {'name':'Level','label':'风控等级','editor':'com-field-select','required':True,
                     'options':[
                        {'value':x["Level"],'label':x['Memo']} for x in json.loads( TbSetting.objects.get(settingname='RiskControlLevel').settingvalue)
                    ]},
                    {'name':'PossibleWinAmount','label':'可赢额','required':True,'editor':'com-field-number','fv_rule':'number'},
                    {'name':'DelaySec','label':'延迟秒数','editor':'com-field-number','required':True,'fv_rule':'integer(+0)'},
                ]
            })
        if head['name']=='handicapcount':
            head['fv_rule'] = 'integer(+)'
        if head['name'] == 'reopenmarketsdelay':
            head['fv_rule'] = 'integer(+)'
        if head['name'] == 'ticketdelay':
            head['suffix'] = '秒'
            head['width'] = '19rem'
        return head
    
    def dict_row(self, inst):
        return {
            'league_count':inst.tbtournament_set.count() 
        }
    
    def clean(self):
        super().clean()
        if 'enabled' in self.changed_data and self.cleaned_data.get('enabled') ==0:
            if self.instance.tbtournament_set.count() != 0:
                self.add_error('enabled', '联赛组已经被使用，不能禁用')
    
    def after_save(self):
        #if 'handicapcount' in self.changed_data or 'minodds' in self.changed_data:
        notifyLeagueGroup(json.dumps({'type':1,'id':self.instance.id}))

class TbLeaguegroupMarketweightTable(ModelTable):
    model = TbLeaguegroupMarketweight
    exclude = []
    pop_edit_fields = ['tid']
    hide_fields=['leaguegroup']
    def get_operation(self):
        ops = super().get_operation()
        for op in ops:
            if op['name'] =='add_new':
                op['pre_set'] = 'rt={leaguegroup_id:scope.vc.par_row.pk}'
        return ops
    
    def dict_head(self, head):
        width ={
            'leaguegroup':140,
            'market':250
        }
        if head['name'] in width:
            head['width'] = width.get(head['name'])
        return head
    
    class filters(RowFilter):
        names = ['leaguegroup','market__marketnamezh']
        icontains=['market__marketnamezh']
        def getExtraHead(self):
            return [
                {'name':'market__marketnamezh','label':'玩法名称'},
            ]
        def get_context(self):
            heads = super().get_context()
            out_heads=[]
            for head in heads:
                if head['name'] !='leaguegroup':
                    out_heads.append(head)
            return out_heads
    
    class sort(RowSort):
        names = ['market']
        def get_query(self, query):
            if self.sort_str =='market':
                return query.order_by('market__marketid')
            elif self.sort_str =='-market':
                return query.order_by('-market__marketid')
            else:
                return query

class TbLeaguegroupMarketweightForm(ModelFields):
    hide_fields=['leaguegroup']
    class Meta:
        model = TbLeaguegroupMarketweight
        exclude = []
    
    def dict_head(self, head):
        if head['name'] =='market':
            head['editor'] ='com-field-single-select2'
            head['options'] = [{'value':x.pk,'label':str(x)} for x in TbMarkets.objects.filter(enabled=True)]
        return head
    
    def clean(self):
        super().clean()
        if 'market' in self.changed_data:
            if TbLeaguegroupMarketweight.objects.filter(market=self.cleaned_data.get('market'),leaguegroup=self.cleaned_data.get('leaguegroup') ).exists():
                self.add_error('market','玩法[%s]已经存在'%self.cleaned_data.get('market'))

    
field_map.update({
    '%s.enabled'%model_to_name(TbLeagueGroup):IntBoolProc
})

director.update({
    'newleaguegroup':LeagueGroupPage.tableCls,
    'newleaguegroup.edit':LeagureGroupForm,
    'TbLeaguegroupMarketweightTable':TbLeaguegroupMarketweightTable,
    'TbLeaguegroupMarketweightTable.edit':TbLeaguegroupMarketweightForm
})

page_dc.update({
    'newleaguegroup':LeagueGroupPage
})