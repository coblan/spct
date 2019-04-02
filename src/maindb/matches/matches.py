# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable, TablePage, page_dc, ModelFields, RowFilter, RowSort, \
    SelectSearch, Fields, director_view
from ..models import TbMatches, TbOdds, TbMatchesoddsswitch, TbOddstypegroup,TbTournament,\
     TbLivescout,TbMatch,TbPeriodscore,TbMarkets,TbMarkethcpswitch
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from helpers.director.base_data import director
from maindb.mongoInstance import updateMatchMongo
from maindb.rabbitmq_instance import closeHandicap
import json
from ..redisInstance import redisInst
from django.db.models import Q
import urllib
import requests
from django.conf import settings
from helpers.director.model_func.dictfy import to_dict
import functools
from .match_outcome_forms import FootBallPoints, NumberOfCorner
from helpers.director.middleware.request_cache import get_request_cache
from django.db import connections
import datetime

import logging
op_log = logging.getLogger('operation_log')


class MatchsPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self, prefer=None):
        return '比赛信息'

    def get_context(self):
        ctx = super().get_context()
        match_form = MatchForm(crt_user=self.crt_user)
        match_tabs=[
            {'name':'match_base_info',
             'label':'基本信息',
             'com':'com-tab-fields',
             'get_data': {
                 'fun': 'get_row',
                 'kws': {
                     'director_name': match_form.get_director_name(),
                     'relat_field': 'matchid',
                 }
             },
             'after_save': {
                 'fun': 'update_or_insert'
             },
             'heads': match_form.get_heads(),
             'ops': match_form.get_operations()             
            },
            {
                'name':'peroidscore',
                'label':'比分',
                'com':'com-tab-table',
                'pre_set':'rt={matchid:scope.par_row.matchid}',
                'table_ctx': PeriodScoreTab(crt_user=self.crt_user).get_head_context(),
                #'visible': can_touch(TbLivescout, self.crt_user), 
             },
            {
                'name':'danger_football',
                'label':'危险球',
                'com':'com-tab-table',
                'par_field': 'matchid',
                'table_ctx': TbLivescoutTable(crt_user=self.crt_user).get_head_context(),
                #'visible': can_touch(TbLivescout, self.crt_user), 
                },
            {'name': 'special_bet_value',
             'label': '盘口',
             'com': 'com-tab-special-bet-value',
             'update_director': 'get_special_bet_value',
             'save_director': 'save_special_bet_value',
             'ops': [
                 {'fun': 'save', 'label': '保存', 'editor': 'com-op-plain-btn', 'icon': 'fa-save', },
                 {'fun': 'refresh', 'label': '刷新', 'editor': 'com-op-plain-btn', 'icon': 'fa-refresh', }, 
                 {'fun':'filter_name','label':'玩法过滤','editor':'com-op-search',
                  'icon':'fa-refresh','btn_text':False},
             ]
            },
            {
                'name':'manul_outcome',
                'label':'手动结算',
                'com':'com-tab-table',
                'par_field': 'matchid',
                'table_ctx': OutcomeTab(crt_user=self.crt_user).get_head_context(),
                #'visible': can_touch(TbLivescout, self.crt_user), 
            },
            
                  
        ]
        
        ctx['named_ctx'] = {
            'match_tabs':match_tabs,
            }
        return ctx
    
    class tableCls(ModelTable):
        sportid=1
        model = TbMatch
        exclude = []  # 'ishidden', 'iscloseliveodds'
        fields_sort = ['matchid', 'tournamentid', 'team1zh', 'team2zh', 'matchdate', 'score',
                       'winner', 'statuscode', 'isrecommend', 'hasliveodds', 'isshow', 'openlivebet', 'marketstatus']

        def getExtraHead(self):
            return [{'name': 'isshow', 'label': '显示'}, {'name': 'openlivebet', 'label': '开启走地'}]
        
        @classmethod
        def clean_search_args(cls, search_args):
            now = datetime.datetime.now()
            if search_args.get('_start_matchdate')==None and search_args.get('_end_matchdate')==None:
                search_args['_start_matchdate']=now.strftime("%Y-%m-%d 00:00:00")
                search_args['_end_matchdate']=now.strftime("%Y-%m-%d 23:59:59")       
            return search_args
                
        def inn_filter(self, query):
            return query.filter(sportid=self.sportid).extra(select={
                '_tournamentid_label':'SELECT TB_Tournament.tournamentnamezh'},
                where=['TB_Tournament.TournamentID=TB_Match.TournamentID AND TB_Tournament.SportID=%s'%self.sportid],
                tables =['TB_Tournament']
            )

        class filters(RowFilter):
            range_fields = ['matchdate']
            names = ['isrecommend', 'marketstatus','statuscode','tournamentid']
            fields_sort=['isrecommend', 'marketstatus', 'statuscode','tournamentid','matchdate']
            def getExtraHead(self):
                return [
                    {'name':'specialcategoryid','editor':'com-filter-select','label':'类型',
                     'options':[
                        {'value':0,'label':'常规'},
                        {'value':1,'label':'特殊'}
                    ],
                     }
                ]
            
            def clean_query(self, query):
                if self.kw.get('specialcategoryid')==0:
                    return query.filter(specialcategoryid__lte=0)
                elif self.kw.get('specialcategoryid')==1:
                    return query.filter(specialcategoryid__gt=0)
                else:
                    return query
                
            def dict_head(self, head):
                if head['name']=='statuscode':
                    head['options']=list( filter(lambda x:x['value'] in [0,6,7,31,40,100,110,120],head['options']) )
                
                if head['name'] == 'tournamentid':
                    #head['editor'] = 'com-filter-search-select'
                    head['editor'] = 'com-filter-single-select2'
                    head['placeholder'] = '请选择联赛'
                    head['style'] = 'width:200px;'
                    head['options']=[
                        {'value':x.tournamentid,'label':str(x)} for x in TbTournament.objects.filter(sportid=1)
                    ]
                return head

        class search(SelectSearch):
            names = ['team1zh']
            exact_names = ['matchid']

            def get_option(self, name):
                if name == 'team1zh':
                    return {'value': 'team1zh', 'label': '球队名称', }
                else:
                    return super().get_option(name)

            def get_express(self, q_str):
                if self.qf == 'team1zh':
                    return Q(team1zh__icontains=q_str) | Q(team2zh__icontains=q_str)
                else:
                    return super().get_express(q_str)

        class sort(RowSort):
            names = ['matchdate']

        def get_operation(self):
            points_form =  FootBallPoints(crt_user= self.crt_user)
            corner_form = NumberOfCorner(crt_user= self.crt_user)
            
            PeriodTypeForm_form =  PeriodTypeForm(crt_user= self.crt_user)
            
            #spoutcome_form =  SpOutcome(crt_user= self.crt_user)
            ops = [
                 #'match_express': 'scope.row.specialcategoryid <= 0 ',
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '推荐', 'confirm_msg': '确认推荐吗？',
                 'pre_set': 'rt={isrecommend:1}', 'row_match': 'many_row', 
                 'match_msg': '只能推荐常规比赛。',
                 'visible': 'isrecommend' in self.permit.changeable_fields(),},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '取消推荐', 'confirm_msg': '确认取消推荐吗？',
                 'pre_set': 'rt={isrecommend:0}', 'row_match': 'many_row',
                 'match_msg': '只能取消推荐常规比赛。',
                 'visible': 'isrecommend' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '走地', 'confirm_msg': '确认打开走地吗？',
                 'field': 'iscloseliveodds',
                 'value': 0,  'visible': 'iscloseliveodds' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '取消走地', 'confirm_msg': '确认取消走地吗？',
                 'field': 'iscloseliveodds',
                 'value': 1, 'visible': 'iscloseliveodds' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '显示', 'confirm_msg': '确认显示比赛吗？',
                 'field': 'ishidden',
                 'value': 0, 'visible': 'ishidden' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '隐藏', 'confirm_msg': '确认隐藏比赛吗？',
                 'field': 'ishidden',
                 'value': 1, 'visible': 'ishidden' in self.permit.changeable_fields()},
                #{'fun': 'express', 'editor': 'com-op-btn', 'label': '封盘', 'row_match': 'one_row',
                    #'express': 'rt=scope.ts.switch_to_tab({tab_name:"special_bet_value",ctx_name:"match_iscloseliveodds_tabs",par_row:scope.ts.selected[0]})',
                            #'visible': self.permit.can_edit(),}, 
                 {'fun': 'director_call', 'editor': 'com-op-btn', 
                  'director_name': 'football_quit_ticket',
                  'label': '退单', 'confirm_msg': '确认要退单吗？', 'row_match': 'one_row',
                  'pre_set': 'rt={PeriodType:2}',
                  #'after_save': 'rt=cfg.showMsg(scope.new_row.Message)',
                 'fields_ctx': PeriodTypeForm_form.get_head_context(),
                 'visible': 'ishidden' in self.permit.changeable_fields()},
                 
            ]
            return ops
        
        def dict_head(self, head):
            dc = {
                'matchid': 70,
                'matchdate': 120,
                'tournamentid': 160,
                'team1zh': 120,
                'team2zh': 120,
                'score': 80,
                'winner': 60,
                'statuscode': 70,
                'roundinfo': 60,
                'isrecommend': 50,
                'livebet': 60,
                'ishidden': 50,
                'categoryid': 80,
                'currentperiodstart': 150,
                'maxsinglepayout': 120,
                'marketstatus': 70,
                'iscloseliveodds': 70
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'matchdate':
                head['editor'] = 'com-table-label-shower'
            if head['name'] in ('iscloseliveodds', 'openlivebet', 'isshow'):
                head['editor'] = 'com-table-bool-shower'
            
            if head['name']=='matchid':
                head['editor']='com-table-switch-to-tab'
                head['ctx_name']='match_tabs'
                head['tab_name']='match_base_info'            
            
            if head['name']=='tournamentid':
                head['editor']='com-table-label-shower'
            # 弹出 table 框
            #if head['name']=='tournamentzh':
                #mytable = TbLivescoutTable(crt_user=self.crt_user)
                #director_name = mytable.get_director_name()
                #head.update({
                    #'editor':'com-table-pop-table',
                    #'table_ctx':mytable.get_head_context(),
                    
                #})
              
            return head

        def dict_row(self, inst):
            return {
                '_matchid_label': '%(home)s VS %(away)s' % {'home': inst.team1zh, 'away': inst.team2zh},
                '_matchdate_label': str(inst.matchdate)[: -3],
                'isshow': not bool(inst.ishidden),
                'openlivebet': not bool(inst.iscloseliveodds),
                '_tournamentid_label':inst._tournamentid_label
            }
 
#@director_view('get_football_league_options')
#def get_football_league_options(source=0):
    #ls =[{'label':str(x) ,'value':x.tournamentid} for x in TbTournament.objects.filter(source=source)]
    #return ls
      
  
@director_view('football_quit_ticket')
def football_quit_ticket(rows, new_row): 
    return quit_ticket(rows, new_row, sportid = 1)

def quit_ticket(rows, new_row, sportid = 1): 
    PeriodType = new_row.get('PeriodType')
    row = rows[0]
    url = urllib.parse.urljoin( settings.CENTER_SERVICE, '/Match/ManualResulting')
    data ={
        'MatchID':row.get('matchid'),
        'SportID': sportid, 
        'OrderBack': True,
        'PeriodType': PeriodType,  # 1上半场 0全场 2 上半场+ 全场
    }    
    
    rt = requests.post(url,data=data)
    dc = json.loads( rt.text ) 
    
    op_log.info('执行%(type)s Matchid=%(matchid)s退单操作! PeriodType=%(PeriodType)s' % {'type': {0: '足球',1: '篮球',}[sportid],
                                                            'matchid': row.get('matchid'), 
                                                            'PeriodType': PeriodType,})
    return {'msg': dc.get('Message'),}


class MatchForm(ModelFields):
    
    proc_map = {
        0: FootBallPoints,
        2: NumberOfCorner,
    }
    
    class Meta:
        model = TbMatch
        exclude = ['marketstatus', 'matchstatustype', 'specialcategoryid', 'mainleagueid', 
                   'mainhomeid', 'mainawayid', 'mainmatchid', 'maineventid', 'settlestatus', ]

    field_sort = ['matchid', 'team1zh', 'team2zh', 'matchdate']

    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw):
        if kw.get('matchid'):
            matchid = kw.get('matchid')
            match = self.Meta.model.objects.get(matchid=matchid)
            super().__init__(dc, pk, crt_user, nolimit,instance=match, *args, **kw)
        else:
            super().__init__(dc, pk, crt_user, nolimit, *args, **kw)
        
    def dict_head(self, head):
        if head['name'] == 'matchid':
            head['readonly'] = True
        return head

    def dict_row(self, inst):
        return {'isshow': not bool(inst.ishidden),
                'openlivebet': not bool(inst.iscloseliveodds),
                '_matchdate_label':inst.matchdate.strftime('%Y-%m-%d %H:%M'),
                }
    
    def clean_save(self):
        if 'matchdate' in self.changed_data:
            self.instance.prematchdate = self.instance.matchdate - datetime.timedelta(minutes=15)
            
    
    def save_form(self):
        msg = []
        if self.kw.get('meta_type') == 'manul_outcome':
            specialcategoryid = self.kw.get('specialcategoryid')
            ProcCls = self.proc_map.get(specialcategoryid)
            proc_obj = ProcCls(crt_user = self.crt_user)
            self.instance.settletime = datetime.datetime.now()
            rt_msg =  proc_obj.manul_outcome( self.kw, self.instance)
            msg.append(rt_msg)
        else:
            super().save_form()
            
        self.updateMongo()
        self.proc_redis()
        return {'msg': msg,}
    
    def updateMongo(self): 
        match =  self.instance
        dc = {
            'MatchID': match.matchid,
            'IsRecommend': match.isrecommend,
            'IsHidden': match.ishidden,
            'IsCloseLiveOdds': match.iscloseliveodds, 
            'Team1ZH': match.team1zh,
            'Team2ZH': match.team2zh,
            'StatusCode': match.statuscode,
            #'Period1Score': match.period1score,
            'MatchScore': match.score,
            'Winner': match.winner,
            'MatchDate':match.matchdate.replace(tzinfo= datetime.timezone.utc ), #datetime.timezone(datetime.timedelta(hours=8))).astimezone(datetime.timezone.utc),
            'PreMatchDate':match.prematchdate.replace(tzinfo= datetime.timezone.utc ), #datetime.timezone(datetime.timedelta(hours=8))).astimezone(datetime.timezone.utc)
        }        
        updateMatchMongo(dc)
    
    def proc_redis(self): 
        if 'iscloseliveodds' in self.changed_data:
            if self.instance.iscloseliveodds == 0:
                redisInst.delete('backend:match:iscloseliveodds:%(matchid)s' % {'matchid': self.instance.eventid})
            else:
                redisInst.set('backend:match:iscloseliveodds:%(matchid)s' % {'matchid': self.instance.eventid}, 1,
                              60 * 1000 * 60 * 24 * 7)

