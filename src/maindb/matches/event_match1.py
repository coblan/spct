from helpers.director.shortcut import TablePage,PlainTable,page_dc,director,Fields,ModelTable,director_view,ModelFields
from maindb.mongoInstance import mydb,mongo2tm
from maindb.models import TbMatch,TbSporttypes,TbTournament,TbTeammapping
from maindb.matches.matches import MatchsPage
from maindb.rabbitmq_instance import notifyScrapyMatch,notifyMatchMaping
import json
from helpers.director.model_func.dictfy import sim_dict
from django.utils import timezone
from django.db.models import Q
from ..rabbitmq_instance import notifyCreateNewMatch
from helpers.director.shortcut import DirectorEncoder,get_request_cache
import datetime
import time
from ..status_code import MATCH_SOURCE
from helpers.director.exceptions.question import QuestionException
from helpers.director.access.permit import has_permit

import logging
operation_log = logging.getLogger('operation_log')

beijin = datetime.timezone(datetime.timedelta(hours=8))
utc = datetime.timezone(datetime.timedelta(hours=0))
def tm2mongo(dt):
    if not dt:
        return dt
    tmp = dt.replace(tzinfo=beijin)
    #return tmp.astimezone(beijin)
    return tmp

#def mongo2tm(dt):
    #if not dt:
        #return dt
    #dd = dt.replace(tzinfo=utc)
    #return dd.astimezone(beijin)

