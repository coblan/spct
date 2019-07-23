from helpers.director.shortcut import TablePage,ModelTable,ModelFields,director,page_dc,field_map,model_to_name,RowFilter
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from maindb.models import TbLeagueGroup,TbSetting
import json
from django.db.models import Count
from maindb.basic_data.league import League

class LeagueGroupPage(TablePage):
    def get_label(self):
        return '联赛风控'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbLeagueGroup
        exclude = []
        pop_edit_fields=['id']
        hide_fields=['riskleveldelay']
        
        def dict_head(self, head):
            width = {
                'groupname':200
            }
            if head['name'] in width:
                head['width'] = width[head['name']]
            return head
        def getExtraHead(self):
            table_ctx = League.tableCls().get_head_context()
            table_ctx.update({
                'init_express':'scope.ps.search_args.group_id=scope.ps.par_row.pk;scope.ps.search()',
                'ops_loc':'bottom'
            })
            return [
                {'name':'league_count','label':'包含联赛','editor':'com-table-click',
                 'table_ctx':table_ctx,
                 'action':'scope.head.table_ctx.par_row=scope.row;cfg.pop_vue_com("com-table-panel",scope.head.table_ctx)'
                 }
            ]
        
        
         #head['editor'] = 'com-table-click'
                #head['table_ctx'] =UserPage.tableCls().get_head_context()
                #head['table_ctx'].update({
                    ##'init_express':'ex.director_call(scope.vc.ctx.director_name,{car_no:scope.vc.par_row.car_no}).then(res=>ex.vueAssign(scope.row,res))',
                    ##'after_save':'scope.vc.par_row.car_no =scope.row.car_no; scope.vc.par_row.has_washed=scope.row.has_washed ',
                    ##'init_express':'cfg.show_load(),ex.director_call(scope.vc.ctx.director_name,{pk:scope.vc.par_row.pk}).then((res)=>{cfg.hide_load();ex.vueAssign(scope.row,res)})',
                    #'init_express':'scope.ps.search_args.groups_id=scope.ps.par_row.pk;scope.ps.search()',
                    #'ops_loc':'bottom'
                #})
                #head['action'] = 'scope.head.table_ctx.par_row=scope.row;cfg.pop_vue_com("com-table-panel",scope.head.table_ctx)'
        
        
        def inn_filter(self, query):
            return query.annotate(league_count=Count('tbtournament'))
        
        def dict_row(self, inst):
            return {
                'league_count':inst.league_count
            }
        
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
                'table_heads':[
                    {'name':'Level','label':'风控等级','editor':'com-table-pop-fields-local',
                     'inn_editor':'com-table-mapper','options':[
                        {'value':x["Level"],'label':x['Memo']} for x in json.loads( TbSetting.objects.get(settingname='RiskControlLevel').settingvalue)
                    ]},
                    {'name':'PossibleWinAmount','label':'可赢额'},
                    {'name':'DelaySec','label':'延迟秒数'},
                ],
                'fields_heads':[
                    {'name':'Level','label':'风控等级','editor':'com-field-select',
                     'options':[
                        {'value':x["Level"],'label':x['Memo']} for x in json.loads( TbSetting.objects.get(settingname='RiskControlLevel').settingvalue)
                    ]},
                    {'name':'PossibleWinAmount','label':'可赢额','editor':'com-field-number','fv_rule':'number'},
                    {'name':'DelaySec','label':'延迟秒数','editor':'com-field-number','fv_rule':'integer(+0)'},
                ]
            })

        return head
    
    
field_map.update({
    '%s.enabled'%model_to_name(TbLeagueGroup):IntBoolProc
})

director.update({
    'newleaguegroup':LeagueGroupPage.tableCls,
    'newleaguegroup.edit':LeagureGroupForm
})

page_dc.update({
    'newleaguegroup':LeagueGroupPage
})