class PeriodTypeForm(Fields):
    def get_heads(self): 
        return [
            {'name': 'PeriodType','label': 'PeriodType','editor': 'sim_select','options': [
                {'value': 0, 'label': '全场',}, 
                #{'value': 1, 'label': '上半场',}, 
                {'value': 2, 'label': '上半场+全场',}
                ],}
        ]
    def get_row(self): 
        return {
            'PeriodType': 2,
            '_director_name': self.get_director_name(),
        }
    

class TbLivescoutTable(ModelTable):
    """危险球表格"""
    model = TbLivescout
    exclude=[]
    fields_sort=['id','matchid','betstatus','matchtime','matchscore','stopreason','eventdesc','servertime','createtime']
    def get_operation(self):
        return [
            {'name':'director_call',
             'director_name':'match.add_livescout',
             'editor':'com-op-switch',
            'label':'危险球',
            'pre_set':'rt={matchid:scope.ps.crt_row.matchid,is_danger:scope.head.value}',
            #'pre_set':'', # 预先设置的字
            'active_color':'red',
            'op_confirm_msg':'scope.value?"是否开启危险球?":"是否关闭危险球?"',
            'after_save':'rt=scope.ts.search()',
            'init_express':'rt=ex.director_call("match.livescout_status",{matchid:scope.ps.vc.par_row.matchid}).then((resp)=>scope.vc.myvalue=resp)'
            },
              {
                  'name':'search',
                  'editor':'com-op-btn',
                  'label':'刷新',
                  'icon':'fa-refresh',
                  'class':'btn btn-sm btn-success',
        
            },
        ]
    
    def dict_head(self, head):
        width_dc={
            'servertime':150,
            'createtime':150,
            'stopreason':150,
        }
        if width_dc.get(head['name']):
            head['width']=width_dc.get(head['name'])
        return head
    
    def getExtraHead(self):
        return [
            {'name':'stopreason','label':'危险球原因'}
        ]
    
    def inn_filter(self, query):
        query = super().inn_filter(query)
        query = query.extra(select={'stopreason':'SELECT TB_BetStopReason.description'},
                    where=['TB_BetStopReason.id =TB_LiveScout.BrExtraInfo'],
                    tables =['TB_BetStopReason'])
        if self.kw.get('matchid'):
            return query.filter(matchid=self.kw.get('matchid'),eventtypeid__in=[33,34]).order_by('-createtime')
        else:
            return query  
    
    def dict_row(self, inst):
        return {
            'stopreason':inst.stopreason
        }