class OtherWebMatchPage(TablePage):
    def get_label(self):
        return '比赛匹配'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def check_permit(self):
        return has_permit(self.request.user,'web_match_data1')
  
    class tableCls(PlainTable):
    
        def __init__(self, *arg,**kws):
            super().__init__(*arg,**kws)
            self.filter_args={}
            if self.search_args.get('_start_EventDateTime'):
                self.filter_args['EventDateTime'] = {'$gte' : tm2mongo( timezone.datetime.strptime( self.search_args.get('_start_EventDateTime'),'%Y-%m-%d %H:%M:%S' ) ) }
            if self.search_args.get('_end_EventDateTime'):
                if 'EventDateTime' not in  self.filter_args:
                    self.filter_args['EventDateTime'] = {'$lte' : tm2mongo( timezone.datetime.strptime( self.search_args.get('_end_EventDateTime'),'%Y-%m-%d %H:%M:%S' ) )}
                else:
                    self.filter_args['EventDateTime'].update(
                        {'$lte' : tm2mongo( timezone.datetime.strptime( self.search_args.get('_end_EventDateTime'),'%Y-%m-%d %H:%M:%S' ) )}
                    )
            if self.search_args.get('LeagueId'):
                self.filter_args['LeagueId'] =  int( self.search_args.get('LeagueId') )#{'$regex' : ".*%s.*"%self.search_args.get('LeagueZh')}
            if self.search_args.get('Team'):
                self.filter_args['$or'] = [{'Team1En':{'$regex' : ".*%s.*"%self.search_args.get('Team')}},
                                           {'Team2En':{'$regex' : ".*%s.*"%self.search_args.get('Team')}},
                                           {'Team1Zh':{'$regex' : ".*%s.*"%self.search_args.get('Team')}},
                                           {'Team2Zh':{'$regex' : ".*%s.*"%self.search_args.get('Team')}}]
            if self.search_args.get('ContrastStatus'):
                self.filter_args['ContrastStatus'] =int( self.search_args.get('ContrastStatus') )
            if self.search_args.get('TeamSwap'):
                if self.search_args.get('TeamSwap') ==1:
                    self.filter_args['TeamSwap'] = True
                else:
                    self.filter_args['$and']=[{'$or':[{'TeamSwap':{'$exists':False,}},
                                                      {'TeamSwap':False}
                                                      ]}
                                              ]
            if self.search_args.get('Source'):
                self.filter_args['Source'] =self.search_args.get('Source')
            if self.search_args.get('has_matched'):
                if self.search_args.get('has_matched') ==1:
                    self.filter_args['MatchID'] =  {'$gt':0}  #{'$exists':True}
                else:
                    self.filter_args['MatchID'] = {'$exists':False}
            if self.search_args.get('SportId'):
                self.filter_args['SportId'] = self.search_args.get('SportId')
  
        
        def get_head_context(self):
            ctx = super().get_head_context()
            heads_names = [head['name'] for head in ctx.get('heads')]
            ctx.update({
                'advise_heads':heads_names,
            })
            named_ctx = get_request_cache()['named_ctx']
            #if 'sql_league_options' not in named_ctx:
                #named_ctx['sql_league_options'] =[{'value':x.pk,'label':x.tournamentnamezh} for x in TbTournament.objects.all()]
            return ctx
        
        def get_heads(self):
            #select_table_ctx =MatchPicker().get_head_context()
            
            return [
                 #{'name':'Team1En','label':'主队英文名','editor':'com-table-click','width':130,
                 #'table_ctx':select_table_ctx,
                 #'action':'''scope.ps.selected = [scope.row];scope.head.table_ctx.par_row=scope.row; 
                 #scope.head.table_ctx.search_args._q = scope.row.Team1En.replace(/-/g,' ');
                 #scope.head.table_ctx.search_args._qf = "teamname";
                 #scope.head.table_ctx.search_args._start_matchdate=scope.row.EventDateTime;
                 #scope.head.table_ctx.search_args._end_matchdate=scope.row.EventDateTime; 
                 #cfg.pop_vue_com("com-table-panel",scope.head.table_ctx)'''},
                 {'name':'Eid','label':'EID'},
                {'name':'Team1En','label':'主队英文名','editor':'com-table-click','width':130,
                 'fields_ctx':WebMatchForm().get_head_context(),
                 'action':"var ctx =scope.head.fields_ctx;ctx.row=scope.row;ctx.ops_loc='bottom';cfg.pop_vue_com('com-form-one',ctx).then(row=>{ex.vueAssign(scope.row,row)})"},
                {'name':'team1en','label':'主队英文名(Betradar)','editor':'com-table-rich-span','width':130,'class':'matched_match','css':'.el-table--border th.matched_match{background-color:#588AB5;color:white}'},
                {'name':'Team1Zh','label':'主队中文名','editor':'com-table-span','width':130},
                {'name':'team1zh','label':'主队中文名(Betradar)','editor':'com-table-span','width':130,'class':'matched_match'},
                {'name':'Team2En','label':'客队英文名','editor':'com-table-span','width':130},
                {'name':'team2en','label':'客队英文名(Betradar)','editor':'com-table-span','width':130,'class':'matched_match'},
                {'name':'Team2Zh','label':'客队中文名','editor':'com-table-span','width':130},
                {'name':'team2zh','label':'客队中文名(Betradar)','editor':'com-table-span','width':130,'class':'matched_match'},
                {'name':'EventDateTime','label':'比赛日期','editor':'com-table-span','width':150},
                {'name':'LeagueZh','label':'联赛','editor':'com-table-span','width':120},
                {'name':'tournamentid','label':'联赛(Betradar)','editor':'com-table-label-shower','width':120,'class':'matched_match'},
                {'name':"MatchID",'label':'比赛(比对结果)','editor':'com-table-label-shower','width':300},
                {'name':'Source','label':'抓取源','editor':'com-table-mapper','options':[
                    {'value':2,'label':'188'},
                    {'value':3,'label':'沙巴'},
                    ]},
                {'name':"MatchSource",'label':'比赛来源','editor':'com-table-mapper','options':[
                    {'value':x[0],'label':x[1]} for x in MATCH_SOURCE
                    ]},
                {'name':'SportId','label':'体育类型','editor':'com-table-mapper','width':120,'options':[
                    {'value':x.sportid,'label':x.sportnamezh} for x in TbSporttypes.objects.all()
                    ]},
                #{'name':'ContrastStatus','label':'采集状态',
                 #'editor':'com-table-rich-span',
                 #'inn_editor':'com-table-mapper',
                 #'class':'middle-col btn-like-col',
                 #'cell_class':'var dc={1:"success",2:"primary"};rt=dc[scope.row.ContrastStatus]',
                 #'width':100,'options':[
                    ##{'value':0,'label':'未爬取'},
                    #{'value':1,'label':'采集中'},
                    #{'value':2,'label':'手动停止'},
                    #{'value':3,'label':'异常停止'},
                    #{'value':4,'label':'采集完成'},
                    #]},
                {'name':'bat_liveodds','label':'走地(Betradar)',
                 'inn_editor':'com-table-mapper',
                 'editor':'com-table-rich-span','class':'middle-col btn-like-col',
                 'cell_class':'var mymap={0:"warning",1:"success"};rt=mymap[scope.row.bat_liveodds]',
                 'options':[
                     {'value':0,'label':'否'},
                     {'value':1,'label':'是'},
                     ]},
                
                {'name':'TeamSwap','label':'交换主客队','editor':'com-table-bool-shower'},
                {'name':'Reason','label':'原因','editor':'com-table-span'},
                {'name':'AutoMap','label':'自动匹配','editor':'com-table-bool-shower'},
                {'name':'Active','label':'启用跟水','editor':'com-table-bool-shower'},
            ]
        
        def get_rows(self):
            start_index = ( self.page -1 ) * self.perpage
            #for item in mydb['Event'].find(self.filter_args).sort('CreateTime',-1).skip(start_index).limit(self.perpage):
            rows =[]
            #'Event'
            beijin = datetime.timezone(datetime.timedelta(hours=8))
            utc = datetime.timezone(datetime.timedelta(hours=0))
            for item in mydb['ThirdPartEvent'].find(self.filter_args).sort( [('EventDateTime',1)]).skip(start_index).limit(self.perpage):
                dc ={
                    '_director_name':'web_match_data1.edit_self'
                }
                dd = item.get('EventDateTime')
                yy = dd.replace(tzinfo=utc)
                dd = yy.astimezone(beijin)
                item['EventDateTime'] = dd.strftime('%Y-%m-%d %H:%M:%S')
                item.pop('_id')
                if 'Active' not in item:
                    item['Active']=True
                dc.update(item)
                rows.append(dc)
            
            matchid_list = [x.get('MatchID') for x in rows if x.get('MatchID')]
            dc ={}
            for inst in TbMatch.objects.filter(matchid__in=matchid_list).extra(
                select={'_tournamentid_label':'SELECT TB_Tournament.tournamentnamezh',},
                       where=['TB_Tournament.TournamentID=TB_Match.TournamentID '],
                        tables =['TB_Tournament']
                ):
                dc[inst.matchid] = inst
            for row in rows:
                if row.get('MatchID'):
                    match_inst = dc.get(row.get('MatchID'))
                    row['_MatchID_label'] = str( match_inst )
                    row.update( sim_dict( match_inst ) )
                    row.update({
                        '_tournamentid_label':match_inst._tournamentid_label,
                        
                    })
                row.update({
                    'pk':row.get('Eid'),
                    'TeamSwap':bool(row.get('TeamSwap'))
                })
            
            bat_matchlist = [x.get('MatchID') for x in rows if x.get('MatchID')]
            bat_match_dc ={}
            for match in TbMatch.objects.filter(matchid__in=bat_matchlist,source=1):
                bat_match_dc[match.matchid] = match
            for row in rows:
                if row.get('MatchID'):
                    bat_match = bat_match_dc.get(row.get('MatchID'))
                    if bat_match:
                        row['bat_liveodds'] = 1 if bat_match.hasliveodds else 0
                if 'bat_liveodds' not in row:
                    row['bat_liveodds'] =''
                        
            
            return rows
        
        @classmethod
        def clean_search_args(cls, search_args):
            if search_args.get('_first','1') == '1':
                search_args['_first'] = '0'
                search_args['_start_EventDateTime'] = timezone.now().strftime('%Y-%m-%d')+' 00:00:00'
                search_args['_end_EventDateTime'] = ( timezone.now() + timezone.timedelta(days=1) ).strftime('%Y-%m-%d')+' 23:59:59'
            return search_args
        
        def getRowFilters(self):
            league_options = [{'value':x['LeagueId'],'label':x['LeagueNameZh']} for x in mydb['League'].find({}).sort( [('LeagueNameZh',1)])]
            return [
                {'name':'Team','label':'球队名称','editor':'com-filter-text'},
                {'name':'EventDateTime','label':'日期','editor':'com-filter-datetime-range'},
                #{'name':'ContrastStatus','label':'采集状态','editor':'com-filter-select','options':[
                    #{'value':1,'label':'采集中'},
                    #{'value':2,'label':'手动停止'},
                    #{'value':3,'label':'异常停止'},
                    #{'value':4,'label':'采集完成'},
                #]},
                {'name':'TeamSwap','label':'交换主客队','editor':'com-filter-select','options':[
                    {'value':1,'label':'是'},
                    {'value':2,'label':'否'}
                ]},
                {'name':'has_matched','label':'匹配','editor':'com-filter-select','options':[
                    {'value':1,'label':'是'},
                    {'value':2,'label':'否'}
                ]},
                {'name':'Source','label':'抓取源','editor':'com-filter-select','options':[
                    {'value':2,'label':'188'},
                    {'value':3,'label':'沙巴'}
                    ]},
                {'name':'SportId','label':'体育类型','editor':'com-filter-select','options':[
                    {'label':str(x),'value':x.pk} for x in TbSporttypes.objects.filter(enabled=True)
                    ]},
                {'name':'LeagueId','label':'联赛','editor':'com-filter-single-select2',
                 'placeholder':'请选择联赛','options':league_options},
            ]
        
        def getRowPages(self):
            return {
                'crt_page':self.page,
                'total':mydb['ThirdPartEvent'].find(self.filter_args).count(),
                'perpage':self.perpage,
            }
        
        def get_operation(self):
            return [
                 {'editor':'com-op-btn','label':'设置列','icon': 'fa-gear',
                  'action':'cfg.pop_vue_com("com-panel-table-setting",{table_ps:scope.ps,title:"列调整"})'},
                #{'name':'director_call',
                 #'director_name':'event_match.start_scrapy',
                 #'editor':'com-op-btn',
                 #'label':'启动采集',
                 #'row_match':'many_row',
                 #'match_express':'Boolean( scope.row.MatchID )',
                 #'match_msg':'只能选择已经匹配完成的比赛',
                 #'confirm_msg':'确定启动这些比赛抓取', 
                 #'class':'btn-success',
                 #'icon':'fa-play',
                #},
                #{'name':'director_call',
                 #'director_name':'event_match.stop_scrapy',
                 #'editor':'com-op-btn',
                 #'label':'停止采集',
                 #'row_match':'many_row',
                 
                 #'match_express':'Boolean( scope.row.MatchID )',
                 #'match_msg':'只能选择已经匹配完成的比赛',
                 #'confirm_msg':'确定停止这些比赛抓取', 
                 #'class':'btn-default',
                 #'icon':'fa-pause',
                #},
                {'name':'selected_set_and_save',
                 'editor':'com-op-btn',
                 'label':'交换主客队',
                 'row_match':'many_row',
                 'pre_set':  'rt={TeamSwap:true}',#'rt={_my_swap_team:1}', 
                 'confirm_msg':'确定交换主客队', 
                 'class':'btn-default',
                },
                {'name':'selected_set_and_save',
                 'editor':'com-op-btn',
                 'label':'取消交换',
                 'row_match':'many_row',
                 'pre_set':  'rt={TeamSwap:false}',#'rt={_my_swap_team:1}', 
                 'confirm_msg':'确定取消交换主客队?', 
                 'class':'btn-default',
                },
                {'name':'selected_set_and_save',
                 'editor':'com-op-btn',
                 'label':'清除匹配',
                 'row_match':'many_row',
                 'pre_set':  'rt={matchid:null,_op:"clear_match"}',
                 'confirm_msg':'确定清除比赛匹配?', 
                 'class':'btn-default',
                },
                {
                 'editor':'com-op-btn',
                 'label':'同步匹配关系',
                 'confirm_msg':'确定同步匹配关系?', 
                 'class':'btn-default',
                  'action':'cfg.show_load();ex.director_call("event_match_v2.sync_match_relation").then((resp)=>{return scope.ps.search()}).then((resp)=>{cfg.hide_load(); cfg.toast("同步完成!")} )'
                },
                {
                    'editor':'com-op-btn',
                    'label':'自动批量匹配',
                    'class':'btn-danger',
                    'action':'''
                    cfg.confirm("批量匹配需要花费一定时间，是否开始自动匹配？").then(()=>{
                         cfg.show_load();
                         return ex.director_call("event_match.auto_mapping_match")
                   }).then((resp)=>{
                        cfg.hide_load()
                        scope.ps.search()
                        cfg.showMsg("自动匹配"+resp.count + " 条比赛!")
                    })
                    ''',
                    #'visible':False,
                
                },
                #{'name':'selected_set_and_save',
                 #'editor':'com-op-btn',
                 #'label':'启用跟水数据',
                 #'help_text':'可控制单场是否跟水',
                 #'row_match':'many_row',
                 #'pre_set':  'rt={Active:true,_op:"active"}',
                 #'confirm_msg':'确定开启这些比赛?', 
                 #'class':'btn-default',
                #},
                #{'name':'selected_set_and_save',
                 #'editor':'com-op-btn',
                 #'label':'弃用跟水数据',
                  #'help_text':'可控制单场是否跟水',
                 #'row_match':'many_row',
                 #'pre_set':  'rt={Active:false,_op:"active"}',
                 #'confirm_msg':'确定关闭这些比赛?', 
                 #'class':'btn-default',
                #},
                
            ]
        

