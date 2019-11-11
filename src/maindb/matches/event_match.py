from helpers.director.shortcut import TablePage,PlainTable,page_dc,director,Fields,ModelTable,director_view,QuestionException
from maindb.mongoInstance import mydb
from maindb.models import TbMatch,TbSporttypes
from maindb.matches.matches import MatchsPage
from maindb.rabbitmq_instance import notifyScrapyMatch
import json
from helpers.director.model_func.dictfy import sim_dict
from django.utils import timezone
from django.db.models import Q
import logging

operation_log = logging.getLogger('operation_log')

class OtherWebMatchPage(TablePage):
    def get_label(self):
        return '比赛匹配'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(PlainTable):
        
        def __init__(self, *arg,**kws):
            super().__init__(*arg,**kws)
            self.filter_args={}
            if self.search_args.get('_start_EventDateTime'):
                self.filter_args['EventDateTime'] = {'$gte' : timezone.datetime.strptime( self.search_args.get('_start_EventDateTime'),'%Y-%m-%d %H:%M:%S' ) }
            if self.search_args.get('_end_EventDateTime'):
                if 'EventDateTime' not in  self.filter_args:
                    self.filter_args['EventDateTime'] = {'$lte' : timezone.datetime.strptime( self.search_args.get('_end_EventDateTime'),'%Y-%m-%d %H:%M:%S' ) }
                else:
                    self.filter_args['EventDateTime'].update(
                        {'$lte' : timezone.datetime.strptime( self.search_args.get('_end_EventDateTime'),'%Y-%m-%d %H:%M:%S' )}
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
                    
            if self.search_args.get('has_matched'):
                if self.search_args.get('has_matched') ==1:
                    self.filter_args['MatchID'] = {'$exists':True}
                else:
                    self.filter_args['MatchID'] = {'$exists':False}
            if self.search_args.get('SportId'):
                self.filter_args['SportId'] = self.search_args.get('SportId')
            if self.search_args.get('IsLive') != None:
                self.filter_args['IsLive'] = self.search_args.get('IsLive')
                
  
        
        def get_head_context(self):
            ctx = super().get_head_context()
            heads_names = [head['name'] for head in ctx.get('heads')]
            ctx.update({
                'advise_heads':heads_names,
            })
            return ctx
        
        def get_heads(self):
            select_table_ctx =MatchPicker().get_head_context()
            
            return [
                 #{'name':'Team1En','label':'主队英文名','editor':'com-table-click','width':130,
                 #'table_ctx':select_table_ctx,
                 #'action':'''scope.ps.selected = [scope.row];scope.head.table_ctx.par_row=scope.row; 
                 #scope.head.table_ctx.search_args._q = scope.row.Team1En.replace(/-/g,' ');
                 #scope.head.table_ctx.search_args._qf = "teamname";
                 #scope.head.table_ctx.search_args._start_matchdate=scope.row.EventDateTime;
                 #scope.head.table_ctx.search_args._end_matchdate=scope.row.EventDateTime; 
                 #cfg.pop_vue_com("com-table-panel",scope.head.table_ctx)'''},
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
                 {'name':'EventTime','label':'EventTime','editor':'com-table-span','width':100},
                {'name':'LeagueZh','label':'联赛','editor':'com-table-span','width':120},
                {'name':'tournamentid','label':'联赛(Betradar)','editor':'com-table-label-shower','width':120,'class':'matched_match'},
                {'name':"MatchID",'label':'比赛(比对结果)','editor':'com-table-label-shower','width':300},
                {'name':"IsLive",'label':'是否走地','editor':'com-table-bool-shower',},
                {'name':'ContrastStatus','label':'采集状态',
                 'editor':'com-table-rich-span',
                 'inn_editor':'com-table-mapper',
                 'class':'middle-col btn-like-col',
                 'cell_class':'var dc={1:"success",2:"primary"};rt=dc[scope.row.ContrastStatus]',
                 'width':100,'options':[
                    #{'value':0,'label':'未爬取'},
                    {'value':1,'label':'采集中'},
                    {'value':2,'label':'手动停止'},
                    {'value':3,'label':'异常停止'},
                    {'value':4,'label':'采集完成'},
                    ]},
                {'name':'TeamSwap','label':'交换主客队','editor':'com-table-bool-shower'},
                {'name':'Reason','label':'原因','editor':'com-table-span'},
            ]
        
        def get_rows(self):
            start_index = ( self.page -1 ) * self.perpage
            #for item in mydb['Event'].find(self.filter_args).sort('CreateTime',-1).skip(start_index).limit(self.perpage):
            rows =[]
            
            for item in mydb['Event'].find(self.filter_args).sort( [('EventDateTime',1)]).skip(start_index).limit(self.perpage):
                dc ={
                    '_director_name':'web_match_data.edit_self'
                }
                item.pop('_id')
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
                {'name':'Team','placeholder':'球队名称','editor':'com-filter-text'},
                {'name':'EventDateTime','label':'日期','editor':'com-filter-datetime-range'},
                {'name':'ContrastStatus','label':'采集状态','editor':'com-filter-select','options':[
                    {'value':1,'label':'采集中'},
                    {'value':2,'label':'手动停止'},
                    {'value':3,'label':'异常停止'},
                    {'value':4,'label':'采集完成'},
                ]},
                {'name':'TeamSwap','placeholder':'交换主客队','editor':'com-filter-select','options':[
                    {'value':1,'label':'是'},
                    {'value':2,'label':'否'}
                ]},
                {'name':'has_matched','placeholder':'匹配','editor':'com-filter-select','options':[
                    {'value':1,'label':'是'},
                    {'value':2,'label':'否'}
                ]},
                {'name':'IsLive','label':'是否走地','editor':'com-filter-select','options':[
                    {'value':True,'label':'是'},
                    {'value':False,'label':'否'}
                ]},
                {'name':'SportId','placeholder':'体育类型','editor':'com-filter-select','options':[
                    {'label':str(x),'value':x.pk} for x in TbSporttypes.objects.filter(enabled=True)
                    ]},
                {'name':'LeagueId','label':'联赛','editor':'com-filter-single-select2',
                 'placeholder':'请选择联赛','options':league_options},
            ]
        
        def getRowPages(self):
            return {
                'crt_page':self.page,
                'total':mydb['Event'].find(self.filter_args).count(),
                'perpage':self.perpage,
            }
        
        def get_operation(self):
            return [
                 {'editor':'com-op-btn','label':'设置列','icon': 'fa-gear',
                  'action':'cfg.pop_vue_com("com-panel-table-setting",{table_ps:scope.ps,title:"列调整"})'},
                {'name':'director_call',
                 'director_name':'event_match.start_scrapy',
                 'editor':'com-op-btn',
                 'label':'启动采集',
                 'row_match':'many_row',
                 'match_express':'Boolean( scope.row.MatchID )',
                 'match_msg':'只能选择已经匹配完成的比赛',
                 'confirm_msg':'确定启动这些比赛抓取', 
                 'class':'btn-success',
                 'icon':'fa-play',
                },
                {'name':'director_call',
                 'director_name':'event_match.stop_scrapy',
                 'editor':'com-op-btn',
                 'label':'停止采集',
                 'row_match':'many_row',
                 
                 'match_express':'Boolean( scope.row.MatchID )',
                 'match_msg':'只能选择已经匹配完成的比赛',
                 'confirm_msg':'确定停止这些比赛抓取', 
                 'class':'btn-default',
                 'icon':'fa-pause',
                },
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
                 'pre_set':  'rt={matchid:null}',
                 'confirm_msg':'确定清除比赛匹配?', 
                 'class':'btn-default',
                },
                
                
            ]
        

