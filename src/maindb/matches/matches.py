# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable, TablePage, page_dc, ModelFields, RowFilter, RowSort, \
    SelectSearch, Fields, director_view
from ..models import TbMatches, TbOdds, TbMatchesoddsswitch, TbOddstypegroup
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


class MatchsPage(TablePage):
    template = 'jb_admin/table.html'
    extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]

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

        class filters(RowFilter):
            range_fields = ['matchdate']
            names = ['isrecommend', 'livebet', 'statuscode', 'tournamentid']

            def dict_head(self, head):
                if head['name'] == 'tournamentid':
                    #head['editor'] = 'com-filter-search-select'
                    head['editor'] = 'com-filter-single-select2'
                    head['placeholder'] = '请选择联赛'
                    head['style'] = 'width:200px;'
                    head['order'] = True
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
            PeriodTypeForm_form =  PeriodTypeForm(crt_user= self.crt_user)
            ops = [
                {'fun': 'express',
                 'express': "rt=manual_end_money(scope.ts,scope.kws)",
                 'editor': 'com-op-btn',
                 'label': '手动结算',
                 # 'disabled':'!only_one_selected',
                 'fields_ctx': {
                     'heads': [{'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
                               {'name': 'home_score', 'label': '主队分数', 'editor': 'linetext'},
                               {'name': 'home_half_score', 'label': '主队半场得分', 'editor': 'linetext'},
                               {'name': 'home_corner', 'label': '主队角球', 'editor': 'linetext'},
                               {'name': 'away_score', 'label': '客队分数', 'editor': 'linetext'},
                               {'name': 'away_half_score', 'label': '客队半场得分', 'editor': 'linetext'},
                               {'name': 'away_corner', 'label': '客队角球', 'editor': 'linetext'},
                               ],
                     #'ops': [{"fun": 'produce_match_outcome', 'label': '保存', 'editor': 'com-field-op-btn'}, ],
                     
                  
                     #'extra_mixins': ['produce_match_outcome'],
                     #'fieldsPanel': 'produceMatchOutcomePanel',
                    'option': {
                           'ops': [{"fun": 'produce_match_outcome', 'label': '保存', 'editor': 'com-field-op-btn', }, ],
                           'produce_match_outcome_director': 'football_produce_match_outcome',
                        },
                     'form': 'com-form-produceMatchOutcomePanel',
                     
                 }, 
                 'visible': self.permit.can_edit(),
                 },
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '推荐', 'confirm_msg': '确认推荐吗？',
                 'field': 'isrecommend',
                 'value': 1, 'visible': 'isrecommend' in self.permit.changeable_fields(),},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '取消推荐', 'confirm_msg': '确认取消推荐吗？',
                 'field': 'isrecommend',
                 'value': 0,  'visible': 'isrecommend' in self.permit.changeable_fields()},
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
                  'director_name': 'quit_ticket',
                  'label': '退单', 'confirm_msg': '确认要退单吗？', 'row_match': 'one_row',
                  'pre_set': 'rt={PeriodType:2}',
                  #'after_save': 'rt=cfg.showMsg(scope.new_row.Message)',
                 'fields_ctx': PeriodTypeForm_form.get_head_context(),
                 'visible': 'ishidden' in self.permit.changeable_fields()},
                #closeHandicap:function(){
                    #if(self.selected.length !=1){
                        #cfg.showMsg('请选择一条记录')
                        #return
                    #}
                    #self.op_funs.switch_to_tab({tab_name:'special_bet_value',row:self.selected[0]})
                #},                      
                #{'fun': 'closeHandicap', 'editor': 'com-op-btn', 'label': '封盘',  'visible': self.permit.can_edit(),}
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
        
        @staticmethod
        @director_view('quit_ticket')
        def quit_ticket(rows, new_row): 
            PeriodType = new_row.get('PeriodType')
            row = rows[0]
            url = urllib.parse.urljoin( settings.CENTER_SERVICE, '/Match/ManualResulting')
            data ={
                'MatchID':row.get('matchid'),
                'SportID': 0, 
                'OrderBack': True,
                'PeriodType': PeriodType,  # 1上半场 0全场 2 上半场+ 全场
            }    
            
            rt = requests.post(url,data=data)
            #print(rt.text)
            dc = json.loads( rt.text )  
            return {'msg': dc.get('Message'),}