class NewMatchForm(ModelFields):
    class Meta:
        model =TbMatch
        fields=['sportid','team1en','team1zh','team2en','team2zh','hasliveodds','matchdate','tournamentid']
    
    def clean(self):
        pass
    
    def dict_head(self, head):
        if head['name'] == 'sportid':
            head['editor'] = 'com-field-select'
            head['options'] =[
                {'value':x.sportid,'label':x.sportnamezh } for x in TbSporttypes.objects.all()
            ]
        if head['name'] == 'tournamentid':
            head['editor'] = 'com-field-single-select2'
            head['init_express']='ex.director_call("get_league_options",{sportid:scope.row.sportid}).then( resp=>{scope.vc.inn_options=resp;Vue.nextTick(()=>{scope.vc.update_select2()}) })'
            #head['init_express']='scope.vc.inn_options= named_ctx["sql_league_options"];Vue.nextTick(()=>{scope.vc.update_select2()})'
            head['options'] = []
        return head
    
    def get_row(self):
        return {}
    
    def save_form(self):
        tournment = TbTournament.objects.get(pk = self.kw.get('tournamentid'))
        eventid = int( time.time()*1000 )
        dc = {
            'SportId':self.kw.get('sportid'),
            'CategoryId':tournment.categoryid,
            'EventId': eventid, # self.kw.get('eventid'),
            'HasLiveOdds':self.kw.get('hasliveodds',False),
            'Team1Id':0,
            'Team2Id':0,
            'Team1Zh':self.kw.get('team1zh'),
            'Team2Zh':self.kw.get('team2zh'),
            'Team1En':self.kw.get('team1en'),
            'Team2En':self.kw.get('team2en'),
            'UniqueTournamentId':tournment.uniquetournamentid,
            'TournamentId':tournment.tournamentid,
            'TournamentName':tournment.tournamentname,
            'MatchDate':self.kw.get('matchdate'),
            'Source':self.kw.get('source'),
            
        }
        notifyCreateNewMatch(json.dumps([dc],cls=DirectorEncoder,ensure_ascii=False))
        operation_log.info('创建比赛 %s'%json.dumps(dc,cls=DirectorEncoder,ensure_ascii=False))
    