@director_view('PeriodScoreTab')
class PeriodScoreTab(ModelTable):
    model = TbPeriodscore
    exclude=[]
    
    def inn_filter(self, query):
        return query.filter(matchid = self.kw.get('matchid')).order_by('periodnumber')
    
    def dict_head(self, head):
        if head['name']=='statuscode':
            head['editor']='com-table-mapper'
        return head

@director_view('match.livescout_status')
def match_livescout_status(matchid,**kws):
    live = TbLivescout.objects.filter(matchid=matchid,eventtypeid__in=[33,34]).order_by('-createtime').first()
    if live and live.eventtypeid ==33:    
        return False
    else:
        return True

@director_view('match.add_livescout')
def add_livescout(new_row,**kws):
    match = TbMatches.objects.get(matchid=new_row.get('matchid'))
    #TbLivescout.objects.order_by('-createtime').first()
    if new_row.get('is_danger'):
        TbLivescout.objects.create(matchstatusid=0,brextrainfo='999',matchid=new_row.get('matchid'),matchscore=match.score,eventtypeid=34,typeid=1011,betstatus=3,scoutfeedtype=2,eventdesc='BetStop')
    else:
        TbLivescout.objects.create(matchstatusid=0,brextrainfo='999',matchid=new_row.get('matchid'),matchscore=match.score,eventtypeid=33,typeid=1010,betstatus=2,scoutfeedtype=2,eventdesc='BetStart')
        with connections['Sports'].cursor() as cursor:
            sql_args = {
                'MatchID':new_row.get('matchid')
            }
            sql = r"exec dbo.SP_DangerousBack_V1 %(MatchID)s" \
                  % sql_args
            cursor.execute(sql)        
    return {'success':True}
 

