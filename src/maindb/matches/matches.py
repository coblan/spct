# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable, TablePage, page_dc, ModelFields, model_dc, RowFilter, RowSort, \
    RowSearch, SelectSearch
from ..models import TbMatches, TbOdds, TbMatchesoddsswitch, TbOddstypegroup
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from helpers.director.base_data import director
from django.utils.timezone import datetime
import time
import requests
from maindb.mongoInstance import updateMatchMongo
from maindb.rabbitmq_instance import closeHandicap
import json
from ..redisInstance import redisInst


class MatchsPage(TablePage):
    template = 'jb_admin/table.html'
    extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]

    def get_label(self, prefer=None):
        return '比赛信息'

    class tableCls(ModelTable):
        model = TbMatches
        exclude = []
        fields_sort = ['matchid', 'tournamentzh', 'team1zh', 'team2zh', 'matchdate', 'period1score', 'matchscore',
                       'winner', 'statuscode',
                       'isrecommend', 'livebet', 'ishidden','closelivebet','marketstatus']
        pop_edit_field = 'matchid'

        class filters(RowFilter):
            range_fields = ['matchdate']
            names = ['isrecommend', 'livebet', 'statuscode', 'tournamentid']
            
            def dict_head(self, head): 
                if head['name'] == 'tournamentid':
                    head['editor'] = 'com-filter-search-select'
                    head['placeholder'] = '请选择联赛'
                    head['style'] = 'width:200px;'
                    head['order'] = True
                return head

        class search(SelectSearch):
            names = ['matchid', 'team1zh', 'team2zh']
            

        class sort(RowSort):
            names = ['matchdate']

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['extra_table_logic'] = 'match_logic'
            ls = [
                {'name': 'special_bet_value',
                 'label': '盘口',
                 'com': 'com-tab-special-bet-value',
                 'ops': [
                     {'fun': 'save', 'label': '保存', 'editor': 'com-op-btn', 'icon': 'fa-save', },
                     {'fun': 'refresh', 'label': '刷新', 'editor': 'com-op-btn', 'icon': 'fa-refresh', }
                 ]
                 }
            ]
            ctx['tabs'] = ls
            return ctx

        def get_operation(self):
            ops = [
                # {'name':'save_changed_rows','editor':'com-op-a','label':'保存','hide':'!changed'},

                # {'fun':'close_match','editor':'com-op-a','label':'结束比赛'},
                {'fun': 'manual_end_money',
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
                     'ops': [{"fun": 'produce_match_outcome', 'label': '保存', 'editor': 'com-field-op-btn'}, ],
                     'extra_mixins': ['produce_match_outcome'],
                     'fieldsPanel': 'produceMatchOutcomePanel',
                 }
                 },
                # {'fun':'jie_suan_pai_cai','editor':'com-op-a','label':'结算派彩'},
                {'fun': 'recommendate', 'editor': 'com-op-btn', 'label': '推介'},
                {'fun': 'un_recommendate', 'editor': 'com-op-btn', 'label': '取消推介'},

                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '滚球', 'field': 'closelivebet',
                 'value': 0 },
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '取消滚球', 'field': 'closelivebet', 'value': 1 },


                # {'fun': 'livebet', 'editor': 'com-op-btn', 'label': '滚球'},
                # {'fun': 'un_livebet', 'editor': 'com-op-btn', 'label': '取消滚球'},

                {'fun': 'show_match', 'editor': 'com-op-btn', 'label': '开启'},
                {'fun': 'hide_match', 'editor': 'com-op-btn', 'label': '关闭'},

                {'fun': 'closeHandicap', 'editor': 'com-op-btn', 'label': '封盘'},
                # {'fun': 'change_maxsinglepayout', 'editor': 'com-op-btn','label':'maxsinglepayout'}

            ]
            return ops

        def dict_head(self, head):
            dc = {
                'matchid': 70,
                'matchdate': 120,
                'tournamentzh': 160,
                'team1zh': 120,
                'team2zh': 120,
                'matchscore': 60,
                'winner': 60,
                'statuscode': 60,
                'roundinfo': 60,
                'isrecommend': 50,
                'livebet': 80,
                'ishidden':50,
                'categoryid': 80,
                'currentperiodstart': 150,
                'maxsinglepayout': 120,
                'marketstatus': 100,
                'closelivebet':70
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'matchdate':
                head['editor'] = 'com-table-label-shower'
            if head['name']=='closelivebet':
                head['editor']='com-table-bool-shower'
            # if head['name'] == 'matchid':
            # head['editor'] = 'com-table-switch-to-tab'
            # head['tab_name']='special_bet_value'

            return head

        def dict_row(self, inst):
            return {
                '_matchid_label': '%(home)s VS %(away)s' % {'home': inst.team1zh, 'away': inst.team2zh},
                '_matchdate_label': str(inst.matchdate)[: -3],
            }
        # def get_heads(self):
        # heads = [{'name':'operations',
        # 'label':'操作',
        # 'editor':'com-table-operations',
        # 'operations':[
        # {'name':'manul_end','label':'手动结算'},
        # {'name':'has_end_match','label':'已结束'} #100
        # ],
        # 'width':130,
        # }]
        # org_heads = ModelTable.get_heads(self)
        # heads.extend(org_heads)
        # return heads

        # def dict_row(self, inst):
        # dc={}
        # if inst.statuscode != 100:
        # dc['_op_has_end_match_hide']=True
        # if inst.statuscode == 100:
        # dc['_op_manul_end_hide']=True

        # return dc


class MatchForm(ModelFields):
    class Meta:
        model = TbMatches
        exclude = []

    field_sort = ['matchid', 'team1zh', 'team2zh']

    def dict_head(self, head):
        if head['name'] == 'matchid':
            head['readonly'] = True
        return head

    def save_form(self):
        super().save_form()
        inst = self.instance
        dc = {
            'MatchID': inst.matchid,
            'IsRecommend': inst.isrecommend,
            'IsHidden': inst.ishidden,
            'LiveBet': inst.livebet,
        }
        updateMatchMongo(dc)
        

        # if 'isrecommend' in self.changed_data:
        # redisInst.delete('App:Cache:index:matches')

    # def clean(self):
    # if 'statuscode' in self.changed_data:
    # self.instance.currentperiodstart = datetime.now()
    # self.instance.save()
    # return ModelFields.clean(self)


def get_special_bet_value(matchid):
    """
    获取封盘状态数据
    """
    try:
        TbMatchesoddsswitch.objects.get(matchid=matchid, status=1, oddstypegroup_id=0)
        match_opened = False
    except:
        match_opened = True

    oddstype = []
    specialbetvalue = []

    for odtp in TbOddstypegroup.objects.filter(enabled=1):
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
    for switch in TbMatchesoddsswitch.objects.filter(matchid=matchid, types=3):
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

    for oddsswitch in TbMatchesoddsswitch.objects.select_related('oddstypegroup').filter(matchid=matchid, status=1,
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


def save_special_bet_value_proc(matchid, match_opened, oddstype, specialbetvalue):
    """
    存储封盘操作
    """
    # TbMatchesoddsswitch.objects.filter(matchid=matchid,status=1).delete()
    batchOperationSwitch = []

    matchSwitch, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, types=1, defaults={'status': 0})

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
            playMethod, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, types=2,
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
            spSwitch, created = TbMatchesoddsswitch.objects.get_or_create(matchid=matchid, types=3,
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
    match = TbMatches.objects.get(matchid=matchid)
    msg = ['TbMatchesoddsswitch操作成功']

    # if match.livebet == 1:
    # url = 'http://192.168.40.103:9001/Match/Messages'
    # rt = requests.post(url,data={'EventName':'oddtypesChanged','MatchID':matchid})
    # msg.append('已经滚球，请求service封盘，返回结果为:%s'%rt.text)

    return {'status': 'success'}  # ,'msg':msg}


director.update({
    'match.table': MatchsPage.tableCls,
    'match.table.edit': MatchForm,

})

# model_dc[TbMatches]={'fields':MatchForm,'table':MatchsPage}

page_dc.update({
    'maindb.Matches': MatchsPage
})
