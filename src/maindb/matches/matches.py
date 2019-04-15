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
from maindb.rabbitmq_instance import notifyManulOutcome
from . manul_outcome import outcome_header

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
                'pre_set': 'rt={matchid:scope.par_row.matchid}',
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
                  'director_name': 'match.quit_ticket',
                  'label': '退单', 'confirm_msg': '确认要退单吗？', 'row_match': 'one_row',
                  #'pre_set': 'rt={PeriodType:2}',
                  #'after_save': 'rt=cfg.showMsg(scope.new_row.Message)',
                 #'fields_ctx': PeriodTypeForm_form.get_head_context(),
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
      
  
#@director_view('football_quit_ticket')
#def football_quit_ticket(rows, new_row): 
    #return quit_ticket(rows, new_row, sportid = 1)

@director_view('match.quit_ticket')
def quit_ticket(rows,**kws ): 
    row = rows[0]
    send_dc = {
        'MatchID':row['matchid'],
        'SendTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Source':'AdminBackend',
        'IsSettleByScore':False,
        'Special':[],
        'Unsubscribe':True,
    }
    
    #PeriodType = new_row.get('PeriodType')
    #row = rows[0]
    #url = urllib.parse.urljoin( settings.CENTER_SERVICE, '/Match/ManualResulting')
    #data ={
        #'MatchID':row.get('matchid'),
        #'SportID': sportid, 
        #'OrderBack': True,
        #'PeriodType': PeriodType,  # 1上半场 0全场 2 上半场+ 全场
    #}    
    
    #rt = requests.post(url,data=data)
    #dc = json.loads( rt.text ) 
    notifyManulOutcome(json.dumps(send_dc))
    op_log.info('执行 Matchid=%(matchid)s 退单操作!' % {'matchid': row.get('matchid'), })
    return {'msg': '指令发送成功',}


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
            #'MatchDate':match.matchdate.replace(tzinfo= datetime.timezone.utc ), #datetime.timezone(datetime.timedelta(hours=8))).astimezone(datetime.timezone.utc),
            #'PreMatchDate':match.prematchdate.replace(tzinfo= datetime.timezone.utc ), #datetime.timezone(datetime.timedelta(hours=8))).astimezone(datetime.timezone.utc)
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
    hide_fields=['tid']
    model = TbPeriodscore
    exclude=['createtime']
    
    @classmethod
    def clean_search_args(cls, search_args):
        search_args['_sort']= search_args.get('_sort') or 'statuscode'
        return search_args
    
    def inn_filter(self, query):
        return query.filter(matchid = self.kw.get('matchid'))
    
    def dict_head(self, head):
        if head['name']=='statuscode':
            head['editor']='com-table-mapper'
        return head
    class sort(RowSort):
        names=['statuscode']

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
            'SpecialBetValue': switch.specialbetvalue or '',
            'Specifiers':switch.specifiers or '',
            'Status': switch.status,
        })  
    if ls:
        closeHandicap(json.dumps(ls))
    
    # 请求service，关闭盘口
    #match = TbMatches.objects.get(matchid=matchid)
    #msg = ['TbMatchesoddsswitch操作成功']


    return {'success': True}  # ,'msg':msg}