@director_view('get_special_bet_value')
def getSpecialbetValue(matchid):
    """
    获取封盘状态数据
    """
    try:
        #TbMatchesoddsswitch.objects.get(matchid=matchid,sportid = sportid, status=1, oddstypegroup_id=0)
        match_opened = True
    except:
        match_opened = True
        
    markets =[]
    specialbetvalue = []
    # 填充玩法
    for market in TbMarkets.objects.filter(enabled=1):
        markets.append({
            'name':market.marketnamezh,
            'marketid':market.marketid,
            'sort':market.sort,
            'opened':True,
        })
    
    # 填充盘口   
            #.values('marketname', 'specialbetvalue','specifiers',
                    #'handicapkey')
    for odd in TbOdds.objects.filter(matchid=matchid, status=1,):
        if odd.specialbetvalue != '':
            name = "%s %s" % (odd.marketname, odd.specialbetvalue)
            spbetname = '±%s'%odd.specialbetname[1:] if odd.specialbetname.startswith( ('+','-')) else odd.specialbetname
            specialbetvalue.append(
                {
                    'name':name,
                    'marketname': odd.marketname,
                    'marketid':odd.marketid,
                    #'oddstypegroup': odd['oddstype__oddstypegroup'],
                    'specialbetvalue': odd.specialbetvalue,
                    'specialbetname':spbetname,
                    'specifiers':odd.specifiers,
                    'opened': True,
                    #'Handicapkey': odd['handicapkey'],
                }
            )    
    
    # 把 以前操作过的 盘口 加进来。因为这时通过tbOdds 已经查不到这些 sp value了
    for switch in TbMarkethcpswitch.objects.filter(matchid=matchid,type=3, status = 1).select_related('marketid'):
        name = "%s %s" % (switch.marketid.marketnamezh, switch.specialbetvalue)
        
        specialbetvalue.append(
            {
                'name': name,
                'marketid':switch.marketid_id,
                #'oddstypegroup': switch.oddstypegroup_id,
                'marketname':switch.marketname,
                'specialbetname':switch.specialbetname,
                'specialbetvalue': switch.specialbetvalue,
                'specifiers':switch.specifiers,
                'opened': switch.status == 0,
                #'Handicapkey': switch.handicapkey,
                #'BetTypeId': switch.bettypeid,
                #'PeriodType': switch.periodtype,
            }
        )

        # 去重
    tmp_dc = {}
    tmp_ls = []
    for i in specialbetvalue:
        name = "%s_%s" % (i['specialbetvalue'], i['marketid'])
        if name not in tmp_dc:
            tmp_dc[name] = ''
            tmp_ls.append(i)
    specialbetvalue = tmp_ls

    for oddsswitch in TbMarkethcpswitch.objects.filter(matchid=matchid,status=1, marketid__enabled=1):
        # 1 封盘 比赛 这个 OddsTypeGroup =0 所以这里筛选条件里面没有它
        # if oddsswitch.types==1:
        # match_opened =False
        # 2 封盘 玩法
        if oddsswitch.type == 2:
            for i in markets:
                if i['marketid'] == oddsswitch.marketid_id:
                    i['opened'] = False
        # 3 封盘 值 specialbetvalue
        elif oddsswitch.type == 3:
            for i in specialbetvalue:
                if i['marketid'] == oddsswitch.marketid_id and \
                   i['specialbetvalue'] == oddsswitch.specialbetvalue:
                    i['opened'] = False

    return {
        'match_opened': match_opened,
        'markets': markets,
        'specialbetvalue': specialbetvalue,
    }