@director_view('get_league_options')
def get_league_options(sportid):
    return [{'value':x.pk,'label':x.tournamentnamezh} for x in TbTournament.objects.filter(sport_id = sportid)]

class WebMatchForm(Fields):
    
    def get_operations(self):
        ops = super().get_operations()
        return [
            {'label':'创建比赛','editor':'com-op-btn',
             'fields_ctx':NewMatchForm().get_head_context(),
             'action':''' var prow=scope.ps.vc.row;
             scope.head.fields_ctx.row={sportid:prow.SportId,
             team1en:prow.Team1En.replace(/-/g,' '),
             team1zh:prow.Team1Zh,
             team2en:prow.Team2En.replace(/-/g,' '),
             team2zh:prow.Team2Zh,
             hasliveodds:prow.HasLiveOdds,
             eventid:prow.Eid+'-'+prow.Source,
             matchdate:prow.EventDateTime,
             source:prow.Source,
             _director_name:'new_match_form1'}; 
             cfg.pop_vue_com("com-form-one",scope.head.fields_ctx)'''
             }
            ]+ops
    
    def get_heads(self):
        return [
            {'name':'LeagueZh','label':'联赛','editor':'com-field-linetext','readonly':True,},
            {'name':'EventDateTime','label':'比赛日期','editor':'com-field-datetime','readonly':True},
            {'name':'Team1En','label':'主队英文名','editor':'com-field-linetext','readonly':True,'css':'''.enname1.field-input-td .field-input span{color:red}
            .group_info_compare .field-input-td span{width:200px;}''','class':'enname1'},
            {'name':'Team1Zh','label':'主队中文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team2En','label':'客队英文名','editor':'com-field-linetext','readonly':True,'css':'.enname2.field-input-td .field-input span{color:blue}','class':'enname2'},
            {'name':'Team2Zh','label':'客队中文名','editor':'com-field-linetext','readonly':True},
            {'name':'MatchID','label':'比赛','editor':'com-field-pop-table-select',
             'init_express':'''
            scope.head.table_ctx.par_row=scope.row; 
            scope.head.table_ctx.search_args._q = scope.row.Team1En.replace(/-/g,' ');
            scope.head.table_ctx.search_args._qf = "teamname";
            Vue.set(scope.head.table_ctx.search_args,"_start_matchdate",scope.row.EventDateTime)
            Vue.set(scope.head.table_ctx.search_args,"_end_matchdate",scope.row.EventDateTime)
            Vue.set(scope.head.table_ctx.search_args,"sportid",scope.row.SportId)
             ''',
             'after_select':'ex.vueAssign(scope.row,scope.selected_row);',
             'table_ctx':MatchPicker().get_head_context(),'options':[],},
            
            {'name':'TeamSwap','label':'交换主客队','class':'myteamswap','css':'.myteamswap .field-input{width:250px}','editor':'com-field-bool','help_text':'当第三方赛事主客队顺序和Betrader不一致时，必须勾选此选项，否则会导致赔率严重错误!!!'},
            
            {'name':'tournamentid','label':'联赛(Betradar)','editor':'com-field-label-shower','readonly':True,},
            {'name':'matchdate','label':'比赛日期(Betradar)','editor':'com-field-datetime','readonly':True},
            {'name':'team1en','label':'主队英文名(Betradar)','editor':'com-field-linetext','readonly':True,'class':'enname1'},
            {'name':'team1zh','label':'主队中文名(Betradar)','editor':'com-field-linetext','readonly':True},
            {'name':'team2en','label':'客队英文名(Betradar)','editor':'com-field-linetext','readonly':True,'class':'enname2'},
            {'name':'team2zh','label':'客队中文名(Betradar)','editor':'com-field-linetext','readonly':True},
            {'name':'Active','label':'启用跟水','editor':'com-field-bool','help_text':'勾选后，即加入跟水名单组'},
        ]
    
    
    def get_head_context(self):
        ctx = super().get_head_context()
        ctx.update({
            'table_grid':[
                ['LeagueZh','tournamentid'],
                ['EventDateTime','matchdate'],
                ['Team1En','team1en'],
                ['Team1Zh','team1zh'],
                ['Team2En','team2en'],
                ['Team2Zh','team2zh'],
                ['MatchID'],
                ['TeamSwap','Active'],
                          ],
            'fields_group':[
                {'name':'info_compare','label':'信息对比','heads':['LeagueZh','tournamentid','EventDateTime','matchdate','Team1En','team1en','Team1Zh','team1zh','Team2En','team2en','Team2Zh','team2zh']},
                {'name':'jj','label':'匹配选择','heads':['MatchID','TeamSwap','Active']}
            ]
        })
        return ctx
    
    def dict_row(self):
        dc = mydb['ThirdPartEvent'].find_one({'Eid':self.kw.get('Eid')})
        out_dc = {
             '_director_name':'web_match_data1.edit_self'
        }
        dc.pop('_id')
        
        out_dc.update(dc)       
        if out_dc.get('MatchID'):
            inst = TbMatch.objects.get(matchid=out_dc.get('MatchID') )
            out_dc.update(sim_dict( inst ))
            out_dc.update({
                '_MatchID_label':str(inst) ,
            })
        else:
            for key in ['matchdate','team1en','team1zh','team2en','team2zh','tournamentid','_tournamentid_id','_MatchID_label','MatchSource','bat_liveodds']:
                out_dc[key]=''
        out_dc.update({
            'pk':dc.get('Eid'),
            'TeamSwap':bool(dc.get('TeamSwap')),
            'CreateTime':mongo2tm(dc.get('CreateTime')),
            'EventDateTime':mongo2tm(dc.get('EventDateTime')),
            'Active':dc.get('Active',True)
        })
        return out_dc
    
    def get_org_dict(self,row=[]):
        return {}
    
    def clean(self):
        
        
        if self.kw.get('matchid'):
            org_match = mydb['Event'].find_one({'MatchID':self.kw.get('matchid')})
            if org_match and org_match['Eid'] != self.kw.get('Eid'):
                raise UserWarning('比赛已经被%s vs %s匹配过了'%(org_match['Team1En'],org_match['Team2En']))
            if self.kw.get('source') !=1 and self.kw.get('source') != self.kw.get('Source'):
                # @source 本地的matchsource   @Source   mongodb 中的抓取源
                raise UserWarning('只能选取Betradar或本抓取源的比赛。')
            if  self.kw.get('source') == self.kw.get('Source') and self.kw.get('TeamSwap'):
                # @source 本地的matchsource   @Source   mongodb 中的抓取源
                raise UserWarning('抓取源与本地比赛源一致，不能交换主客队。')
            super().clean()
            eventdatetime = timezone.datetime.strptime(self.kw.get('EventDateTime'), '%Y-%m-%d %H:%M:%S' ) 
            matchdatetime = timezone.datetime.strptime(self.kw.get('matchdate') ,'%Y-%m-%d %H:%M:%S', ) 
            
            # 调试代码
            #if self.kw.get('meta_force_save'):
                #pass
            #else:
                #raise QuestionException(''' debugger;cfg.hide_load();cfg.confirm("匹配比赛时间相差大于10分钟").then(()=>{
                    #cfg.show_load();layer.close(scope.index);scope.kws.row.meta_force_save=1;ex.director_call(scope.director_name,scope.kws).then(resp=>{scope.resolve(resp)})
                #})
                 #''' )
            if  self.kw.get('meta_force_save'):
                # 如果是强制保存，就不用在询问了。
                pass 
            elif eventdatetime - matchdatetime > timezone.timedelta(minutes=10) or matchdatetime - eventdatetime > timezone.timedelta(minutes=10):
                raise QuestionException('''debugger;cfg.hide_load();cfg.confirm("匹配比赛时间相差大于10分钟,确定要保存?")
                .then(()=>{
                    cfg.show_load();layer.close(scope.index); 
                    scope.kws.row.meta_force_save=1;
                    return ex.director_call(scope.director_name,scope.kws)
                }).then(resp=>{scope.resolve(resp)})
                 ''' )
        
    
         
    def save_form(self):
        #if self.kw.get('_op')=='active':
            #dc={
                #'Active':self.kw.get('Active')
            #}
            #mydb['ThirdPartEvent'].update({'Eid':self.kw.get('Eid'),'Source':self.kw.get('Source')}, {'$set': dc})
            #operation_log.info('操作比赛匹配 [%s]:跟水数据: Active = [%s]'%(self.kw.get('Eid') , self.kw.get('Active')) )
            #return
        
        if self.kw.get('matchid'):
            match = TbMatch.objects.get(matchid=self.kw.get('matchid'))
            dc = {'MatchID':self.kw.get('matchid'),'TeamSwap':self.kw.get('TeamSwap'),'EventId':self.kw.get('eventid'),
                  'MatchSource':match.source,
                  'Active':self.kw.get('Active'),
                  } 
            self.record_team_map(match)
            mydb['ThirdPartEvent'].update({'Eid':self.kw.get('Eid'),'Source':self.kw.get('Source')}, {'$set': dc})
            dc['Eid'] = self.kw.get('Eid')
            operation_log.info('操作匹配比赛:%s'%json.dumps(dc))
        elif self.kw.get('_op') == "clear_match":
            dc = {'MatchID':"",
                  'TeamSwap':"",
                  'EventId':"",
                  'MatchSource':"",
                  'AutoMap':"",
                  'Active':"",
                  } 
            mydb['ThirdPartEvent'].update({'Eid':self.kw.get('Eid'),'Source':self.kw.get('Source')}, {'$unset': dc}) 
            operation_log.info('清除匹配比赛:%s'%self.kw.get('Eid'))
        else:
            dc ={
                'TeamSwap':self.kw.get('TeamSwap'),
                'Active':self.kw.get('Active'),
            }
            mydb['ThirdPartEvent'].update({'Eid':self.kw.get('Eid'),'Source':self.kw.get('Source')}, {'$set': dc})
            dc['Eid'] = self.kw.get('Eid')
            operation_log.info('操作匹配比赛:%s'%json.dumps(dc))
        
        #notifyMatchMaping(json.dumps({'Eid':self.kw.get('Eid')}))
    def record_team_map(self,match):
        if self.kw.get('TeamSwap'):
            home_id = match.team2id
            away_id = match.team1id
            home_source ={
                'sourceteamnameen':self.kw.get('Team2En'),
                'sourceteamnamezh':self.kw.get('Team2Zh'),
            }
            home_local ={
                'teamnameen':self.kw.get('team2en'),
                'teamnamezh':self.kw.get('team2zh'),
            }
            away_source={
                'sourceteamnameen':self.kw.get('Team1En'),
                'sourceteamnamezh':self.kw.get('Team1Zh'),
            }
            away_local={
                'teamnameen':self.kw.get('team1en'),
                'teamnamezh':self.kw.get('team1zh'),
            }
        else:
            home_id = match.team1id
            away_id = match.team2id
            home_source ={
                'sourceteamnameen':self.kw.get('Team1En'),
                'sourceteamnamezh':self.kw.get('Team1Zh'),
            }
            home_local ={
                'teamnameen':self.kw.get('team1en'),
                'teamnamezh':self.kw.get('team1zh'),
            }
            away_source={
                'sourceteamnameen':self.kw.get('Team2En'),
                'sourceteamnamezh':self.kw.get('Team2Zh'),
            }
            away_local={
                'teamnameen':self.kw.get('team2en'),
                'teamnamezh':self.kw.get('team2zh'),
            }
        
        TbTeammapping.objects.update_or_create(sportid=self.kw.get('sportid'),
                                               source = self.kw.get('Source'),
                                               **home_source,
                                               defaults={
                                                   'teamid':home_id,
                                                    'mappingkey':'%(sportid)s_%(source)s_%(sourceteamnameen)s_%(sourceteamnamezh)s'%{'sportid':self.kw.get('sportid'),
                                                                                                                                     'source': self.kw.get('Source') ,#2, # 现在写死的，因为都是球队来源都是188。
                                                                                                                                                 # 注意 self.kw.Source 是比赛来源，不要搞混了
                                                                                                                                     **home_source},
                                                   **home_local
                                               })
        TbTeammapping.objects.update_or_create(sportid=self.kw.get('sportid'),
                                                source = self.kw.get('Source'),
                                           **away_source,
                                           defaults={
                                               'teamid':away_id,
                                               'mappingkey':'%(sportid)s_%(source)s_%(sourceteamnameen)s_%(sourceteamnamezh)s'%{'sportid':self.kw.get('sportid'),
                                                                                                                                'source':self.kw.get('Source'),#2, # 现在写死的，因为都是球队来源都是188。
                                                                                                                                            # 注意 self.kw.Source 是比赛来源，不要搞混了
                                                                                                                                **away_source},
                                               **away_local
                                           })
        
        