class OutcomeTab(ModelTable):
    model = TbMarkets
    selectable=False
    include =['marketid','marketname','marketnamezh']
    
    def getExtraHead(self):
        return [
            {'name':'outcome','label':'结果','editor':'com-table-json','width':250},
            {'name':'ops','label':'','editor':'com-table-ops-cell','width':50,
             'ops':[
                 {
                         'editor':'com-op-plain-btn',
                         'label':'清空',
                         'class':'btn btn-primary btn-xs',
                         'action':"""rt=scope.row.outcome=''"""}
                 ]},

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
            head.update(outcome_header)
        return head

    
    def inn_filter(self, query):
        # 291 是篮球的
        return query.filter(enabled=True,marketid__in = [8,9,100,101,102,103,104,105,106,107,108,109,110,163,174,])
    
    def get_operation(self):
        return [
            {'name':'outcome','label':'结算','editor':'com-op-btn','action':'rt=cfg.confirm("确定发送手动结算信息?").then(()=>out_come_save(scope.ps.rows,scope.ps.vc.par_row.matchid))'},
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
    for score in TbPeriodscore.objects.filter(matchid=matchid,statuscode__in=[6,7,40,50],scoretype__in=[1,5]):
        row['home_%s_%s'%(score.statuscode,score.scoretype)] = score.home
        row['away_%s_%s'%(score.statuscode,score.scoretype)] = score.away
        
    return row

@director_view('out_com_save')
def out_com_save(rows,matchid):

    send_dc = {
        'MatchID':matchid,
        'SendTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Source':'AdminBackend',
        'IsSettleByScore':False,
        'Special':[],
        'Unsubscribe':False,
        #public long MatchID { get; set; }
        #public DateTime SendTime { get; set; }
        #public string Source { get; set; }
        #public bool IsSettleByScore { get; set; }
        #public List<SpecialEntity> Special { get; set; }
    }

    which_map= {
                291:'pointnr=%(org_sp)s',
                174:'cornernr=%(org_sp)s',
                163:'cornernr=%(org_sp)s',
                8:'goalnr=%(org_sp)s',
                100:'goalnr=%(org_sp)s',
                101:'goalnr=%(org_sp)s',
                102:'%(org_sp)s',
                105:'%(org_sp)s',
                108:'%(org_sp)s',
      }

    batch_create=[]
    for row in rows:
        if row['pk'] == -1:
            # 足球手动输入比分
            send_dc['IsSettleByScore']=True
            dc = {}
            has_overtime = row.pop('has_overtime',False)
            has_penalty = row.pop('has_penalty',False)
            TbPeriodscore.objects.filter(matchid=matchid,scoretype__in=[1,5]).delete()
            total_home_1=0
            total_away_1=0
            total_home_5=0
            total_away_5=0
            
            if has_overtime:
                home = row.pop('home_40_1')
                away = row.pop('away_40_1')
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=1,type=1,home=home,away=away)) 
                home = row.pop('home_40_5')
                away = row.pop('away_40_5')
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=5,type=1,home=home,away=away) )

            if has_penalty:
                home = row.pop('home_50_1')
                away = row.pop('away_50_1')
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=50,scoretype=1,home=home,away=away ,type=2) )
                          
            home = row.get('home_6_1')
            away = row.get('away_6_1')
            total_home_1 += int( home )
            total_away_1 += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=6,scoretype=1,home=home,away=away ,type=0) )
            home = row.get('home_7_1')
            away = row.get('away_7_1')
            total_home_1 += int(home)
            total_away_1 += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=7,scoretype=1,home=home,away=away ,type=0) )
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,home=total_home_1,away=total_away_1 ,type=0) )
            
            home = row.get('home_6_5')
            away = row.get('away_6_5')
            total_home_5 += int(home)
            total_away_5 += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=6,scoretype=5,home=home,away=away ,type=0) )
            home = row.get('home_7_5')
            away = row.get('away_7_5')
            total_home_5 += int(home)
            total_away_5 += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=7,scoretype=5,home=home,away=away ,type=0) )
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=100,scoretype=5,home=total_home_5,away=total_away_5 ,type=0) )

        if row['pk'] in which_map:
            
            outcome_list = json.loads(row.get('content','[]') ) 
            for item in outcome_list:
                item['Specifiers'] = which_map[row['pk']]%{'org_sp':item['Specifiers']}
                item['MarketId']= row['pk']
                send_dc['Special'].append(item)
        if row['pk'] in [103,106,109]:
            outcome_list = json.loads(row.get('content','[]') ) 
            for item in outcome_list:
                item['Specifiers'] = 'goalnr='+item.pop('Specifiers_1')+item['Specifiers']
                item['MarketId']= row['pk']
                send_dc['Special'].append(item)
        if row['pk'] in [104,107,110]:
            outcome_list = json.loads(row.get('content','[]') ) 
            for item in outcome_list:
                item['Specifiers'] = 'total='+item.pop('Specifiers_1')+item['Specifiers']
                item['MarketId']= row['pk']
                item['Score'] = '%s:%s'%(item.pop('OutcomeId'),item.pop('OutcomeId_1') )
                send_dc['Special'].append(item)
        if row['pk'] == -2:
            # 普通篮球手动输入比分 （有四小节）
            send_dc['IsSettleByScore']=True
            dc = {}
            has_overtime = row.pop('has_overtime',False)
     
            TbPeriodscore.objects.filter(matchid=matchid,scoretype=1).delete()
            total_home = 0
            total_away = 0
            half_home=0
            half_away=0
            half2_home=0
            half2_away=0
            
            if has_overtime:
                home = row.pop('home_40_1')
                away = row.pop('away_40_1')
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=1,type=1,home=home,away=away)) 
                                      
            home = row.get('home_13_1')
            away = row.get('away_13_1')
            total_home += int(home)
            total_away += int(away)
            half_home += int(home)
            half_away += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=13,scoretype=1,home=home,away=away ,type=0) )
            home = row.get('home_14_1')
            away = row.get('away_14_1')
            total_home += int(home)
            total_away += int(away)
            half_home += int(home)
            half_away += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=14,scoretype=1,home=home,away=away ,type=0) )
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=6,scoretype=1,home=half_home,away=half_away ,type=0) )

            home = row.get('home_15_1')
            away = row.get('away_15_1')
            total_home += int(home)
            total_away += int(away)
            half2_home += int(home)
            half2_away += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=15,scoretype=1,home=home,away=away ,type=0) )
            home = row.get('home_16_1')
            away = row.get('away_16_1')
            total_home += int(home)
            total_away += int(away)
            half2_home += int(home)
            half2_away += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=16,scoretype=1,home=home,away=away ,type=0) )
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=7,scoretype=1,home=half2_home,away=half2_away ,type=0) )
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,home=total_home,away=total_away ,type=0) )

        if row['pk'] == -3:
            # NCAA 篮球手动输入比分 （只有上下半场,有加时赛）
            send_dc['IsSettleByScore']=True
            dc = {}
            has_overtime = row.pop('has_overtime',False)
           
            TbPeriodscore.objects.filter(matchid=matchid,scoretype=1).delete()
            total_home = 0
            total_away = 0
            if has_overtime:
                home = row.pop('home_40_1')
                away = row.pop('away_40_1')
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=1,type=1,home=home,away=away)) 
                                
            home = row.get('home_6_1')
            away = row.get('away_6_1')
            total_home += int(home)
            total_away += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=6,scoretype=1,home=home,away=away ,type=0) )
            home = row.get('home_7_1')
            away = row.get('away_7_1')
            total_home += int(home)
            total_away += int(away)
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=7,scoretype=1,home=home,away=away ,type=0) )
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,home=total_home,away=total_away ,type=0) )

    TbPeriodscore.objects.bulk_create(batch_create)
    if send_dc.get('IsSettleByScore'):
        home_score =0
        away_score =0
        for inst in batch_create:
            if inst.scoretype==1 and inst.statuscode in [6,7,40,50]:
                home_score += int(inst.home)
                away_score += int(inst.away)
            
        match = TbMatch.objects.get(matchid=matchid)
        match.score = '%s:%s'%(home_score,away_score)
        match.marketstatus=3
        match.statuscode = 100
        match.terminator ='manual'
        match.save()
        dc={
            'MatchID':match.matchid, 
            'Score':match.score,
            'MarketStatus':match.marketstatus,
            'StatusCode':match.statuscode,
            'Terminator':match.terminator
        }
        updateMatchMongo(dc)
        
    notifyManulOutcome(json.dumps(send_dc))

    
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