@director_view('save_special_bet_value')
def save_special_bet_value_proc(matchid, markets, specialbetvalue):
    """
    存储封盘操作
    """
    # TbMatchesoddsswitch.objects.filter(matchid=matchid,status=1).delete()
    log_msg = '封盘操作：'
    batchOperationSwitch = []

    #matchSwitch, created = TbMarkethcpswitch.objects.get_or_create(matchid=matchid, types=1, defaults={'status': 0})

    #if not match_opened:
        #if matchSwitch.status == 0:
            #matchSwitch.status = 1
            #matchSwitch.save()
            #log_msg += '开启比赛%s;' % matchid
            #batchOperationSwitch.append(matchSwitch)
    #else:
        #if matchSwitch.status == 1:
            #matchSwitch.status = 0
            #matchSwitch.save()
            #log_msg += '关闭比赛%s;' % matchid
            #batchOperationSwitch.append(matchSwitch)
    
    dbOddSwitchs = list( TbMarkethcpswitch.objects.filter(matchid=matchid) )
    
    changedSwitch=[]
    for market in markets:
        #oddSwitch, created = TbMarkethcpswitch.objects.get_or_create(matchid=matchid, type=2,
                                                                        #marketid_id=market['marketid'],
        oddSwitch=None                                       #defaults={'status': 0})
        for item in dbOddSwitchs:
            if item.type==2 and item.marketid_id==market['marketid']:
                oddSwitch = item
                dbOddSwitchs.remove(item)
                break
        if not oddSwitch:
            oddSwitch = TbMarkethcpswitch(matchid=matchid, type=2,marketid_id=market['marketid'],status=100)
        
        if not market['opened']:
            if oddSwitch.status != 1:
                oddSwitch.status = 1
                log_msg += '屏蔽玩法：%s' % market['name']
                batchOperationSwitch.append(oddSwitch)
        else:
            if oddSwitch.status != 0:
                oddSwitch.status = 0
                log_msg += '开启玩法：%s' % market['name']
                batchOperationSwitch.append(oddSwitch)

    for spbt in specialbetvalue:
        for market in markets:
            if spbt['marketid'] == market['marketid']:
                par_market = market
                break
        
        spSwitch=None                                       
        for item in dbOddSwitchs:
            if item.type==3 and item.marketid_id==spbt['marketid'] and \
               item.specialbetvalue == spbt['specialbetvalue']:
                spSwitch = item
                dbOddSwitchs.remove(item)
                break
        if not spSwitch:
            spSwitch = TbMarkethcpswitch(matchid=matchid, type=3,marketid_id=market['marketid'],
                                         specialbetname=spbt['specialbetname'],marketname=spbt['marketname'],
                                         specialbetvalue=spbt['specialbetvalue'],specifiers=spbt['specifiers'],status=100)     
 
        #spSwitch, created = TbMarkethcpswitch.objects.get_or_create(matchid=matchid,  type=3,
                                                                      #marketid_id=par_market['marketid'],
                                                                      #specialbetvalue=spbt['specialbetvalue'],
                                                                      #defaults={'status': 0})
                                                                      
        if par_market['opened']:
            if not spbt['opened']:
                if spSwitch.status != 1:
                    spSwitch.status = 1
                    log_msg += '屏蔽盘口：%s' % spbt['specialbetvalue']
                    batchOperationSwitch.append(spSwitch)
            else:
                if spSwitch.status != 0:
                    spSwitch.status = 0
                    log_msg += '开启盘口：%s' % spbt['specialbetvalue']
                    batchOperationSwitch.append(spSwitch)
                        
    new_list = []
    changed_list=[]
    for item in [x for x in batchOperationSwitch]:
        if item.tid is None:
            if item.status==1:
                new_list.append(item)
                changed_list.append(item)
        elif  item.status==1:
            item.save()
            changed_list.append(item)
        else:
            changed_list.append(item)
            item.delete()
    TbMarkethcpswitch.objects.bulk_create(new_list)    
    op_log.info(log_msg)
    
    ls=[]
    for switch in changed_list:
        ls.append({
            'MatchID': switch.matchid,
            'Type': switch.type,
            'Marketid': switch.marketid_id,
            'SpecialBetValue': switch.specialbetvalue,
            'Specifiers':switch.specifiers,
            'Status': switch.status,
        })        
    closeHandicap(json.dumps(ls))
    
    # 请求service，关闭盘口
    #match = TbMatches.objects.get(matchid=matchid)
    #msg = ['TbMatchesoddsswitch操作成功']


    return {'success': True}  # ,'msg':msg}


class OutcomeTab(ModelTable):
    model = TbMarkets
    include =['marketid','marketname','marketnamezh']
    
    def getExtraHead(self):
        return [
            {'name':'outcome','label':'结算结果','editor':'com-table-json','width':250}
        ]
    
    def get_rows(self):
        bf = [
            {'marketid':'','pk':-1,'marketname':'score','marketnamezh':'比分型'}
        ]
        rows = super().get_rows()
        return bf+rows
    
    def dict_head(self, head):
        width={
            'marketname':240,
            'marketnamezh':250,
        }
        if head['name'] in width:
            head['width'] = width.get(head['name'])
        if head['name'] =='marketname':
            head['editor'] = 'com-table-click'
            head['action'] = 'var panel=scope.head.panel_map[scope.row.pk],\
            rt=cfg.pop_vue_com({editor:panel.editor,ctx:{row:scope.row.outcome,init_express:panel.init_express,layout:panel.layout,ops_loc:"bottom",heads:panel.heads,ops:panel.ops,par_row:scope.ps.vc.par_row,init_express:panel.init_express}})\
            .then(res=>Vue.set(scope.row,"outcome",res))'
            head.update({
                'panel_map':{
                    -1:{
                        'heads': [   # get_score_heads([6,7])+
                            {'name':'home_6_1','label':'主队上半场得分','editor':'com-field-linetext','required':True},
                            {'name':'away_6_1','label':'客队上半场得分','editor':'com-field-number','required':True},
                            {'name':'home_7_1','label':'主队下半场得分','editor':'com-field-number','required':True},
                            {'name':'away_7_1','label':'客队下半场得分','editor':'com-field-number','required':True},
                            {'name':'home_40_1','label':'主队加时赛得分','editor':'com-field-number','show':'scope.row.has_overtime'},
                            {'name':'away_40_1','label':'客队加时赛得分','editor':'com-field-number','show':'scope.row.has_overtime'},
                            {'name':'home_50_1','label':'主队点球大战得分','editor':'com-field-number','show':'scope.row.has_penalty'},
                            {'name':'away_50_1','label':'客队点球大战得分','editor':'com-field-number','show':'scope.row.has_penalty'},
                            
                            {'name':'home_6_5','label':'主队上半场角球','editor':'com-field-number',},
                            {'name':'away_6_5','label':'客队上半场角球','editor':'com-field-number',},
                            {'name':'home_7_5','label':'主队下半场角球','editor':'com-field-number',},
                            {'name':'away_7_5','label':'客队下半场角球','editor':'com-field-number',},
                            {'name':'home_40_5','label':'主队加时赛角球','editor':'com-field-number','show':'scope.row.has_overtime'},
                            {'name':'away_40_5','label':'客队加时赛角球','editor':'com-field-number','show':'scope.row.has_overtime'},
                            
                            
                            {'name':'has_overtime','label':'加时赛','editor':'com-field-bool'},
                            {'name':'has_penalty','label':'点球大战','editor':'com-field-bool'},
                            ],
                        'editor':'com-form-one', #'com-outcome-score',
                        'layout':{
                            #'table_grid':[['has_overtime','has_penalty'],
                                          #['home_6_1','away_6_1'],
                                          #['home_7_1','away_7_1'],
                                          #['home_40_1','away_40_1'],
                                          #['home_50_1','away_50_1'],
                                          #['home_6_5','away_6_5'],
                                          #['home_7_5','away_7_5'],
                                          #['home_40_5','away_40_5'],
                                          #],
                            'fields_group':[
                                {'name':'huji','label':'基本控制','head_names':['has_overtime','has_penalty']},
                                {'name':'huji','label':'比分','head_names':['home_6_1','away_6_1','home_7_1','away_7_1','home_40_1','away_40_1','home_50_1','away_50_1']},
                                {'name':'huji','label':'角球','head_names':['home_6_5','away_6_5','home_7_5','away_7_5','home_40_5','away_40_5']},
                            ]
                            },
                        'ops_loc':'down',
                        'ops':[
                            {'name':'save','label':'确定','editor':'com-op-btn','action':'rt=scope.ps.vc.isValid()?scope.ps.vc.$emit("finish",scope.ps.vc.row):""'}
                        ],
                        'init_express':'ex.director_call("get_match_outcome_info",{matchid:scope.vc.ctx.par_row.matchid}).then(res=>ex.vueAssign(scope.row,res))'
                        }
                }
            })
        return head
    
    def inn_filter(self, query):
        return query.filter(enabled=True,marketid__in = [8,9,100,101,102,103,104,105,106,107,108,109,110,163,174,291])
    
    def get_operation(self):
        return [
            {'name':'outcome','label':'结算','editor':'com-op-btn','action':'out_come_save(scope.ps.rows)'},
        ]
    