class MatchPicker(MatchsPage.tableCls):
    fields_sort=['source','sportid','matchid', 'tournamentid','team1en', 'team1zh', 'team2en','team2zh', 'matchdate',]
    def dict_head(self, head):
        head = super().dict_head(head)
        width={
            'team1en':150,
            'team2en':150,
        }
        if head['name'] in width:
            head['width'] = width.get(head['name'])
        if head['name'] =='matchid':
            head['editor'] ='com-table-click'
            head['action']='delete scope.row._director_name;delete scope.row.pk;scope.ps.vc.$emit("finish",scope.row)'
            #head['action'] = 'delete scope.row._director_name;ex.vueAssign(scope.ps.par_row,scope.row);scope.ps.vc.$emit("finish");cfg.show_load();ex.director_call("d.save_row",{row:scope.ps.par_row}).then((resp)=>{cfg.hide_load();ex.vueAssign(scope.ps.par_row,resp.row)})'
        return head
    
    def get_operation(self):
        return []
    
    class filters(MatchsPage.tableCls.filters):
        names=['sportid','tournamentid']
    
    class search(MatchsPage.tableCls.search):
        names = ['teamname',]
        exact_names = ['matchid']
        field_sort=['teamname','matchid',]
        def get_option(self, name):
            if name == 'teamname':
                return {'value': 'teamname', 'label': '球队名称', }
            else:
                return super().get_option(name)
        def get_express(self, q_str):
            if self.qf == 'teamname':
                return Q(team1zh__icontains=q_str) | Q(team2zh__icontains=q_str) | Q(team1en__icontains=q_str) | Q(team2en__icontains=q_str)
            else:
                return super().get_express(q_str)
    
