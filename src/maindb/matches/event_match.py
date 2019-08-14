from helpers.director.shortcut import TablePage,PlainTable,page_dc,director,Fields,ModelTable,director_view
from maindb.mongoInstance import mydb
from maindb.models import TbMatch
from maindb.matches.matches import MatchsPage
from maindb.rabbitmq_instance import notifyScrapyMatch
import json
from helpers.director.model_func.dictfy import sim_dict
from django.utils import timezone
from django.db.models import Q

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
            if self.search_args.get('LeagueZh'):
                self.filter_args['LeagueZh'] = {'$regex' : ".*%s.*"%self.search_args.get('LeagueZh')}
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
                 {'name':'Team1En','label':'主队英文名','editor':'com-table-click','width':130,
                 'table_ctx':select_table_ctx,
                 'action':'''scope.ps.selected = [scope.row];scope.head.table_ctx.par_row=scope.row; 
                 scope.head.table_ctx.search_args._q = scope.row.Team1En.replace(/-/g,' ');
                 scope.head.table_ctx.search_args._qf = "teamname";
                 scope.head.table_ctx.search_args._start_matchdate=scope.row.EventDateTime;
                 scope.head.table_ctx.search_args._end_matchdate=scope.row.EventDateTime; 
                 cfg.pop_vue_com("com-table-panel",scope.head.table_ctx)'''},
                #{'name':'Team1En','label':'主队英文名','editor':'com-table-click','width':130,
                 #'fields_ctx':WebMatchForm().get_head_context(),
                 #'action':"scope.head.fields_ctx.row=scope.row;cfg.pop_vue_com('com-form-one',scope.head.fields_ctx).then(row=>{ex.vueAssign(scope.row,row)})"},
                {'name':'team1en','label':'主队英文名(Betradar)','editor':'com-table-rich-span','width':130,'class':'matched_match','css':'.el-table--border th.matched_match{background-color:#588AB5;color:white}'},
                {'name':'Team1Zh','label':'主队中文名','editor':'com-table-span','width':130},
                {'name':'team1zh','label':'主队中文名(Betradar)','editor':'com-table-span','width':130,'class':'matched_match'},
                {'name':'Team2En','label':'客队英文名','editor':'com-table-span','width':130},
                {'name':'team2en','label':'客队英文名(Betradar)','editor':'com-table-span','width':130,'class':'matched_match'},
                {'name':'Team2Zh','label':'客队中文名','editor':'com-table-span','width':130},
                {'name':'team2zh','label':'客队中文名(Betradar)','editor':'com-table-span','width':130,'class':'matched_match'},
                {'name':'EventDateTime','label':'比赛日期','editor':'com-table-span','width':150},
                {'name':'LeagueZh','label':'联赛','editor':'com-table-span','width':120},
                {'name':"MatchID",'label':'比赛(比对结果)','editor':'com-table-label-shower','width':300},
                {'name':'ContrastStatus','label':'是否正在爬取',
                 'editor':'com-table-rich-span',
                 'inn_editor':'com-table-mapper',
                 'class':'middle-col btn-like-col',
                 'cell_class':'var dc={1:"success",2:"primary"};rt=dc[scope.row.ContrastStatus]',
                 'width':100,'options':[
                    #{'value':0,'label':'未爬取'},
                    {'value':1,'label':'爬取中'},
                    {'value':2,'label':'已爬取'},
                    ]},
                {'name':'TeamSwap','label':'交换主客队','editor':'com-table-bool-shower'}
            ]
        
        def get_rows(self):
            start_index = ( self.page -1 ) * self.perpage
            #for item in mydb['Event'].find(self.filter_args).sort('CreateTime',-1).skip(start_index).limit(self.perpage):
            rows =[]
            
            for item in mydb['Event'].find(self.filter_args).skip(start_index).limit(self.perpage):
                dc ={
                    '_director_name':'web_match_data.edit_self'
                }
                item.pop('_id')
                dc.update(item)
                rows.append(dc)
            
            matchid_list = [x.get('MatchID') for x in rows if x.get('MatchID')]
            dc ={}
            for inst in TbMatch.objects.filter(matchid__in=matchid_list):
                dc[inst.matchid] = inst
            for row in rows:
                if row.get('MatchID'):
                    match_inst = dc.get(row.get('MatchID'))
                    row['_MatchID_label'] = str( match_inst )
                    row.update( sim_dict( match_inst ) )
                row.update({
                    'pk':row.get('Eid'),
                    'TeamSwap':bool(row.get('TeamSwap'))
                })
            return rows
        
        @classmethod
        def clean_search_args(cls, search_args):
            if search_args.get('_first','1') == '1':
                search_args['_first'] = '0'
                search_args['_start_EventDateTime'] = ( timezone.now() - timezone.timedelta(days=1) ).strftime('%Y-%m-%d %H:%M:%S')
                search_args['_end_EventDateTime'] = ( timezone.now() + timezone.timedelta(days=1) ).strftime('%Y-%m-%d %H:%M:%S')
            return search_args
        
        def getRowFilters(self):
            
            return [
                {'name':'Team','label':'球队名字','editor':'com-filter-text'},
                {'name':'EventDateTime','label':'日期','editor':'com-filter-datetime-range'},
                {'name':'LeagueZh','label':'联赛','editor':'com-filter-select','options':[
                    ]},
                {'name':'ContrastStatus','label':'抓取状态','editor':'com-filter-select','options':[
                    {'value':1,'label':'抓取中'},
                    {'value':2,'label':'已爬取'}
                ]},
                {'name':'TeamSwap','label':'交换主客队','editor':'com-filter-select','options':[
                    {'value':1,'label':'交换'},
                    {'value':2,'label':'未交换'}
                ]}
            ]
        
        def getRowPages(self):
            return {
                'crt_page':self.page,
                'total':mydb['Event'].find(self.filter_args).count(),
                'perpage':self.perpage,
            }
        
        def get_operation(self):
            return [
                 {'editor':'com-op-btn','label':'设置字段','icon': 'fa-gear',
                  'action':'cfg.pop_vue_com("com-panel-table-setting",{table_ps:scope.ps,title:"字段调整"})'},
                {'name':'director_call',
                 'director_name':'event_match.start_scrapy',
                 'editor':'com-op-btn',
                 'label':'启动抓取',
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
                 'label':'停止抓取',
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
                
                
            ]
        

class WebMatchForm(Fields):
    def get_heads(self):
        return [
            {'name':'Team1En','label':'英文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team1Zh','label':'主队中文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team2En','label':'客队英文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team2Zh','label':'客队中文名','editor':'com-field-linetext','readonly':True},
            {'name':'MatchID','label':'比赛','editor':'com-field-pop-table-select',
             'table_ctx':MatchPicker().get_head_context(),'options':[]},
            
        ]
    
    
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
        out_dc.update({
            'pk':dc.get('Eid'),
            'TeamSwap':bool(dc.get('TeamSwap'))
        })
        return out_dc
    
    def get_org_dict(self,row=[]):
        return {}
    
    def save_form(self):
        #if self.kw.get('_my_swap_team'):
            #if self.kw.get('TeamSwap'):
                #mydb['Event'].update({'Eid':self.kw.get('Eid')}, {'$set': {'TeamSwap':False}})
            #else:
                #mydb['Event'].update({'Eid':self.kw.get('Eid')}, {'$set': {'TeamSwap':True}})
        #else:
        dc = {'MatchID':self.kw.get('matchid'),'TeamSwap':self.kw.get('TeamSwap')}
        mydb['Event'].update({'Eid':self.kw.get('Eid')}, {'$set': dc})
        
        

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
            head['action'] = 'delete scope.row._director_name;ex.vueAssign(scope.ps.par_row,scope.row);scope.ps.vc.$emit("finish");cfg.show_load();ex.director_call("d.save_row",{row:scope.ps.par_row}).then((resp)=>{cfg.hide_load();ex.vueAssign(scope.ps.par_row,resp.row)})'
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
    
    if mydb['Event'].find({"ContrastStatus":1}).count() +len(rows) > 20:
        raise UserWarning('最多同时爬取20场比赛!')
    
    for row in rows:
        msg = {'MatchID':row.get('MatchID'),'Eid':row.get('Eid'),'EventTeam':row.get('EventTeam'),'Source':'Backend','Action':'Start'}
        notifyScrapyMatch( json.dumps( msg,ensure_ascii=False) )

@director_view('event_match.stop_scrapy')
def start_scrapy(rows,**kws):
    for row in rows:
        msg = {'MatchID':row.get('MatchID'),'Eid':row.get('Eid'),'EventTeam':row.get('EventTeam'),'Source':'Backend','Action':'Stop'}
        notifyScrapyMatch( json.dumps( msg,ensure_ascii=False) )


director.update({
    'web_match_data':OtherWebMatchPage.tableCls,
    'web_match_data.edit_self':WebMatchForm,
    'matchpicker':MatchPicker
})

page_dc.update({
    'web_match_data':OtherWebMatchPage
})