def get_score_heads(ls):
    dc = dict((
        (6, '上半场'),
        (7,'下半场'),
        (13,'第一节'),
        (14,'第二节'),
        (15,'第三节'),
        (16,'第四节'),
        (50,'点球'),
        (40,'加时赛'),
        (100,'全场'),
        (110,'加时赛'),
        (120,'点球大战'),
    ))
    
    bb = {1:'得分',5:'角球'} # ,2: '黄牌',3: '红牌' , 4:'黄红'
    tm = {1:[6,7,40,50],5:[6,7,40],} #2:[6,7,40,],3:[6,7,40],4:[6,7,40]
    out_heads =[]
    #for item in [6,7,40,100,50,]:
        #out_heads.append(
            #{'name':'home_%s_1'%item,'label':dc.get(item)+'比分','editor':'com-field-number'}
        #)
        #out_heads.append(
            #{'name':'away_%s_1'%item,'label':dc.get(item)+'比分','editor':'com-field-number'}
        #)
    
    for k,v1 in bb.items():
        for item in tm.get(k):
            out_heads.append(
                {'name':'home_%s_%s'%(item,k),'label':'主队'+dc.get(item)+v1,'editor':'com-field-number'}
            )
            out_heads.append(
                {'name':'away_%s_%s'%(item,k),'label':'客队'+dc.get(item)+v1,'editor':'com-field-number'}
            )
    
    
    return out_heads
  

@director_view('get_match_outcome_info')
def get_match_outcome_info(matchid):
   
    row ={}
    for score in TbPeriodscore.objects.filter(matchid=matchid):
        if score.statuscode in [6,7,13,14,15,16,40,50,]:
            row['home_%s_1'%score.statuscode] = score.home
            row['away_%s_1'%score.statuscode] = score.away
    return row

@director_view('out_com_save')
def out_com_save(rows):
    periodnumber_map ={
       6:1,
       7:2,
       13:1,
       14:2,
       15:3,
       16:4,
    }
    scoretype_map={
        6:1,
        7:1,
        13:1,
        14:1,
        15:1,
        16:1,
    }
    
    for row in rows:
        if row['pk'] == '-1':
            outcome = row['outcome']
            dc = {}
            for k,v in outcome.item():
                statuscode = k[5:]
                if statuscode not in dc:
                    dc[statuscode] = {'statuscode':statuscode}
                if k.startswith('home_'):
                    dc[statuscode].update({'home':v})
                elif k.startswith('away_'):
                    dc[statuscode].update({'away':v})
            for k,v in dc.items():
                TbPeriodscore.objects.update_or_create()
                
        



        #{'fun': 'pop_panel',
                 #'editor': 'com-op-btn',
                 ##'panel':  'com-panel-fields', #'com-form-produceMatchOutcomePanel',
                 #'panel_express': 'rt=manul_outcome_panel_express_parse(scope.kws.panel_map,scope.kws.play_type,scope.ts.selected[0].specialcategoryid)',
                 #'label': '手动结算',
                 #'row_match': 'one_row',
                 #'ctx_express': 'rt=manul_outcome_panel_ctx(scope.ts.selected[0],scope.kws,scope.ts.selected[0].specialcategoryid)',
                 #'play_type': {
                     #'normal': [0], 
                     #'corner': [2],
                     #'race-to-first-number-of-points': [185],
                     #},
                 #'row_adapt': {
                     #'normal': 'rt=scope.adaptor.parse_score(scope.row)',
                     #'corner': 'rt=scope.adaptor.parse_score(scope.row)',
                     #},
                 #'panel_map': {
                     #'normal': 'com-form-produceMatchOutcomePanel',
                     #'corner': 'com-form-produceMatchOutcomePanel',
                     #'race-to-first-number-of-points': 'com-panel-fields',
                     #},
                 #'ctx_dict': {
                     #'normal': points_form.get_head_context(),
                     #'corner': corner_form.get_head_context(),
                     #},
               
                 #'visible': self.permit.can_edit(),
                 #},
    
    
    

#@director_view('football_get_special_bet_value')
#def football_get_special_bet_value(matchid): 
    #return get_special_bet_value(matchid,sportid = 1 )