@director_view('event_match.auto_mapping_match')
def auto_mapping_match():
    now = tm2mongo(timezone.now())
    
    mapping_list =[]
    match_in_mongo = list( mydb['ThirdPartEvent'].find({'$and': [
        {'$or':[{'MatchID':{'$exists':False}},{'MatchID':None}]},
        {'Active':{'$exists':False}},
        {'EventDateTime':{'$gte':now}},
    ] }))
    for item in match_in_mongo:
        key1 = '%(sportid)s_%(source)s_%(sourceteamnameen)s_%(sourceteamnamezh)s'%{
            'sportid':item.get('SportId'),
            'source':item.get('Source'),
            'sourceteamnameen':item.get('Team1En'),
            'sourceteamnamezh':item.get('Team1Zh')
        }
        mapping_list.append(key1)
        key2 = '%(sportid)s_%(source)s_%(sourceteamnameen)s_%(sourceteamnamezh)s'%{
            'sportid':item.get('SportId'),
            'source':item.get('Source'),
            'sourceteamnameen':item.get('Team2En'),
            'sourceteamnamezh':item.get('Team2Zh')
        }
        mapping_list.append(key2)
    
    mapping_dc={}
    for mapping in TbTeammapping.objects.filter(mappingkey__in=mapping_list):
        mapping_dc[mapping.mappingkey] = mapping
    
    op_list =[]
    for item in match_in_mongo:
        key1 = '%(sportid)s_%(source)s_%(sourceteamnameen)s_%(sourceteamnamezh)s'%{
            'sportid':item.get('SportId'),
            'source': item.get('Source'),
            'sourceteamnameen':item.get('Team1En'),
            'sourceteamnamezh':item.get('Team1Zh')
        }
        key2 = '%(sportid)s_%(source)s_%(sourceteamnameen)s_%(sourceteamnamezh)s'%{
            'sportid':item.get('SportId'),
            'source': item.get('Source'),
            'sourceteamnameen':item.get('Team2En'),
            'sourceteamnamezh':item.get('Team2Zh')
        }
        
        home = mapping_dc.get(key1)
        away = mapping_dc.get(key2)
        sportid = item.get('SportId')
        
        if home and away:
            eventdate = mongo2tm( item.get('EventDateTime') ).strftime('%Y-%m-%d %H:%M:%S')
            match = TbMatch.objects.filter(sportid=sportid,
                                           team1id=home.teamid,team1en = home.teamnameen,team1zh=home.teamnamezh,
                                           team2id=away.teamid,team2en = away.teamnameen,team2zh=away.teamnamezh,
                                           matchdate=eventdate).first()
            if match:
                dc={
                    'MatchID':match.matchid,
                    'MatchSource':match.source,
                    'AutoMap':True,
                    'EventId':match.eventid,
                    'Active':True
                }
                mydb['ThirdPartEvent'].update({'Eid':item.get('Eid')}, {'$set': dc})
                op_list.append('%s=>%s'%(item.get('Eid'),match.matchid))
            else:
                match = TbMatch.objects.filter(sportid=sportid,
                                               team1id=away.teamid,team1en = away.teamnameen,team1zh=away.teamnamezh,
                                               team2id=home.teamid,team2en = home.teamnameen,team2zh=home.teamnamezh,
                                               matchdate=eventdate).first()
                if match:
                    dc={
                        'MatchID':match.matchid,
                        'MatchSource':match.source,
                        'TeamSwap':True,
                        'AutoMap':True,
                        'EventId':match.eventid,
                        'Active':True
                    }
                    mydb['ThirdPartEvent'].update({'Eid':item.get('Eid')}, {'$set': dc})
                    op_list.append('%s=>%s'%(item.get('Eid'),match.matchid))
            
    operation_log.info('自动匹配比赛:%s'%(';'.join(op_list) ) )
    return {'count':len(op_list)}

       

