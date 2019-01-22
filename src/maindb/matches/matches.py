# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable, TablePage, page_dc, ModelFields, RowFilter, RowSort, \
    SelectSearch, Fields, director_view
from ..models import TbMatches, TbOdds, TbMatchesoddsswitch, TbOddstypegroup,TbTournament
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
from django.utils.timezone import datetime
from helpers.director.middleware.request_cache import get_request_cache
from django.utils import timezone

import logging
op_log = logging.getLogger('operation_log')


class MatchsPage(TablePage):
    template = 'jb_admin/table.html'
    #extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]

    def get_label(self, prefer=None):
        return '比赛信息'

    def get_context(self):
        ctx = super().get_context()
        #ctx['extra_table_logic'] = 'match_logic'
        ls = [
            {'name': 'special_bet_value',
             'label': '盘口',
             'com': 'com-tab-special-bet-value',
             'update_director': 'football_get_special_bet_value',
             'save_director': 'football_save_special_bet_value',
             'ops': [
                 {'fun': 'save', 'label': '保存', 'editor': 'com-op-btn', 'icon': 'fa-save', },
                 {'fun': 'refresh', 'label': '刷新', 'editor': 'com-op-btn', 'icon': 'fa-refresh', }, 
             ]
             }
        ]
        ctx['named_ctx'] = {
            'match_closelivebet_tabs': ls,
        }
        return ctx
    
    class tableCls(ModelTable):
        model = TbMatches
        exclude = []  # 'ishidden', 'closelivebet'
        fields_sort = ['matchid', 'tournamentzh', 'team1zh', 'team2zh', 'matchdate', 'period1score', 'matchscore',
                       'winner', 'statuscode', 'isrecommend', 'livebet', 'isshow', 'openlivebet', 'marketstatus']
        pop_edit_field = 'matchid'

        def getExtraHead(self):
            return [{'name': 'isshow', 'label': '显示'}, {'name': 'openlivebet', 'label': '开启走地'}]
        
        @classmethod
        def clean_search_args(cls, search_args):
            now = timezone.now()
            if search_args.get('_start_matchdate')==None and search_args.get('_end_matchdate')==None:
                search_args['_start_matchdate']=now.strftime("%Y-%m-%d 00:00:00")
                search_args['_end_matchdate']=now.strftime("%Y-%m-%d 23:59:59")
            return search_args
                
        
        def inn_filter(self, query):
            return query.extra(
                where=["TB_SportTypes.source= TB_Matches.source","TB_SportTypes.SportID=0"],
                tables=['TB_SportTypes']
            )
        
        class filters(RowFilter):
            range_fields = ['matchdate']
            names = ['isrecommend', 'livebet','statuscode','tournamentid']
            fields_sort=['isrecommend', 'livebet', 'statuscode','tournamentid']
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
                #if head['name']=='source':
                    #head['event_slots']=[
                             #{'event':'input','express':'scope.ts.$emit("data-source.changed",scope.event)'},
                        #]
                if head['name'] == 'tournamentid':
                    #head['editor'] = 'com-filter-search-select'
                    head['editor'] = 'com-filter-single-select2'
                    head['placeholder'] = '请选择联赛'
                    head['style'] = 'width:200px;'
                    head['options']=[
                        {'value':x.tournamentid,'label':str(x)} for x in TbTournament.objects.extra(
                            where=["TB_SportTypes.source= TB_Tournament.source","TB_SportTypes.SportID=0"],
                            tables=['TB_SportTypes'])
                    ]
                    #head['director_name']='get_football_league_options'
                    #head['event_slots']=[
                        #{'par_event':'data-source.changed','express':'rt=scope.vc.clear_value()'},
                        #{'par_event':'data-source.changed','express':'rt=scope.vc.get_options({post_data:{source:scope.event} })'},
                        #]
                    #head['order'] = False
                    #head['options']=[{'label':x.get('tournamentname'),'value':x.get('tournamentid')} for x in TbTournament.objects.values('tournamentname','tournamentid').order_by('tournamentname')] 
                         
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

        def get_context(self):
            ctx = ModelTable.get_context(self)
            #ctx['extra_table_logic'] = 'match_logic'
            ls = [
                {'name': 'special_bet_value',
                 'label': '盘口',
                 'com': 'com-tab-special-bet-value',
                 'ops': [
                     {'fun': 'save', 'label': '保存', 'editor': 'com-op-btn', 'icon': 'fa-save', },
                     {'fun': 'refresh', 'label': '刷新', 'editor': 'com-op-btn', 'icon': 'fa-refresh', }, 
                 ]
                 }
            ]
            ctx['named_ctx'] = {
                'match_closelivebet_tabs': ls,
            }
            return ctx


        def get_operation(self):
            points_form =  FootBallPoints(crt_user= self.crt_user)
            corner_form = NumberOfCorner(crt_user= self.crt_user)
            
            PeriodTypeForm_form =  PeriodTypeForm(crt_user= self.crt_user)
            
            #spoutcome_form =  SpOutcome(crt_user= self.crt_user)
            ops = [
                #{'fun': 'express',
                 #'express': "rt=manual_end_money(scope.ts,scope.kws)",
                 #'editor': 'com-op-btn',
                 #'label': '手动结算',
                 #'row_match': 'one_row',
                 ## 'disabled':'!only_one_selected',
                 #'fields_ctx': {
                     #'heads': [{'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
                               #{'name': 'home_score', 'label': '主队分数', 'editor': 'linetext'},
                               #{'name': 'home_half_score', 'label': '主队半场得分', 'editor': 'linetext'},
                               #{'name': 'home_corner', 'label': '主队角球', 'editor': 'linetext'},
                               #{'name': 'away_score', 'label': '客队分数', 'editor': 'linetext'},
                               #{'name': 'away_half_score', 'label': '客队半场得分', 'editor': 'linetext'},
                               #{'name': 'away_corner', 'label': '客队角球', 'editor': 'linetext'},
                               #],
                     
                    #'ops': [{"fun": 'produce_match_outcome', 'label': '保存', 'editor': 'com-field-op-btn', }, ],
                    #'produce_match_outcome_director': 'football_produce_match_outcome',

                 #}, 
                 #'visible': self.permit.can_edit(),
                 #},
                 
                 
                  {'fun': 'pop_panel',
                 'editor': 'com-op-btn',
                 #'panel':  'com-panel-fields', #'com-form-produceMatchOutcomePanel',
                 'panel_express': 'rt=manul_outcome_panel_express_parse(scope.kws.panel_map,scope.kws.play_type,scope.ts.selected[0].specialcategoryid)',
                 'label': '手动结算',
                 'row_match': 'one_row',
                 'ctx_express': 'rt=manul_outcome_panel_ctx(scope.ts.selected[0],scope.kws,scope.ts.selected[0].specialcategoryid)',
                 'play_type': {
                     'normal': [0], 
                     'corner': [2],
                     'race-to-first-number-of-points': [185],
                     },
                 'row_adapt': {
                     'normal': 'rt=scope.adaptor.parse_score(scope.row)',
                     'corner': 'rt=scope.adaptor.parse_score(scope.row)',
                     },
                 'panel_map': {
                     'normal': 'com-form-produceMatchOutcomePanel',
                     'corner': 'com-form-produceMatchOutcomePanel',
                     'race-to-first-number-of-points': 'com-panel-fields',
                     },
                 'ctx_dict': {
                     'normal': points_form.get_head_context(),
                     'corner': corner_form.get_head_context(),
                     #'normal': {
                        #'heads': [{'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
                                  #{'name': 'home_score', 'label': '主队分数', 'editor': 'linetext'},
                                  #{'name': 'home_half_score', 'label': '主队半场得分', 'editor': 'linetext'},
                                  #{'name': 'home_corner', 'label': '主队角球', 'editor': 'linetext'},
                                  #{'name': 'away_score', 'label': '客队分数', 'editor': 'linetext'},
                                  #{'name': 'away_half_score', 'label': '客队半场得分', 'editor': 'linetext'},
                                  #{'name': 'away_corner', 'label': '客队角球', 'editor': 'linetext'},
                                  #],
                        
                       #'ops': [{"fun": 'produce_match_outcome', 'label': '保存', 'editor': 'com-field-op-btn', }, ],
                       #'produce_match_outcome_director': 'football_produce_match_outcome',
                       #'after_express': 'rt=scope.ts.update_or_insert(scope.resp)',
                         #},
                     #'race-to-first-number-of-points': spoutcome_form.get_head_context(),
                     },
               
                 'visible': self.permit.can_edit(),
                 },
                 
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '推荐', 'confirm_msg': '确认推荐吗？',
                 'pre_set': 'rt={isrecommend:1}', 'row_match': 'many_row', 'match_express': 'scope.row.specialcategoryid <= 0 ',
                 'match_msg': '只能推荐常规比赛。',
                 'visible': 'isrecommend' in self.permit.changeable_fields(),},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '取消推荐', 'confirm_msg': '确认取消推荐吗？',
                 'pre_set': 'rt={isrecommend:0}', 'row_match': 'many_row', 'match_express': 'scope.row.specialcategoryid <= 0 ',
                 'match_msg': '只能取消推荐常规比赛。',
                 'visible': 'isrecommend' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '走地', 'confirm_msg': '确认打开走地吗？',
                 'field': 'closelivebet',
                 'value': 0,  'visible': 'closelivebet' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '取消走地', 'confirm_msg': '确认取消走地吗？',
                 'field': 'closelivebet',
                 'value': 1, 'visible': 'closelivebet' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '显示', 'confirm_msg': '确认显示比赛吗？',
                 'field': 'ishidden',
                 'value': 0, 'visible': 'ishidden' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '隐藏', 'confirm_msg': '确认隐藏比赛吗？',
                 'field': 'ishidden',
                 'value': 1, 'visible': 'ishidden' in self.permit.changeable_fields()},
                {'fun': 'express', 'editor': 'com-op-btn', 'label': '封盘', 'row_match': 'one_row',
                    'express': 'rt=scope.ts.switch_to_tab({tab_name:"special_bet_value",ctx_name:"match_closelivebet_tabs",par_row:scope.ts.selected[0]})',
                            'visible': self.permit.can_edit(),}, 
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
                'tournamentzh': 160,
                'team1zh': 120,
                'team2zh': 120,
                'matchscore': 80,
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
                'closelivebet': 70
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'matchdate':
                head['editor'] = 'com-table-label-shower'
            if head['name'] in ('closelivebet', 'openlivebet', 'isshow'):
                head['editor'] = 'com-table-bool-shower'
            # if head['name'] == 'matchid':
            # head['editor'] = 'com-table-switch-to-tab'
            # head['tab_name']='special_bet_value'

            return head

        def dict_row(self, inst):
            return {
                '_matchid_label': '%(home)s VS %(away)s' % {'home': inst.team1zh, 'away': inst.team2zh},
                '_matchdate_label': str(inst.matchdate)[: -3],
                'isshow': not bool(inst.ishidden),
                'openlivebet': not bool(inst.closelivebet)
            }
 