#def get_special_bet_value(matchid, sportid = 1 , oddsModel = TbOdds):
    #"""
    #获取封盘状态数据
    #"""
    #try:
        #TbMatchesoddsswitch.objects.get(matchid=matchid,sportid = sportid, status=1, oddstypegroup_id=0)
        #match_opened = False
    #except:
        #match_opened = True

    #oddstype = []
    #specialbetvalue = []

    #for odtp in TbOddstypegroup.objects.filter(enabled=1, sportid = sportid):
        #oddstype.append(
            #{
                #'name': odtp.oddstypenamezh,
                ## 'oddsid':odd.oddstype.oddsid,
                #'oddstypegroup': odtp.oddstypegroup,
                ## 'oddstypeid':odd.oddstype.oddstypeid,
                #'opened': True,
                #'sort': odtp.sort,
            #}
        #)

    #for odd in oddsModel.objects.filter(matchid=matchid, status=1,) \
            #.values('marketname', 'specialbetvalue',
                    #'handicapkey', 'oddstype__oddstypegroup__periodtype'):
        ## print(odd.specialbetvalue)
        #if odd['specialbetvalue'] != '':
            #name = "%s %s" % (odd['marketname'], odd['specialbetvalue'])
            #specialbetvalue.append(
                #{
                    #'name': name,
                    ##'oddstypegroup': odd['oddstype__oddstypegroup'],
                    #'specialbetvalue': odd['specialbetvalue'],
                    #'opened': True,
                    #'Handicapkey': odd['handicapkey'],
                    ##'BetTypeId': odd['oddstype__oddstypeid'],
                    #'PeriodType': odd['oddstype__oddstypegroup__periodtype'],
                #}
            #)

    ## 把 以前操作过的 spvalue 加进来。因为这时通过tbOdds 已经查不到这些 sp value了
    #for switch in TbMatchesoddsswitch.objects.filter(matchid=matchid, sportid = sportid,types=3, status = 1):
        #name = "%s %s" % (switch.oddstypegroup.oddstypenamezh, switch.specialbetvalue)
        #specialbetvalue.append(
            #{
                #'name': name,
                #'oddstypegroup': switch.oddstypegroup_id,
                #'specialbetvalue': switch.specialbetvalue,
                #'opened': switch.status == 0,
                #'Handicapkey': switch.handicapkey,
                #'BetTypeId': switch.bettypeid,
                #'PeriodType': switch.periodtype,
            #}
        #)

        ## 去重
    #tmp_dc = {}
    #tmp_ls = []
    #for i in specialbetvalue:
        #name = "%s_%s" % (i['specialbetvalue'], i['oddstypegroup'])
        #if name not in tmp_dc:
            #tmp_dc[name] = ''
            #tmp_ls.append(i)
    #specialbetvalue = tmp_ls

    #for oddsswitch in TbMatchesoddsswitch.objects.select_related('oddstypegroup').filter(matchid=matchid, status=1,sportid = sportid,
                                                                                         #oddstypegroup__enabled=1):
        ## 1 封盘 比赛 这个 OddsTypeGroup =0 所以这里筛选条件里面没有它
        ## if oddsswitch.types==1:
        ## match_opened =False
        ## 2 封盘 玩法
        #if oddsswitch.types == 2:
            #for i in oddstype:
                #if i['oddstypegroup'] == oddsswitch.oddstypegroup_id:
                    #i['opened'] = False
        ## 3 封盘 值 specialbetvalue
        #elif oddsswitch.types == 3:
            #for i in specialbetvalue:
                #if i['oddstypegroup'] == oddsswitch.oddstypegroup_id and i[
                    #'specialbetvalue'] == oddsswitch.specialbetvalue:
                    #i['opened'] = False

    #return {
        #'match_opened': match_opened,
        #'oddstype': oddstype,
        #'specialbetvalue': specialbetvalue,
    #}

#@director_view('football_save_special_bet_value')
#def football_save_special_bet_value(matchid, match_opened, oddstype, specialbetvalue): 
    #return save_special_bet_value_proc(matchid, match_opened, oddstype, specialbetvalue, sportid = 0)

#def save_special_bet_value_proc(matchid, match_opened, oddstype, specialbetvalue, sportid = 0):
    #"""
    #存储封盘操作
    #"""
    ## TbMatchesoddsswitch.objects.filter(matchid=matchid,status=1).delete()
    #log_msg = '封盘操作：'
    #batchOperationSwitch = []

    #matchSwitch, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, sportid = sportid, types=1, defaults={'status': 0})

    #if not match_opened:
        #if matchSwitch.status == 0:
            #matchSwitch.status = 1
            #matchSwitch.save()
            #log_msg += '开启比赛%s;' % matchid
            #batchOperationSwitch.append(matchSwitch)
        ## obj, created = TbMatchesoddsswitch.objects.update_or_create(matchid=matchid,types=1, defaults = { 'status': 1})
    #else:
        #if matchSwitch.status == 1:
            #matchSwitch.status = 0
            #matchSwitch.save()
            #log_msg += '关闭比赛%s;' % matchid
            #batchOperationSwitch.append(matchSwitch)

        #for odtp in oddstype:
            #playMethod, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, sportid = sportid, types=2,
                                                                            #oddstypegroup_id=odtp['oddstypegroup'],
                                                                            #defaults={'status': 0})

            #if not odtp['opened']:

                #if playMethod.status == 0:
                    #playMethod.status = 1
                    #playMethod.save()
                    #log_msg += '屏蔽玩法：%s' % odtp['oddstypegroup']
                    #batchOperationSwitch.append(playMethod)
            #else:
                #if playMethod.status == 1:
                    #playMethod.status = 0
                    #playMethod.save()
                    #log_msg += '开启玩法：%s' % odtp['oddstypegroup']
                    #batchOperationSwitch.append(playMethod)

        #for spbt in specialbetvalue:
            #oddstypegroup = spbt['oddstypegroup']
            #par_odd = None
            #for i in oddstype:
                #if oddstypegroup == i['oddstypegroup']:
                    #par_odd = i
                    #break
            #spSwitch, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, sportid = sportid, types=3,
                                                                          #oddstypegroup_id=par_odd['oddstypegroup'],
                                                                          #bettypeid=spbt['BetTypeId'],
                                                                          #periodtype=spbt['PeriodType'],
                                                                          #handicapkey=spbt['Handicapkey'],
                                                                          #specialbetvalue=spbt['specialbetvalue'],
                                                                          #defaults={'status': 0})
            #if par_odd['opened']:
                #if not spbt['opened']:
                    #if spSwitch.status == 0:
                        #spSwitch.status = 1
                        #spSwitch.save()
                        #log_msg += '屏蔽盘口：%s' % spbt['specialbetvalue']
                        #batchOperationSwitch.append(spSwitch)
                #else:
                    #if spSwitch.status == 1:
                        #spSwitch.status = 0
                        #spSwitch.save()
                        #log_msg += '开启盘口：%s' % spbt['specialbetvalue']
                        #batchOperationSwitch.append(spSwitch)
                        ## TbMatchesoddsswitch.objects.create(matchid=matchid,types=3,status=1,
                        ## oddstypegroup_id=par_odd['oddstypegroup'],
                        ## specialbetvalue=spbt['specialbetvalue'])
    #ls = []
    #for switch in batchOperationSwitch:
        #ls.append({
            #'MatchID': switch.matchid,
            #'SportID': sportid,
            #'Types': switch.types,
            #'OddsTypeGroup': switch.oddstypegroup_id,
            #'SpecialBetValue': switch.specialbetvalue,
            #'Status': switch.status,
            #'BetTypeId': switch.bettypeid,
            #'PeriodType': switch.periodtype,
            #'Handicapkey': switch.handicapkey,
        #})
    #closeHandicap(json.dumps(ls))

    #op_log.info(log_msg)
    
    ## 请求service，关闭盘口
    ##match = TbMatches.objects.get(matchid=matchid)
    ##msg = ['TbMatchesoddsswitch操作成功']


    #return {'status': 'success'}  # ,'msg':msg}

    