@director_view('event_match.start_scrapy')
def start_scrapy(rows,**kws):
    matchid_list = [row.get('MatchID') for row in rows]
    for inst in TbMatch.objects.filter(matchid__in = matchid_list).exclude(marketstatus=2):
        raise UserWarning('%s不是滚球状态，不能触发抓取'% inst)
    
    #if mydb['Event'].find({"ContrastStatus":1}).count() +len(rows) > 20:
        #raise UserWarning('最多同时爬取20场比赛!')
    
    for row in rows:
        msg = {'MatchID':row.get('MatchID'),'Eid':row.get('Eid'),'EventTeam':row.get('EventTeam'),'Source':'Backend','Action':'Start','TeamSwap':row.get('TeamSwap'),
               'EventId':row.get('eventid'),'SportId':row.get('SportId')}
        notifyScrapyMatch( json.dumps( msg,ensure_ascii=False) )

@director_view('event_match.stop_scrapy')
def stop_scrapy(rows,**kws):
    for row in rows:
        msg = {'MatchID':row.get('MatchID'),'Eid':row.get('Eid'),'EventTeam':row.get('EventTeam'),'Source':'Backend','Action':'Stop','TeamSwap':row.get('TeamSwap'),
               'EventId':row.get('eventid'),'SportId':row.get('SportId')}
        notifyScrapyMatch( json.dumps( msg,ensure_ascii=False) )

@director_view('event_match_v2.sync_match_relation')
def sync_match_relation():
    now = timezone.now().replace(tzinfo=beijin)
    ago_3hour= now - timezone.timedelta(hours=3)
    
    for item in mydb['Event'].find({'EventDateTime':{'$gte':ago_3hour},'MatchID':{'$exists':True}}):
        dc={}
        for k,v in item.items():
            if k in ['MatchID','TeamSwap','EventId']:
                dc[k] =v
            dc['MatchSource'] = 1
        mydb['ThirdPartEvent'].update({'Eid':item.get('Eid')}, {'$set': dc})


director.update({
    'web_match_data1':OtherWebMatchPage.tableCls,
    'web_match_data1.edit_self':WebMatchForm,
    'matchpicker1':MatchPicker,
    'new_match_form1':NewMatchForm,
})

page_dc.update({
    'web_match_data1':OtherWebMatchPage
})