class MatchForm(ModelFields):
    class Meta:
        model = TbMatches
        exclude = ['marketstatus']

    field_sort = ['matchid', 'team1zh', 'team2zh']

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
        inst = self.instance
        dc = {
            'MatchID': inst.matchid,
            'IsRecommend': inst.isrecommend,
            'IsHidden': inst.ishidden,
            'CloseLiveBet': inst.closelivebet, 
            'Team1ZH': inst.team1zh,
            'Team2ZH': inst.team2zh,
            
        }
        updateMatchMongo(dc)

        if 'closelivebet' in self.changed_data:
            if self.instance.closelivebet == 0:
                redisInst.delete('Backend:match:closelivebet:%(matchid)s' % {'matchid': self.instance.eventid})
            else:
                redisInst.set('Backend:match:closelivebet:%(matchid)s' % {'matchid': self.instance.eventid}, 1,
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

def get_special_bet_value(matchid, sportid = 0 ):
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

    for odd in TbOdds.objects.filter(match_id=matchid, status=1, oddstype__status=1, oddstype__oddstypegroup__enabled=1) \
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
    batchOperationSwitch = []

    matchSwitch, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, sportid = sportid, types=1, defaults={'status': 0})

    if not match_opened:
        if matchSwitch.status == 0:
            matchSwitch.status = 1
            matchSwitch.save()
            batchOperationSwitch.append(matchSwitch)
        # obj, created = TbMatchesoddsswitch.objects.update_or_create(matchid=matchid,types=1, defaults = { 'status': 1})
    else:
        if matchSwitch.status == 1:
            matchSwitch.status = 0
            matchSwitch.save()
            batchOperationSwitch.append(matchSwitch)

        for odtp in oddstype:
            playMethod, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, sportid = sportid, types=2,
                                                                            oddstypegroup_id=odtp['oddstypegroup'],
                                                                            defaults={'status': 0})

            if not odtp['opened']:

                if playMethod.status == 0:
                    playMethod.status = 1
                    playMethod.save()
                    batchOperationSwitch.append(playMethod)
            else:
                if playMethod.status == 1:
                    playMethod.status = 0
                    playMethod.save()
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
                        batchOperationSwitch.append(spSwitch)
                else:
                    if spSwitch.status == 1:
                        spSwitch.status = 0
                        spSwitch.save()
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

    # 请求service，关闭盘口
    #match = TbMatches.objects.get(matchid=matchid)
    #msg = ['TbMatchesoddsswitch操作成功']


    return {'status': 'success'}  # ,'msg':msg}


@director_view('football_produce_match_outcome')
def football_produce_match_outcome(row): 
    return produce_match_outcome(row, MatchModel = TbMatches, sportid = 0)

def produce_match_outcome(row, MatchModel , sportid):
    """
    手动结算
    """
    #url = 'http://192.168.40.103:9001/Match/ManualResulting'
    url = urllib.parse.urljoin( settings.CENTER_SERVICE, '/Match/ManualResulting')
    
    #data ={
        #'MatchID':row.get('matchid'),
        #'Team1Score':row.get('home_score', 0),
        #'Team2Score':row.get('away_score', 0),
        #'Team1HalfScore':row.get('home_half_score', 0),
        #'Team2HalfScore':row.get('away_half_score', 0),        
        #'Team1Corner':row.get('home_corner', 0),
        #'Team2Corner':row.get('away_corner', 0),
        #'Terminator': 'adminSys',
        #'PeriodType': row.get('PeriodType'),  # 1上半场 0全场 2 上半场+ 全场
        
    #}    
    
    match = MatchModel.objects.get(matchid = row.get('matchid'))
    
    if row.get('home_half_score', '') != '' and row.get('away_half_score', '') != '':
        match.period1score = '%s:%s' % (row.get('home_half_score'), row.get('away_half_score'))
        match.statuscode = 31
    if row.get('home_score', '') != '' and row.get('away_score', '') != '':
        match.matchscore = '%s:%s' % (row.get('home_score'), row.get('away_score'))
        match.homescore = row.get('home_score')
        match.awayscore = row.get('away_score')   
        match.statuscode = 100
    #match.ishidden = True
    match.save()
    
    dc = {
        'MatchID': match.matchid,
        'IsRecommend': match.isrecommend,
        'IsHidden': match.ishidden,
        'CloseLiveBet': match.closelivebet, 
        'Team1ZH': match.team1zh,
        'Team2ZH': match.team2zh,
        'StatusCode': match.statuscode,
    }
    updateMatchMongo(dc)    
        
    data = {
        'SportID': sportid, 
        'MatchID': row.get('matchid'),
        'PeriodType': row.get('PeriodType'),
        'OrderBack': False,
    }
    
    rt = requests.post(url,json=data)
    #print(rt.text)
    dc = json.loads( rt.text )
    dc['row'] = to_dict(match)
    return dc    


director.update({
    'match.table': MatchsPage.tableCls,
    'match.table.edit': MatchForm,
    'PeriodTypeForm': PeriodTypeForm,

})

# model_dc[TbMatches]={'fields':MatchForm,'table':MatchsPage}

page_dc.update({
    'matches': MatchsPage
})