#@director_view('football_produce_match_outcome')
#def football_produce_match_outcome(row): 
    #return produce_match_outcome(row, MatchModel = TbMatches, sportid = 0, half_end_code = 31, updateMongo= updateMatchMongo)

#def produce_match_outcome(row, MatchModel , sportid, half_end_code = 31, updateMongo = updateMatchMongo):
    #"""
    #手动结算
    #""" 
    
    #match = MatchModel.objects.get(matchid = row.get('matchid'))
    #match.ishidden = True
    
    #crt_settlestatus = 0 if not match.settlestatus else match.settlestatus
    #settlestatus = crt_settlestatus
    #if crt_settlestatus < 1 and row.get('home_half_score', '') != '' and row.get('away_half_score', '') != '':
        #match.period1score = '%s:%s' % (row.get('home_half_score'), row.get('away_half_score'))
        #match.statuscode = half_end_code
        #settlestatus = 1
    #if crt_settlestatus < 2 and row.get('home_score', '') != '' and row.get('away_score', '') != '':
        #match.matchscore = '%s:%s' % (row.get('home_score'), row.get('away_score'))
        #match.homescore = row.get('home_score')
        #match.awayscore = row.get('away_score')   
        #match.statuscode = 100
        #settlestatus += 2
        #if row.get('home_score') > row.get('away_score'):
            #match.winner = 1
        #elif row.get('home_score') < row.get('away_score'):
            #match.winner = 2
        #else:
            #match.winner = 3
    
    #settle_dict =  {
            #1: '上半场',
            #2: '全场',
            #3: '半场&全场',
        #}
    #if crt_settlestatus < settlestatus:
        #match.settlestatus = settlestatus
    #else:
        
        #raise UserWarning('%s已经结算,请不要重复结算!' % settle_dict.get(settlestatus))
        
    #data = {
        #'SportID': sportid, 
        #'MatchID': row.get('matchid'),
        #'PeriodType': row.get('PeriodType'),
        #'OrderBack': False,
    #}
    #org_match = to_dict(match)
    #match.save()
    
    #url = urllib.parse.urljoin( settings.CENTER_SERVICE, '/Match/ManualResulting')
    #rt = requests.post(url,json=data)
    #rt_dc = json.loads( rt.text )
    #if not rt_dc.get('Success'):
        #for k in org_match:
            #if not k.startswith('_'):
                #setattr(match, k, org_match[k])
            #match.save()
        #op_log.info('手动结算足球比赛%(matchid)s的%(type)s，未成功,错误消息:%(msg)s' % {'matchid': match.matchid, 
                                                         #'type': settle_dict.get(match.settlestatus),
                                                        #'msg': rt_dc.get('Message',''),})
            
        #raise UserWarning( rt_dc.get('Message', '手动结算后端发生问题'))
    
    #rt_dc['row'] = to_dict(match)
    
    #dc = {
        #'MatchID': match.matchid,
        #'IsRecommend': match.isrecommend,
        #'IsHidden': match.ishidden,
        #'iscloseliveodds': match.iscloseliveodds, 
        #'Team1ZH': match.team1zh,
        #'Team2ZH': match.team2zh,
        #'StatusCode': match.statuscode,
        ##'Period1Score': match.period1score,
        #'Score': match.score,
        #'Winner': match.winner,
    #}
    #updateMongo(dc)    
    
    #op_log.info('手动结算足球比赛%(matchid)s的%(type)s，结算后比分为:上半场:%(period1score)s,全场:%(matchscore)s' % {'matchid': match.matchid, 
                                                     #'type': settle_dict.get(match.settlestatus),
                                                     #'period1score': match.period1score,
                                                     #'matchscore': match.matchscore,})
    #return rt_dc    





director.update({
    'match.table': MatchsPage.tableCls,
    'match.table.edit': MatchForm,
    #'PeriodTypeForm': PeriodTypeForm,
    
    'outcome_tab':OutcomeTab,
    'TbLivescout.table':TbLivescoutTable,
})

# model_dc[TbMatches]={'fields':MatchForm,'table':MatchsPage}

page_dc.update({
    'matches': MatchsPage
})