#@director_view('get_football_league_options')
#def get_football_league_options(source=0):
    #ls =[{'label':str(x) ,'value':x.tournamentid} for x in TbTournament.objects.filter(source=source)]
    #return ls
      
  
@director_view('football_quit_ticket')
def football_quit_ticket(rows, new_row): 
    return quit_ticket(rows, new_row, sportid = 0)

def quit_ticket(rows, new_row, sportid = 0): 
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
        model = TbMatches
        exclude = ['marketstatus', 'matchstatustype', 'specialcategoryid', 'mainleagueid', 
                   'mainhomeid', 'mainawayid', 'mainmatchid', 'maineventid', 'settlestatus', ]

    field_sort = ['matchid', 'team1zh', 'team2zh', ]

    def dict_head(self, head):
        if head['name'] == 'matchid':
            head['readonly'] = True
        return head

    def dict_row(self, inst):
        return {'isshow': not bool(inst.ishidden),
                'openlivebet': not bool(inst.closelivebet)
                }

    def save_form(self):
        super().save_form()
        msg = []
        if self.kw.get('meta_type') == 'manul_outcome':
            specialcategoryid = self.kw.get('specialcategoryid')
            ProcCls = self.proc_map.get(specialcategoryid)
            proc_obj = ProcCls(crt_user = self.crt_user)
            self.instance.settletime = datetime.now()
            rt_msg =  proc_obj.manul_outcome( self.kw, self.instance)
            msg.append(rt_msg)
            
            
        self.updateMongo()
        self.proc_redis()
        return {'msg': msg,}
    
    def updateMongo(self): 
        #inst = self.instance
        #dc = {
            #'MatchID': inst.matchid,
            #'IsRecommend': inst.isrecommend,
            #'IsHidden': inst.ishidden,
            #'CloseLiveBet': inst.closelivebet, 
            #'Team1ZH': inst.team1zh,
            #'Team2ZH': inst.team2zh,
        #}
        match =  self.instance
        dc = {
            'MatchID': match.matchid,
            'IsRecommend': match.isrecommend,
            'IsHidden': match.ishidden,
            'CloseLiveBet': match.closelivebet, 
            'Team1ZH': match.team1zh,
            'Team2ZH': match.team2zh,
            'StatusCode': match.statuscode,
            'Period1Score': match.period1score,
            'MatchScore': match.matchscore,
            'Winner': match.winner,
        }        
        updateMatchMongo(dc)
    
    def proc_redis(self): 
        if 'closelivebet' in self.changed_data:
            if self.instance.closelivebet == 0:
                redisInst.delete('Backend:Soccer:match:closelivebet:%(matchid)s' % {'matchid': self.instance.eventid})
            else:
                redisInst.set('Backend:Soccer:match:closelivebet:%(matchid)s' % {'matchid': self.instance.eventid}, 1,
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
    

        
        
@director_view('football_get_special_bet_value')
def football_get_special_bet_value(matchid): 
    return get_special_bet_value(matchid,sportid = 0 )

def get_special_bet_value(matchid, sportid = 0 , oddsModel = TbOdds):
    """
    获取封盘状态数据
    """
    try:
        TbMatchesoddsswitch.objects.get(matchid=matchid,sportid = sportid, status=1, oddstypegroup_id=0)
        match_opened = False
    except:
        match_opened = True

    oddstype = []
    specialbetvalue = []

    for odtp in TbOddstypegroup.objects.filter(enabled=1, sportid = sportid):
        oddstype.append(
            {
                'name': odtp.oddstypenamezh,
                # 'oddsid':odd.oddstype.oddsid,
                'oddstypegroup': odtp.oddstypegroup,
                # 'oddstypeid':odd.oddstype.oddstypeid,
                'opened': True,
                'sort': odtp.sort,
            }
        )

    for odd in oddsModel.objects.filter(match_id=matchid, status=1, oddstype__oddskind = 2, oddstype__status=1, oddstype__oddstypegroup__enabled=1) \
            .values('oddstype__oddstypegroup__oddstypenamezh', 'oddstype__oddstypegroup', 'specialbetvalue',
                    'handicapkey', 'oddstype__oddstypeid', 'oddstype__oddstypegroup__periodtype'):
        # print(odd.specialbetvalue)
        if odd['specialbetvalue'] != '':
            name = "%s %s" % (odd['oddstype__oddstypegroup__oddstypenamezh'], odd['specialbetvalue'])
            specialbetvalue.append(
                {
                    'name': name,
                    'oddstypegroup': odd['oddstype__oddstypegroup'],
                    'specialbetvalue': odd['specialbetvalue'],
                    'opened': True,
                    'Handicapkey': odd['handicapkey'],
                    'BetTypeId': odd['oddstype__oddstypeid'],
                    'PeriodType': odd['oddstype__oddstypegroup__periodtype'],
                }
            )

    # 把 以前操作过的 spvalue 加进来。因为这时通过tbOdds 已经查不到这些 sp value了
    for switch in TbMatchesoddsswitch.objects.filter(matchid=matchid, sportid = sportid,types=3, status = 1):
        name = "%s %s" % (switch.oddstypegroup.oddstypenamezh, switch.specialbetvalue)
        specialbetvalue.append(
            {
                'name': name,
                'oddstypegroup': switch.oddstypegroup_id,
                'specialbetvalue': switch.specialbetvalue,
                'opened': switch.status == 0,
                'Handicapkey': switch.handicapkey,
                'BetTypeId': switch.bettypeid,
                'PeriodType': switch.periodtype,
            }
        )

        # 去重
    tmp_dc = {}
    tmp_ls = []
    for i in specialbetvalue:
        name = "%s_%s" % (i['specialbetvalue'], i['oddstypegroup'])
        if name not in tmp_dc:
            tmp_dc[name] = ''
            tmp_ls.append(i)
    specialbetvalue = tmp_ls

    for oddsswitch in TbMatchesoddsswitch.objects.select_related('oddstypegroup').filter(matchid=matchid, status=1,sportid = sportid,
                                                                                         oddstypegroup__enabled=1):
        # 1 封盘 比赛 这个 OddsTypeGroup =0 所以这里筛选条件里面没有它
        # if oddsswitch.types==1:
        # match_opened =False
        # 2 封盘 玩法
        if oddsswitch.types == 2:
            for i in oddstype:
                if i['oddstypegroup'] == oddsswitch.oddstypegroup_id:
                    i['opened'] = False
        # 3 封盘 值 specialbetvalue
        elif oddsswitch.types == 3:
            for i in specialbetvalue:
                if i['oddstypegroup'] == oddsswitch.oddstypegroup_id and i[
                    'specialbetvalue'] == oddsswitch.specialbetvalue:
                    i['opened'] = False

    return {
        'match_opened': match_opened,
        'oddstype': oddstype,
        'specialbetvalue': specialbetvalue,
    }

@director_view('football_save_special_bet_value')
def football_save_special_bet_value(matchid, match_opened, oddstype, specialbetvalue): 
    return save_special_bet_value_proc(matchid, match_opened, oddstype, specialbetvalue, sportid = 0)

def save_special_bet_value_proc(matchid, match_opened, oddstype, specialbetvalue, sportid = 0):
    """
    存储封盘操作
    """
    # TbMatchesoddsswitch.objects.filter(matchid=matchid,status=1).delete()
    log_msg = '封盘操作：'
    batchOperationSwitch = []

    matchSwitch, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, sportid = sportid, types=1, defaults={'status': 0})

    if not match_opened:
        if matchSwitch.status == 0:
            matchSwitch.status = 1
            matchSwitch.save()
            log_msg += '开启比赛%s;' % matchid
            batchOperationSwitch.append(matchSwitch)
        # obj, created = TbMatchesoddsswitch.objects.update_or_create(matchid=matchid,types=1, defaults = { 'status': 1})
    else:
        if matchSwitch.status == 1:
            matchSwitch.status = 0
            matchSwitch.save()
            log_msg += '关闭比赛%s;' % matchid
            batchOperationSwitch.append(matchSwitch)

        for odtp in oddstype:
            playMethod, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, sportid = sportid, types=2,
                                                                            oddstypegroup_id=odtp['oddstypegroup'],
                                                                            defaults={'status': 0})

            if not odtp['opened']:

                if playMethod.status == 0:
                    playMethod.status = 1
                    playMethod.save()
                    log_msg += '屏蔽玩法：%s' % odtp['oddstypegroup']
                    batchOperationSwitch.append(playMethod)
            else:
                if playMethod.status == 1:
                    playMethod.status = 0
                    playMethod.save()
                    log_msg += '开启玩法：%s' % odtp['oddstypegroup']
                    batchOperationSwitch.append(playMethod)

        for spbt in specialbetvalue:
            oddstypegroup = spbt['oddstypegroup']
            par_odd = None
            for i in oddstype:
                if oddstypegroup == i['oddstypegroup']:
                    par_odd = i
                    break
            spSwitch, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, sportid = sportid, types=3,
                                                                          oddstypegroup_id=par_odd['oddstypegroup'],
                                                                          bettypeid=spbt['BetTypeId'],
                                                                          periodtype=spbt['PeriodType'],
                                                                          handicapkey=spbt['Handicapkey'],
                                                                          specialbetvalue=spbt['specialbetvalue'],
                                                                          defaults={'status': 0})
            if par_odd['opened']:
                if not spbt['opened']:
                    if spSwitch.status == 0:
                        spSwitch.status = 1
                        spSwitch.save()
                        log_msg += '屏蔽盘口：%s' % spbt['specialbetvalue']
                        batchOperationSwitch.append(spSwitch)
                else:
                    if spSwitch.status == 1:
                        spSwitch.status = 0
                        spSwitch.save()
                        log_msg += '开启盘口：%s' % spbt['specialbetvalue']
                        batchOperationSwitch.append(spSwitch)
                        # TbMatchesoddsswitch.objects.create(matchid=matchid,types=3,status=1,
                        # oddstypegroup_id=par_odd['oddstypegroup'],
                        # specialbetvalue=spbt['specialbetvalue'])
    ls = []
    for switch in batchOperationSwitch:
        ls.append({
            'MatchID': switch.matchid,
            'SportID': sportid,
            'Types': switch.types,
            'OddsTypeGroup': switch.oddstypegroup_id,
            'SpecialBetValue': switch.specialbetvalue,
            'Status': switch.status,
            'BetTypeId': switch.bettypeid,
            'PeriodType': switch.periodtype,
            'Handicapkey': switch.handicapkey,
        })
    closeHandicap(json.dumps(ls))

    op_log.info(log_msg)
    
    # 请求service，关闭盘口
    #match = TbMatches.objects.get(matchid=matchid)
    #msg = ['TbMatchesoddsswitch操作成功']


    return {'status': 'success'}  # ,'msg':msg}


