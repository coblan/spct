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
  
        
        def get_heads(self):
            select_table_ctx =MatchPicker().get_head_context()
            
            return [
                 {'name':'Team1En','label':'主队英文名','editor':'com-table-click','width':130,
                 'table_ctx':select_table_ctx,
                 'action':'''scope.ps.selected = [scope.row];scope.head.table_ctx.par_row=scope.row; 
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
                {'name':'Team2Zh','label':'客队英文名','editor':'com-table-span','width':130},
                {'name':'team2zh','label':'客队英文名(Betradar)','editor':'com-table-span','width':130,'class':'matched_match'},
                {'name':'EventDateTime','label':'比赛日期','editor':'com-table-span','width':150},
                {'name':'LeagueZh','label':'联赛','editor':'com-table-span','width':120},
                {'name':"MatchID",'label':'比赛(比对结果)','editor':'com-table-label-shower','width':300},
            ]
        
        def get_rows(self):
            start_index = ( self.page -1 ) * self.perpage
            #for item in mydb['Event'].find(self.filter_args).sort('CreateTime',-1).skip(start_index).limit(self.perpage):
            rows =[]
            
            for item in mydb['Event'].find(self.filter_args).skip(start_index).limit(self.perpage):
                dc ={
                    '_director_name':'web_match_data.edit_self'
                }
                for k,v in item.items():
                    if k in ['Team1En','Team1Zh','Team2En','Team2Zh','MatchID','Eid','EventDateTime','LeagueZh','EventTeam']:
                        dc[k]=v
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
            return rows
        
        def getRowFilters(self):
            return [
                {'name':'Team','label':'球队名字','editor':'com-filter-text'},
                {'name':'EventDateTime','label':'日期','editor':'com-filter-datetime-range'},
                {'name':'LeagueZh','label':'联赛','editor':'com-filter-text'},
            ]
        
        def getRowPages(self):
            return {
                'crt_page':self.page,
                'total':mydb['Event'].find(self.filter_args).count(),
                'perpage':self.perpage,
            }
        
        def get_operation(self):
            return [
                {'name':'director_call',
                 'director_name':'event_match.start_scrapy',
                 'editor':'com-op-btn',
                 'label':'启动抓取',
                 'row_match':'many_row',
                 'match_express':'Boolean( scope.row.MatchID )',
                 'match_msg':'只能选择已经匹配完成的比赛',
                 'confirm_msg':'确定启动这些比赛抓取', 
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
    
    
    def get_row(self):
        dc = mydb['Event'].find_one({'Eid':self.kw.get('Eid')})
        out_dc = {
             '_director_name':'web_match_data.edit_self'
        }
        for k,v in dc.items():
            if k in ['Team1En','Team1Zh','Team2En','Team2Zh','MatchID','Eid','EventDateTime','LeagueZh','EventTeam']:
                out_dc[k]=v
                
        if out_dc.get('MatchID'):
            inst = TbMatch.objects.get(matchid=out_dc.get('MatchID') )
            out_dc.update(sim_dict( inst ))
            out_dc.update({
                '_MatchID_label':str(inst) 
            })
                
        return out_dc
    
    def save_form(self):
        dc = {'MatchID':self.kw.get('matchid')}
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
    for row in rows:
        msg = {'MatchID':row.get('MatchID'),'Eid':row.get('Eid'),'EventTeam':row.get('EventTeam'),'Source':'Backend'}
        notifyScrapyMatch( json.dumps( msg,ensure_ascii=False) )
        


director.update({
    'web_match_data':OtherWebMatchPage.tableCls,
    'web_match_data.edit_self':WebMatchForm,
    'matchpicker':MatchPicker
})

page_dc.update({
    'web_match_data':OtherWebMatchPage
})