class WebMatchForm(Fields):
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
            
            {'name':'TeamSwap','label':'交换主客队','editor':'com-field-bool','help_text':'当第三方赛事主客队顺序和Betrader不一致时，必须勾选此选项，否则会导致赔率严重错误!!!'},
            
            {'name':'tournamentid','label':'联赛(Betradar)','editor':'com-field-label-shower','readonly':True,},
            {'name':'matchdate','label':'比赛日期(Betradar)','editor':'com-field-datetime','readonly':True},
            {'name':'team1en','label':'主队英文名(Betradar)','editor':'com-field-linetext','readonly':True,'class':'enname1'},
            {'name':'team1zh','label':'主队中文名(Betradar)','editor':'com-field-linetext','readonly':True},
            {'name':'team2en','label':'客队英文名(Betradar)','editor':'com-field-linetext','readonly':True,'class':'enname2'},
            {'name':'team2zh','label':'客队中文名(Betradar)','editor':'com-field-linetext','readonly':True},

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
                ['TeamSwap'],
                          ],
            'fields_group':[
                {'name':'info_compare','label':'信息对比','heads':['LeagueZh','tournamentid','EventDateTime','matchdate','Team1En','team1en','Team1Zh','team1zh','Team2En','team2en','Team2Zh','team2zh']},
                {'name':'jj','label':'匹配选择','heads':['MatchID','TeamSwap']}
            ]
        })
        return ctx
    
    def dict_row(self):
        dc = mydb['Event'].find_one({'Eid':self.kw.get('Eid')})
        out_dc = {
             '_director_name':'web_match_data.edit_self'
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
            for key in ['matchdate','team1en','team1zh','team2en','team2zh','tournamentid']:
                out_dc[key]=''
        out_dc.update({
            'pk':dc.get('Eid'),
            'TeamSwap':bool(dc.get('TeamSwap'))
        })
        return out_dc
    
    def get_org_dict(self,row=[]):
        return {}
    
    def clean(self):
        # 清除比赛时，没有 matchid ,不需要做验证
        if self.kw.get('matchid'):
            org_match = mydb['Event'].find_one({'MatchID':self.kw.get('matchid')})
            if org_match and org_match['Eid'] != self.kw.get('Eid'):
                raise UserWarning('比赛已经被%s vs %s匹配过了'%(org_match['Team1En'],org_match['Team2En']))
            
            super().clean()
            eventdatetime = timezone.datetime.strptime(self.kw.get('EventDateTime'), '%Y-%m-%d %H:%M:%S' ) 
            matchdatetime = timezone.datetime.strptime(self.kw.get('matchdate') ,'%Y-%m-%d %H:%M:%S', ) 
            
            # 调试代码
            #if self.kw.get('meta_force_save'):
                #pass
            #else:
                #raise QuestionException(''' cfg.hide_load();cfg.select("匹配比赛时间相差大于10分钟",
                #[{label:'仍然匹配',action:'cfg.show_load();layer.close(scope.index);var out_scope = scope.option;out_scope.kws.row.meta_force_save=1;ex.director_call(out_scope.director_name,out_scope.kws).then(resp=>{out_scope.resolve(resp)})'},
                #{label:'取消',action:'layer.close(scope.index);'}],
                #scope
                #) ''' )
            if  self.kw.get('meta_force_save'):
                # 如果是强制保存，就不用在询问了。
                pass 
            elif eventdatetime - matchdatetime > timezone.timedelta(minutes=10) or matchdatetime - eventdatetime > timezone.timedelta(minutes=10):
                ##raise UserWarning('匹配比赛时间相差大于10分钟')
                raise QuestionException(''' cfg.hide_load();cfg.select("匹配比赛时间相差大于10分钟",
                [{label:'仍然匹配',action:'cfg.show_load();layer.close(scope.index);var out_scope = scope.option;out_scope.kws.row.meta_force_save=1;ex.director_call(out_scope.director_name,out_scope.kws).then(resp=>{out_scope.resolve(resp)})'},
                {label:'取消',action:'layer.close(scope.index);'}],
                scope
                ) ''')
            
       
        
    def save_form(self):
        #if self.kw.get('_my_swap_team'):
            #if self.kw.get('TeamSwap'):
                #mydb['Event'].update({'Eid':self.kw.get('Eid')}, {'$set': {'TeamSwap':False}})
            #else:
                #mydb['Event'].update({'Eid':self.kw.get('Eid')}, {'$set': {'TeamSwap':True}})
        #else:
        
        dc = {'MatchID':self.kw.get('matchid'),'TeamSwap':self.kw.get('TeamSwap'),'EventId':self.kw.get('eventid')}
        mydb['Event'].update({'Eid':self.kw.get('Eid')}, {'$set': dc})
        operation_log.info('操作匹配比赛:%s'%json.dumps(dc))
        
        

class MatchPicker(MatchsPage.tableCls):
    fields_sort=['sportid','matchid', 'tournamentid','team1en', 'team1zh', 'team2en','team2zh', 'matchdate',]
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


director.update({
    'web_match_data':OtherWebMatchPage.tableCls,
    'web_match_data.edit_self':WebMatchForm,
    'matchpicker':MatchPicker
})

page_dc.update({
    'web_match_data':OtherWebMatchPage
})