@director_view('football_produce_match_outcome')
def football_produce_match_outcome(row): 
    return produce_match_outcome(row, MatchModel = TbMatches, sportid = 0, half_end_code = 31, updateMongo= updateMatchMongo)

def produce_match_outcome(row, MatchModel , sportid, half_end_code = 31, updateMongo = updateMatchMongo):
    """
    手动结算
    """ 
    
    match = MatchModel.objects.get(matchid = row.get('matchid'))
    match.ishidden = True
    
    crt_settlestatus = 0 if not match.settlestatus else match.settlestatus
    settlestatus = crt_settlestatus
    if crt_settlestatus < 1 and row.get('home_half_score', '') != '' and row.get('away_half_score', '') != '':
        match.period1score = '%s:%s' % (row.get('home_half_score'), row.get('away_half_score'))
        match.statuscode = half_end_code
        settlestatus = 1
    if crt_settlestatus < 2 and row.get('home_score', '') != '' and row.get('away_score', '') != '':
        match.matchscore = '%s:%s' % (row.get('home_score'), row.get('away_score'))
        match.homescore = row.get('home_score')
        match.awayscore = row.get('away_score')   
        match.statuscode = 100
        settlestatus += 2
        if row.get('home_score') > row.get('away_score'):
            match.winner = 1
        elif row.get('home_score') < row.get('away_score'):
            match.winner = 2
        else:
            match.winner = 3
    
    settle_dict =  {
            1: '上半场',
            2: '全场',
            3: '半场&全场',
        }
    if crt_settlestatus < settlestatus:
        match.settlestatus = settlestatus
    else:
        
        raise UserWarning('%s已经结算,请不要重复结算!' % settle_dict.get(settlestatus))
        
    data = {
        'SportID': sportid, 
        'MatchID': row.get('matchid'),
        'PeriodType': row.get('PeriodType'),
        'OrderBack': False,
    }
    org_match = to_dict(match)
    match.save()
    
    url = urllib.parse.urljoin( settings.CENTER_SERVICE, '/Match/ManualResulting')
    rt = requests.post(url,json=data)
    rt_dc = json.loads( rt.text )
    if not rt_dc.get('Success'):
        for k in org_match:
            if not k.startswith('_'):
                setattr(match, k, org_match[k])
            match.save()
        op_log.info('手动结算足球比赛%(matchid)s的%(type)s，未成功,错误消息:%(msg)s' % {'matchid': match.matchid, 
                                                         'type': settle_dict.get(match.settlestatus),
                                                        'msg': rt_dc.get('Message',''),})
            
        raise UserWarning( rt_dc.get('Message', '手动结算后端发生问题'))
    
    rt_dc['row'] = to_dict(match)
    
    dc = {
        'MatchID': match.matchid,
        'IsRecommend': match.isrecommend,
        'IsHidden': match.ishidden,
        'CloseLiveBet': match.closelivebet, 
        'Team1ZH': match.team1zh,
        'Team2ZH': match.team2zh,
        'StatusCode': match.statuscode,
        'Period1Score': match.period1score,
        'MatchScore': match.matchscore,
        'Winner': match.winner,
    }
    updateMongo(dc)    
    
    op_log.info('手动结算足球比赛%(matchid)s的%(type)s，结算后比分为:上半场:%(period1score)s,全场:%(matchscore)s' % {'matchid': match.matchid, 
                                                     'type': settle_dict.get(match.settlestatus),
                                                     'period1score': match.period1score,
                                                     'matchscore': match.matchscore,})
    return rt_dc    





director.update({
    'match.table': MatchsPage.tableCls,
    'match.table.edit': MatchForm,
    #'PeriodTypeForm': PeriodTypeForm,
    

})

# model_dc[TbMatches]={'fields':MatchForm,'table':MatchsPage}

page_dc.update({
    'matches': MatchsPage
})
