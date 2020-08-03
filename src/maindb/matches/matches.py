# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable, TablePage, page_dc, ModelFields, RowFilter, RowSort, \
     SelectSearch, Fields, director_view,director_element,director_save_row
from helpers.func.collection.container import evalue_container
from helpers.director.access.permit import has_permit,can_touch,can_write
from ..models import  TbOdds, TbMatchesoddsswitch, TbOddstypegroup,TbTournament,\
     TbMatch,TbPeriodscore,TbMarkets,TbMarkethcpswitch,TbLivefeed,TbSporttypes,TbManualsettlemsg,TbAccount
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from helpers.director.base_data import director
from maindb.mongoInstance import updateMatchMongo
from maindb.rabbitmq_instance import closeHandicap
import json
from ..redisInstance import redisInst,redisInst0
from django.db.models import Q,F
import urllib
import requests
from django.conf import settings
from helpers.director.model_func.dictfy import to_dict
import functools
#from .match_outcome_forms import FootBallPoints, NumberOfCorner
from helpers.director.middleware.request_cache import get_request_cache
from django.db import connections
import datetime
from maindb.rabbitmq_instance import notifyManulOutcome
from . manul_outcome import outcome_header
from django.db.models import Count,Q,QuerySet
from maindb.rabbitmq_instance import notifyMatchRecommond,notifyAdjustOddsBase
from django.utils import timezone
from helpers.director.dapi import save_rows
from maindb.mongoInstance import mydb

import logging
op_log = logging.getLogger('operation_log')


def get_match_tab(crt_user):
    match_form = MatchForm(crt_user=crt_user)
    match_tabs=[
        {'name':'match_base_info',
         'label':'基本信息',
         'com':'com-tab-fields-v1',
         'init_express':'cfg.show_load(); ex.director_call("%s",{matchid:scope.vc.par_row.matchid}).then(resp=>{cfg.hide_load();ex.vueAssign(scope.vc.row,resp.row)})'%match_form.get_director_name(),
         'fields_ctx':match_form.get_head_context(),
         'visible': can_touch(TbMatch, crt_user) ,
         },
        {
            'name':'peroidscore',
            'label':'比分',
            'com':'com-tab-table',
            'pre_set':'rt={matchid:scope.par_row.matchid}',
            'table_ctx': PeriodScoreTab(crt_user = crt_user).get_head_context(),
            'visible': can_touch(TbPeriodscore, crt_user), 
            },
        {
            'name':'danger_football',
            'label':'危险球',
            'com':'com-tab-table',
            'par_field': 'matchid',
            'table_ctx': TbLivescoutTable(crt_user= crt_user).get_head_context(),
            'visible': can_write(TbLivefeed,  crt_user), 
            'show':'scope.par_row.sportid==1'
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
             ],
         'visible': has_permit( crt_user, 'manual_specialbetvalue'), 
         },
        {
            'name':'manul_outcome',
            'label':'手动结算',
            'com':'com-tab-table',
            'pre_set': 'rt={matchid:scope.par_row.matchid}',
            'table_ctx': {
                'init_express':'scope.ps.search()',
                **OutcomeTab(crt_user= crt_user).get_head_context()
                },
            'visible': has_permit( crt_user, 'manual_outcome'), 
            },     
    ]
    return match_tabs

class MatchsPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self, prefer=None):
        return '比赛信息'

    def get_context(self):
        ctx = super().get_context()

        ctx['named_ctx'] = {
            'match_tabs':evalue_container( get_match_tab(self.crt_user) ),
        }
        return ctx

    class tableCls(ModelTable):
        sportid=1
        model = TbMatch
        exclude = []  # 'ishidden', 'iscloseliveodds'
        #fields=['source','sportid','matchid', 'tournamentid', 'team1zh', 'team2zh', 'matchdate', 'score','num_stake',
                       #'winner', 'statuscode', 'isrecommend', 'hasliveodds', 'isshow', 'marketstatus','weight','ticketdelay','isdangerous',
                       #'eventid',]
        fields_sort = ['source','sportid','matchid', 'tournamentid', 'team1zh', 'team2zh', 'matchdate', 'score','num_stake',
                       'winner', 'statuscode', 'isrecommend', 'hasliveodds', 'isshow', 'marketstatus','weight','ticketdelay','isdangerous',
                       'eventid','manual_settle_need_audit'] #'oddsadjustment','oddsadjustmax','baseticketeamout',

        def getExtraHead(self):
            return [{'name': 'isshow', 'label': '显示'},
                    {'name':'num_stake','label':'未结算订单',
                     'editor':'com-table-rich-span',
                     'action':'scope.head.tab_ctx.par_row = scope.row;scope.ps.switch_to_tab(scope.head.tab_ctx)',
                     'tab_ctx':{
                         'tab_name':'manul_outcome',
                         'ctx_name':'match_tabs',
                     },
                     'inn_editor':'com-table-span',
                     'cell_class':'scope.row.num_stake !="0/0"?"mywarning clickable":"clickable"',
                     'css':'.mywarning{background-color:#ff410e;color:white}'
                     },
                    {'name':'manual_settle_need_audit','label':'需要审核',
                     'editor':'com-table-mapper','options':[
                         {'value':0,'label':'编辑中'},
                         {'value':1,'label':'审核中'},
                     ]
                     }]

        @classmethod
        def clean_search_args(cls, search_args):
            now = datetime.datetime.now()
            if search_args.get('_first','1') =='1' :
                search_args['_first'] = '0'
                #search_args.get('_start_matchdate')==None and search_args.get('_end_matchdate')==None:
                search_args['_start_matchdate']=now.strftime("%Y-%m-%d 00:00:00")
                search_args['_end_matchdate']=now.strftime("%Y-%m-%d 23:59:59")       
            return search_args


        def inn_filter(self, query):
            query = query.using('Sports_nolock').extra(select={
                '_tournamentid_label':'SELECT TB_Tournament.tournamentnamezh',
                '_sportid_label':'SELECT TB_SportTypes.SportNameZH',
                #'num_stake':'''SELECT concat( COUNT( CASE WHEN TB_TicketMaster.ParlayRule =11 then 1 ELSE null END),'/', COUNT( CASE WHEN TB_TicketMaster.ParlayRule !=11 then 1 ELSE null END)) FROM TB_TicketMaster, TB_TicketStake ,TB_Account
                #WHERE TB_TicketStake.MatchID = TB_Match.MatchID AND 
                #TB_TicketMaster.TicketID=TB_TicketStake.TicketID  AND 
                #TB_TicketMaster.Status =1 AND 
                #TB_TicketMaster.AccountID = TB_Account.AccountID AND TB_Account.AccountType=0'''
                'num_stake':'''SELECT  cast(  COUNT (1) AS varchar ) +'/' +cast(COUNT ( CASE WHEN TB_TicketMaster.ParlayRule != 11 THEN 1 ELSE NULL END ) AS varchar) 
	FROM TB_TicketMaster,TB_TicketStake,TB_Account 
        WHERE
	TB_TicketStake.MatchID = TB_Match.MatchID 
	AND TB_TicketMaster.TicketID= TB_TicketStake.TicketID 
	AND TB_TicketMaster.Status = 1 
	AND TB_TicketMaster.AccountID = TB_Account.AccountID 
	AND TB_Account.AccountType= 0 ''',
                #'num_stake_total':'''SELECT  COUNT( 1) FROM TB_TicketMaster, TB_TicketStake ,TB_Account
                #WHERE TB_TicketStake.MatchID = TB_Match.MatchID AND 
                #TB_TicketMaster.TicketID=TB_TicketStake.TicketID  AND 
                #TB_TicketMaster.Status =1 AND 
                #TB_TicketMaster.AccountID = TB_Account.AccountID AND TB_Account.AccountType=0''',
                #'num_stake_parlay':'''SELECT  COUNT( CASE WHEN TB_TicketMaster.ParlayRule !=11 then 1 ELSE null END) FROM TB_TicketMaster, TB_TicketStake ,TB_Account
                #WHERE TB_TicketStake.MatchID = TB_Match.MatchID AND 
                #TB_TicketMaster.TicketID=TB_TicketStake.TicketID  AND 
                #TB_TicketMaster.Status =1 AND 
                #TB_TicketMaster.AccountID = TB_Account.AccountID AND TB_Account.AccountType=0''',
                'manual_settle_need_audit':'SELECT status FROM TB_ManualSettleMsg WHERE TB_Match.MatchID=TB_ManualSettleMsg.MatchID',
                
                },
                where=['TB_Tournament.TournamentID=TB_Match.TournamentID ','TB_SportTypes.SportID=TB_Match.SportID','TB_Tournament.IsSubscribe=1',],
                tables =['TB_Tournament','TB_SportTypes',]
                )

            return query


        class filters(RowFilter):
            range_fields = ['matchdate']
            names = ['source','sportid','isrecommend', 'marketstatus','statuscode','hasliveodds','tournamentid',]
            fields_sort=['source','sportid','isrecommend', 'has_unchecked','marketstatus', 'statuscode','hasliveodds','manual_settle_need_audit','tournamentid','matchdate']

            def getExtraHead(self):
                return [
                    {'name':'has_unchecked','label':'有未结算订单','editor':'com-filter-check'},
                    {'name':'specialcategoryid','editor':'com-filter-select','placeholder':'类型',
                     'options':[
                         {'value':0,'label':'常规'},
                        {'value':1,'label':'特殊'}
                        ],
                     },
                    {'name':'manual_settle_need_audit','label':'手动结算状态','editor':'com-filter-select',
                     'options':[
                         {'value':0,'label':'编辑中'},
                         {'value':1,'label':'审核中'},
                     ]}
                ]

            def clean_query(self, query):
                #if self.kw.get('specialcategoryid')==0:
                    #return query.filter(specialcategoryid__lte=0)
                #elif self.kw.get('specialcategoryid')==1:
                    #return query.filter(specialcategoryid__gt=0)
                if self.kw.get('has_unchecked'):
    
                    query =query.filter(tbticketstake__ticket_master__status=1,tbticketstake__ticket_master__accountid__accounttype=0)
                if self.kw.get('manual_settle_need_audit') == 1:
                    query = query.extra(where=['TB_ManualSettleMsg.status=1','TB_ManualSettleMsg.Matchid=TB_Match.Matchid'],
                                       tables=['TB_ManualSettleMsg'])
                elif self.kw.get('manual_settle_need_audit') == 0:
                    query = query.extra(where=['TB_ManualSettleMsg.status=0','TB_ManualSettleMsg.Matchid=TB_Match.Matchid'],
                                       tables=['TB_ManualSettleMsg'])
                    #return query.annotate(need_audit =F('manual_settle_need_audit')).filter(need_audit=1)
                
                return query

            def dict_head(self, head):
                if head['name']=='statuscode':
                    head['options']=list( filter(lambda x:x['value'] in [0,6,7,31,32,34,40,50,100,110,120],head['options']) )

                if head['name'] == 'tournamentid':
                    #head['editor'] = 'com-filter-search-select'
                    head['editor'] = 'com-filter-single-select2'
                    head['placeholder'] = '请选择联赛'
                    head['style'] = 'width:200px;'
                    head['options']=[
                        {'value':x.tournamentid,'label':str(x)} for x in TbTournament.objects.all()
                    ]
                if head['name'] == 'sportid':
                    head['options'] =[
                        {'value':x.sportid,'label':x.sportnamezh } for x in TbSporttypes.objects.filter(enabled = True)
                    ]
                return head

        class search(SelectSearch):
            names = ['teamname','eventid']
            exact_names = ['matchid','eventid']
            field_sort=['matchid','teamname','eventid']
            def get_option(self, name):
                if name == 'teamname':
                    return {'value': 'teamname', 'label': '球队名称', }
                elif name =='eventid':
                    return {'value':'eventid','label':'eventid'}
                else:
                    return super().get_option(name)

            def get_express(self, q_str):
                if self.qf == 'teamname':
                    return Q(team1zh__icontains=q_str) | Q(team2zh__icontains=q_str) 
                else:
                    return super().get_express(q_str)

        class sort(RowSort):
            names = ['matchdate','ticketdelay']

        def get_operation(self):
            ops = [
            
                #{'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '推荐', 'confirm_msg': '确认推荐吗？',
                 #'pre_set': 'rt={isrecommend:true}', 'row_match': 'many_row', 
                 #'after_save':' ex.director_call("notify_match_recommend",{rows:scope.rows})',
                 #'visible': 'isrecommend' in self.permit.changeable_fields(),},
                {'action':''' ex.each(scope.ps.selected,row=>{row.meta_change_fields="isrecommend";row.isrecommend=true});
                cfg.show_load();
                ex.director_call("batch_recommand",{rows:scope.ps.selected})
                .then((resp)=>{
                    cfg.hide_load();
                    ex.each(scope.ps.selected,row=>{delete row.meta_change_fields});
                    scope.ps.update_rows(resp); ex.director_call("notify_match_recommend",{rows:resp});
                    scope.ps.selected =[]
                    })''' ,
                 'editor':'com-op-btn','label':'推荐','confirm_msg': '确认推荐吗？',
                  'row_match': 'many_row',
                  'visible': 'isrecommend' in self.permit.changeable_fields()
                  },
                 #{'fun':'director_call','editor':'com-op-btn','label':'推荐','confirm_msg': '确认推荐吗？',
                  #'pre_set': 'rt={isrecommend:true}', 
                  #'director_name':'batch_recommand',
                  #'row_match': 'many_row',
                  #'after_save':'scope.ps.update_rows(scope.resp); ex.director_call("notify_match_recommend",{rows:scope.resp})',
                  #'visible': 'isrecommend' in self.permit.changeable_fields()
                  #},
                 
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '取消推荐', 'confirm_msg': '确认取消推荐吗？',
                 'pre_set': 'rt={isrecommend:false}', 'row_match': 'many_row',
                 'after_save':'ex.director_call("notify_match_recommend",{rows:scope.rows})',
                 'visible': 'isrecommend' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '走地', 'confirm_msg': '确认打开走地吗？',
                 'field':'hasliveodds', # 'iscloseliveodds', 
                 'value': True,  'visible': 'hasliveodds' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '取消走地', 'confirm_msg': '确认取消走地吗？',
                 'field': 'hasliveodds',
                 'value': False, 'visible': 'hasliveodds' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 
                 'editor': 'com-op-btn', 
                 'label': '显示', 
                 'confirm_msg': '确认显示比赛吗？',
                 'pre_set':'rt={meta_change_fields:"ishidden",ishidden:0}',
                 'visible': 'ishidden' in self.permit.changeable_fields()},
                {'fun': 'selected_set_and_save', 
                 'editor': 'com-op-btn', 
                 'label': '隐藏', 
                 'confirm_msg': '确认隐藏比赛吗？',
                 'pre_set':'rt={meta_change_fields:"ishidden",ishidden:1}',
                  'visible': 'ishidden' in self.permit.changeable_fields()},
                #{'fun': 'express', 'editor': 'com-op-btn', 'label': '封盘', 'row_match': 'one_row',
                #'express': 'rt=scope.ps.switch_to_tab({tab_name:"special_bet_value",ctx_name:"match_iscloseliveodds_tabs",par_row:scope.ps.selected[0]})',
                    #'visible': self.permit.can_edit(),}, 
                {'fun': 'director_call', 'editor': 'com-op-btn', 
                  'director_name': 'match.quit_ticket',
                  'label': '退单', 'confirm_msg': '确认要退单吗？', 'row_match': 'one_row',
                  #'pre_set': 'rt={PeriodType:2}',
                  #'after_save': 'rt=cfg.showMsg(scope.new_row.Message)',
                  #'fields_ctx': PeriodTypeForm_form.get_head_context(),
                 'visible': has_permit(self.crt_user,'TbMatch.quit_ticket')},
                {'label':'清空直播','editor':'com-op-btn','confirm_msg':'确定要清空',
                 'row_match':'many_row',
                 'visible': self.permit.can_edit(),
                 'action':'var matchs=ex.map(scope.ps.selected,(item)=>{return item.pk});cfg.show_load();ex.director_call("match.clear_live_url",{matchs:matchs}).then((resp)=>{cfg.hide_load();cfg.toast("清空"+resp.count+"条")})'}

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
                'iscloseliveodds': 70,
                
                'oddsadjustment' :100,
                'oddsadjustmax' :120,
                'baseticketeamout':100,
                
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'matchdate':
                head['editor'] = 'com-table-label-shower'
            if head['name'] in ('iscloseliveodds', 'isshow'):
                head['editor'] = 'com-table-bool-shower'

            if head['name']=='matchid':
                head['editor']='com-table-switch-to-tab'
                head['ctx_name']='match_tabs'
                if has_permit( self.crt_user, 'manual_specialbetvalue'):
                    head['tab_name']='special_bet_value' 
                else:
                    head['tab_name']='match_base_info'            

            if head['name'] in ['tournamentid','sportid']:
                head['editor']='com-table-label-shower'

            if head['name'] == 'isdangerous':
                head['editor'] ='com-table-map-html'
                head['map_express']="scope.row[scope.head.name]==1?scope.head.danger_img:''"
                head['danger_img']="<img class='danger-ball' src='/static/images/danger.png' />"
                head['css']='.danger-ball{height:20px;display:inline-block;}'

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
                '_tournamentid_label':inst._tournamentid_label,
                '_sportid_label':inst._sportid_label,
                'num_stake': inst.num_stake, # '%s/%s'%(inst.num_stake_total-inst.num_stake_parlay,inst.num_stake_parlay),
                'manual_settle_need_audit':inst.manual_settle_need_audit
            }

@director_view('match.clear_live_url')
def clear_liveurl(matchs):
    rt = mydb['Match'].update({'MatchID':{'$in':matchs},'LiveUrl':{'$ne':None}},{'$set':{'LiveUrl':None}})
    return {
        'count':rt.get('nModified')
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

    class Meta:
        model = TbMatch
        exclude = [ 'matchstatustype', 'specialcategoryid', 'mainleagueid', 
                   'mainhomeid', 'mainawayid', 'mainmatchid', 'maineventid', 'settlestatus', 'prematchdate','createtime']

    field_sort = ['matchid', 'team1zh', 'team2zh', 'matchdate','weight','ticketdelay', 'marketstatus'] #'oddsadjustment','oddsadjustmax','baseticketeamout'
    overlap_fields =['updatetime']
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
        if head['name'] in [ 'oddsadjustment','oddsadjustmax']:
            head['fv_rule']='range(0~0.99);digit(2)'
            
        return head

    def dict_row(self, inst):
        settlemsg = TbManualsettlemsg.objects.filter(matchid = inst.matchid).first()
        
        return {'isshow': not bool(inst.ishidden),
                '_matchdate_label':inst.matchdate.strftime('%Y-%m-%d %H:%M') if inst.matchdate else '',
                'manual_settle_need_audit': settlemsg.status if settlemsg else ''
                }

    def clean_save(self):
        if 'matchdate' in self.changed_data:
            self.instance.prematchdate = self.instance.matchdate - datetime.timedelta(minutes=15)
        #if 'isrecommend' in self.changed_data and self.cleaned_data.get('isrecommend'):
            #now = timezone.now()
            #count = TbMatch.objects.filter(sportid=self.instance.sportid,isrecommend=True,matchdate__gte=now).count()
            #if count >= 5:
                #raise UserWarning('每种体育类型最多5场推荐,但是经过这次操作后,%s已经超过了此限制.'% TbSporttypes.objects.get(sportid=self.instance.sportid) )


    def save_form(self):
        msg = []
        super().save_form()

        self.updateMongo()
        self.proc_redis()
        
        if any([x in self.changed_data for x in ['oddsadjustment','baseticketeamout','oddsadjustmax'] ] ): 
            dc ={
                'Type':2,
                'Ids':[self.instance.matchid]
            }
            notifyAdjustOddsBase(json.dumps(dc))
        
        return {'msg': msg,}

    def updateMongo(self): 
        match =  self.instance
        beijin_tz = datetime.timezone(datetime.timedelta(hours=8))
        dc = {
            'MatchID': match.matchid,
            'IsRecommend': match.isrecommend,
            'IsHidden': match.ishidden,
            'IsCloseLiveOdds': match.iscloseliveodds, 
            'HasLiveOdds':match.hasliveodds,
            'Team1ZH': match.team1zh,
            'Team2ZH': match.team2zh,
            'StatusCode': match.statuscode,
            #'Period1Score': match.period1score,
            'MatchScore': match.score,
            'Winner': match.winner,
            'MarketStatus':match.marketstatus,
            'MatchDate':match.matchdate.replace(tzinfo = beijin_tz ) ,#.replace(tzinfo= datetime.timezone.utc ), #datetime.timezone(datetime.timedelta(hours=8))).astimezone(datetime.timezone.utc),
            'PreMatchDate':match.prematchdate.replace(tzinfo = beijin_tz) ,#.replace(tzinfo= datetime.timezone.utc ), #datetime.timezone(datetime.timedelta(hours=8))).astimezone(datetime.timezone.utc)
        }        
        updateMatchMongo(dc)

    def proc_redis(self): 
        if 'iscloseliveodds' in self.changed_data:
            if self.instance.iscloseliveodds == 0:
                redisInst.delete('backend:match:iscloseliveodds:%(matchid)s' % {'matchid': self.instance.eventid})
            else:
                redisInst.set('backend:match:iscloseliveodds:%(matchid)s' % {'matchid': self.instance.eventid}, 1,
                              60 * 1000 * 60 * 24 * 7)
        if 'team1zh' in self.changed_data or 'team2zh' in self.changed_data:
            key = 'public:match:%(eventid)s'%{'eventid':self.instance.eventid}
            rstr = redisInst0.get(key)
            if rstr:
                dc = json.loads(rstr)
                dc.update({
                    "Team1Zh": self.instance.team1zh,
                    "Team2Zh": self.instance.team2zh,
                })
                redisInst0.set(key,json.dumps(dc,ensure_ascii=False))

class TbLivescoutTable(ModelTable):
    """危险球表格"""
    model = TbLivefeed
    exclude=[]
    fields_sort=['matchid','betstatus','matchscore','eventdesc','servertime','createtime']
    def get_operation(self):
        return [
            {'name':'director_call',
             'director_name':'match.add_livescout',
             'editor':'com-op-switch',
             'label':'危险球',
            'pre_set':'rt={matchid:scope.self.vc.par_row.matchid,is_danger:scope.head.value}',
            'active_color':'red',
            'op_confirm_msg':'scope.value?"是否开启危险球?":"是否关闭危险球?"',
            'after_save':'rt=scope.ps.search()',
            # com-op-switch 里面调用的init_express
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
            'servertime':180,
            'createtime':180,
            'eventdesc':200,
        }
        if width_dc.get(head['name']):
            head['width']=width_dc.get(head['name'])
        if head['name'] == 'eventdesc':
            head['inn_editor'] = head['editor']
            head['editor'] ='com-table-rich-span'
            head['class']='middle-col btn-like-col'
            head['cell_class'] = 'var dc={"危险球解除":"success","有危险球":"warning","危险球解除(M)":"success","有危险球(M)":"warning"};rt=dc[scope.row.eventdesc]'
                
        return head
    
    def dict_row(self, inst):
        return {
            'servertime':inst.servertime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'createtime':inst.createtime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        }
    #def getExtraHead(self):
        #return [
            #{'name':'stopreason','label':'危险球原因'}
        #]

    def inn_filter(self, query):
        query = super().inn_filter(query)
        #query = query.extra(select={'stopreason':'SELECT TB_BetStopReason.description'},
                    #where=['TB_BetStopReason.id =TB_LiveScout.BrExtraInfo'],
                    #tables =['TB_BetStopReason'])
        if self.kw.get('matchid'):
            return query.filter(matchid=self.kw.get('matchid'),eventtypeid__in=[1010,1011,0]).order_by('-createtime')
        else:
            return query  

    #def dict_row(self, inst):
        #return {
            #'stopreason':inst.stopreason
        #}

@director_element('PeriodScoreTab')
class PeriodScoreTab(ModelTable):
    hide_fields=['tid']
    model = TbPeriodscore
    exclude=['createtime','type']

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
        names=['statuscode','scoretype']
        
        def clean_search_args(self):
            if not self.sort_str:
                self.sort_str='statuscode'
        
    class filters(RowFilter):
        names = ['scoretype']
        

@director_view('match.livescout_status')
def match_livescout_status(matchid,**kws):
    live = TbLivefeed.objects.filter(matchid=matchid,eventtypeid__in=[33,34]).order_by('-createtime').first()
    if not live or live.eventtypeid ==1010:    
        return False
    else:
        return True

@director_view('match.add_livescout')
def add_livescout(new_row,**kws):
    match = TbMatch.objects.get(matchid=new_row.get('matchid'))
    #TbLivescout.objects.order_by('-createtime').first()
    if new_row.get('is_danger'):
        TbLivefeed.objects.create(extrainfo='999',side=0,statuscode=match.statuscode,sportid=match.sportid,matchid=new_row.get('matchid'),livefeedid=0,matchscore=match.score,eventid=match.eventid,eventtypeid=1011,betstatus=3,eventdesc='有危险球(M)')
        op_log.info('手动关闭%s的危险球'%match)
    else:
        TbLivefeed.objects.create(extrainfo='999',side=0,statuscode=match.statuscode,sportid=match.sportid,matchid=new_row.get('matchid'),livefeedid=0,matchscore=match.score,eventid=match.eventid,eventtypeid=1010,betstatus=2,eventdesc='危险球解除(M)')
        with connections['Sports'].cursor() as cursor:
            sql_args = {
                'MatchID':new_row.get('matchid')
            }
            sql = r"exec dbo.SP_DangerousBack %(MatchID)s" \
                % sql_args
            cursor.execute(sql) 
            cursor.commit()
        op_log.info('手动开启%s的危险球'%match)
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
    for odds in TbOdds.objects.filter(matchid=matchid,status=1,).extra(select={
        'sort':'SELECT TB_Markets.Sort',
        }, tables=['TB_Markets'],where=['TB_Markets.MarketID=TB_Odds.MarketID']).values('marketname','marketid','sort').distinct():
        markets.append({
            'name':odds.get('marketname'),
            'marketid':odds.get('marketid'),
            'marketname':odds.get('marketname'),
            'sort':odds.get('sort'),
            'opened':True,
        })

    for switch in TbMarkethcpswitch.objects.filter(matchid=matchid,type=2, status = 1).extra(select={
        'sort':'SELECT TB_Markets.Sort',
        }, tables=['TB_Markets'],where=['TB_Markets.MarketID=TB_MarketHcpSwitch.MarketID']):

        markets.append({
            'name':switch.marketname,
            'marketid':switch.marketid_id,
            'marketname':switch.marketname,
            'sort':switch.sort,
            'opened':False,
        })
    # 填充 因为 odds被封了，而造成market消失的那些market
    loaded_marketid = [x['marketid'] for x in markets]
    for switch in TbMarkethcpswitch.objects.filter(matchid=matchid,type=3,status=1).extra(select={
        'sort':'SELECT TB_Markets.Sort',
        }, tables=['TB_Markets'],where=['TB_Markets.MarketID=TB_MarketHcpSwitch.MarketID']).values('marketname','marketid','sort').distinct():
        if switch['marketid'] not in loaded_marketid:
            markets.append({
                'name':switch['marketname'],
                'marketid':switch['marketid'],
                'marketname':switch['marketname'],
                'sort':switch['sort'],
                'opened':True,
            })

    #for market in TbMarkets.objects.filter(enabled=1):
        #markets.append({
            #'name':market.marketnamezh,
            #'marketid':market.marketid,
            #'sort':market.sort,
            #'opened':True,
        #})

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
                    'fortherest':odd.fortherest if odd.fortherest is not None else '',
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
                'fortherest':switch.fortherest,
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
            pass
            #for i in markets:
                #if i['marketid'] == oddsswitch.marketid_id:
                    #i['opened'] = False
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
            # type=2 是玩法market
            if item.type==2 and item.marketid_id==market['marketid']:
                oddSwitch = item
                dbOddSwitchs.remove(item)
                break
        if not oddSwitch:
            oddSwitch = TbMarkethcpswitch(matchid=matchid, type=2,marketid_id=market['marketid'],status=100)

        if not market['opened']:
            if oddSwitch.status != 1:
                oddSwitch.status = 1
                oddSwitch.marketname = market.get('marketname')
                log_msg += '屏蔽玩法：%s' % market['name']
                batchOperationSwitch.append(oddSwitch)
        else:
            if oddSwitch.status != 0:
                oddSwitch.status = 0
                if oddSwitch.pk: # 有pk，证明switch存在于数据库，但是status=0 表示即将开启(删除)
                    log_msg += '开启玩法：%s' % market['name']
                batchOperationSwitch.append(oddSwitch)

    for spbt in specialbetvalue:
        par_market = None
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
            spSwitch = TbMarkethcpswitch(matchid=matchid, type=3,marketid_id=market['marketid'],fortherest= spbt['fortherest'] if spbt['fortherest'] is not None else '',
                                         specialbetname=spbt['specialbetname'],marketname=spbt['marketname'],
                                         specialbetvalue=spbt['specialbetvalue'],specifiers=spbt['specifiers'],status=100)     


        if par_market and par_market['opened']:
            if not spbt['opened']:
                if spSwitch.status != 1:
                    spSwitch.status = 1
                    log_msg += '屏蔽盘口：%s' % spbt['specialbetvalue']
                    batchOperationSwitch.append(spSwitch)
            else:
                if spSwitch.status != 0:
                    spSwitch.status = 0
                    if spSwitch.pk:
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
    for item in new_list:
        if item.type==2:
            # 封玩法，需要把所有odds 取消
            TbOdds.objects.filter(matchid=item.matchid,marketid=item.marketid_id).update(status=-1)

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

    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)
        if self.kw.get('matchid'):
            self.match = TbMatch.objects.get(matchid = self.kw.get('matchid'))

    def getExtraHead(self):
        return [
            {'name':'outcome','label':'结果','editor':'com-table-span','width':250},
            {'name':'ops','label':'','editor':'com-table-ops-cell','width':50,
             'ops':[
                 {
                     'editor':'com-op-plain-btn',
                         'label':'清空',
                         'class':'btn btn-primary btn-xs',
                         'action':""" Vue.set( scope.row,'outcome','') """}
                 ]},

        ]

    def get_rows(self):
        bf =[]

        if self.match.sportid ==1:
            bf = [
                {'marketid':'','pk':-1,'marketname':'score','marketnamezh':'比分型'}
            ]
        elif self.match.sportid == 2:
            if self.match.tournamentid in[ 698,7557]:
                bf = [
                    {'marketid':'','pk':-3,'marketname':'score','marketnamezh':'比分型'}
                ]
            else:
                bf = [
                    {'marketid':'','pk':-2,'marketname':'score','marketnamezh':'比分型'}
                ]
        else: # self.match.sportid == 109:
            bf =[
                {'marketid':'','pk':-self.match.sportid,'marketname':'score','marketnamezh':'比分型'}
            ]

        rows = super().get_rows()
        rows = bf+rows
        try:
            settlemsg = TbManualsettlemsg.objects.get(matchid= self.kw.get('matchid'))
            match_outcome = json.loads(settlemsg.settlemsg)
            for msg_row in match_outcome:
                for row in rows:
                    if msg_row.get('pk')==row.get('pk'):
                        row['outcome'] = msg_row
                        break
        except TbManualsettlemsg.DoesNotExist as e:
            pass
        
        return rows

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
            rt=cfg.pop_vue_com(panel.editor,{row:scope.row.outcome,init_express:panel.init_express,fields_group:panel.fields_group,table_grid:panel.table_grid,ops_loc:"bottom",heads:panel.heads,ops:panel.ops,par_row:scope.ps.vc.par_row,init_express:panel.init_express})\
            .then(res=>Vue.set(scope.row,"outcome",res))'
            head.update(outcome_header)
        return head


    def inn_filter(self, query):
        if self.match.sportid ==1:
            return query.filter(enabled=True,marketid__in = [8,9,100,101,102,103,104,105,106,107,108,109,110,163,174,])
        elif self.match.sportid ==2:
            # 291 是篮球的
            return query.filter(enabled=True,marketid__in = [291])
        elif self.match.sportid == 109:
            # 反恐精英 
            return query.filter(enabled=True,marketid__in = [333])
        elif self.match.sportid == 110:
            # 英雄联盟 
            return query.filter(enabled=True,marketid__in = [333,397,556,557,558])
        elif self.match.sportid == 111:
            # 刀塔2
            return query.filter(enabled=True,marketid__in = [396,397,398,555])
        elif self.match.sportid == 5:
            # 网球
            return query.filter(enabled=True,marketid__in=[195,206])
        #elif self.match.sportid == 19:
            #return query.filter(enabled=True,marketid__in=[])
        else:
            return query.none()

    def get_operation(self):
        return [
            {'name':'outcome','label':'保存结果','editor':'com-op-btn',
             'class':'btn btn-info','action':'''rt=Promise.resolve()
            .then(()=>{ return out_come_save(scope.ps.rows,scope.ps.vc.par_row.matchid)} )
            .then(()=>{
                return ex.director_call("get_row",
                    {
                        director_name:scope.ps.vc.par_row._director_name,matchid:scope.ps.vc.par_row.matchid
                    })
                 })
            .then((res)=>{ex.vueAssign(scope.ps.vc.par_row,res)}) ''', 
            'visible':has_permit(self.crt_user, 'save_manual_outcome')},
            {'label':'提交审核','editor':'com-op-btn',
             'class':'btn btn-primary',
             'action':''' cfg.confirm("确定提交手动结算信息?审核过程中，将不能修改数据。")
             .then(()=>{
                cfg.show_load()
                return ex.director_call("submit_manual_settle_to_audit",{matchid:scope.ps.vc.par_row.matchid})
             }).then((resp)=>{
                cfg.hide_load()
                if(resp.msg){
                     cfg.toast(resp.msg)
                }else{
                    cfg.toast('提交审核成功，等待管理员审核。')
                }
             })
             ''',
             'visible':has_permit(self.crt_user, 'save_manual_outcome')},
            
            {'label':'审核通过','editor':'com-op-btn','class':'btn btn-success',
             'action':'''cfg.confirm("审核通过会立即通知后台进行结算，结果不可挽回，确定通过?")
             .then(()=>{
                 cfg.show_load()
                 return ex.director_call("confirm_manual_settle_to_audit",{matchid:scope.ps.vc.par_row.matchid})
             }).then((resp)=>{
                 cfg.hide_load()
                  if(resp.msg){
                     cfg.toast(resp.msg)
                  }else{
                    cfg.toast('操作成功')
                  }
             })''',
             'visible':has_permit(self.crt_user,'audit_manual_outcome')},
            {'label':'审核拒绝','editor':'com-op-btn',
             'class':'btn btn-danger',
             'action':'''cfg.confirm('审核拒绝后，结算数据会被退回重新填写，确定要拒绝？')
             .then(()=>{
                cfg.show_load()
                return ex.director_call("reject_manual_settle_to_audit",{matchid:scope.ps.vc.par_row.matchid})
             }).then((resp)=>{ 
                cfg.hide_load()
                  if(resp.msg){
                     cfg.toast(resp.msg)
                  }else{
                    cfg.toast('操作成功')
                  }
             })
             ''',
             'visible':has_permit(self.crt_user,'audit_manual_outcome')},
        ]

@director_view('submit_manual_settle_to_audit')
def submit_manual_settle_to_audit(matchid):
    count = TbManualsettlemsg.objects.filter(matchid = matchid,status =0).update(status = 1)
    if not count:
        return {'msg':'没有可提交的结算数据'}
    else:
        op_log.info('提交手动结算审核 matchid = %s'%matchid)
        return {}
    
@director_view('confirm_manual_settle_to_audit')
def confirm_manual_settle_to_audit(matchid):
    settlemsg = TbManualsettlemsg.objects.filter(matchid = matchid,status =1).first()
    if not settlemsg:
        return {'msg':'没有结算数据可以审核'}
    else:
        rows = json.loads(settlemsg.settlemsg)
        real_out_come_save(rows ,matchid)
        op_log.info('审核手动结算:matchid=%s ;settlemsg = %s '%(matchid,settlemsg.settlemsg,))
        settlemsg.delete()
        return {}
        
@director_view('reject_manual_settle_to_audit')
def reject_manual_settle_to_audit(matchid):
    count = TbManualsettlemsg.objects.filter(matchid = matchid,status =1).update(status =0)
    if not count:
        return {'msg':'没有结算数据'}
    else:
        op_log.info('拒绝手动结算审核 matchid = %s'%matchid)
        return {}


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
    match  = TbMatch.objects.get(matchid = matchid)
    if match.sportid in  [109,110,111]:
        row ={}
    else:
        row ={
            'has_half1':True,
            'has_half2':True,
        }
    for score in TbPeriodscore.objects.filter(matchid=matchid,scoretype__in=[1,5]): # statuscode__in=[6,7,13,14,15,16,40,50,100,141,142,143,144,145,146,147,14140,14240,14340,14440,14540,14640,14740,],
        row['home_%s_%s'%(score.statuscode,score.scoretype)] = score.home
        row['away_%s_%s'%(score.statuscode,score.scoretype)] = score.away
        row['has_%s_%s'%(score.statuscode,score.scoretype)] = True

    return row

@director_view('out_com_save')
def out_com_save(rows,matchid):
    if matchid:
        try:
            settlemsg = TbManualsettlemsg.objects.get(matchid = matchid)
            if settlemsg.status != 0:
                raise UserWarning('当前正在审核中，不能进行编辑')
            
        except TbManualsettlemsg.DoesNotExist as e:
            settlemsg = TbManualsettlemsg.objects.create(matchid = matchid,status=0)
        settlemsg .settlemsg = json.dumps(rows)
        settlemsg.save()

            
def real_out_come_save(rows,matchid):
    send_dc = {
        'MatchID':matchid,
        'SendTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Source':'AdminBackend',
        'IsSettleByScore':False,
        'Special':[],
        'Unsubscribe':False,
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
        206:'setnr=%(org_sp)s'
    }

    batch_create=[]
    for row in rows:
        if row['pk'] == -1:
            # 足球手动输入比分
            send_dc['IsSettleByScore']=True
            dc = {}

            has_half2 = row.pop('has_half2',False)
            has_overtime = row.pop('has_overtime',False)
            has_penalty = row.pop('has_penalty',False)
            TbPeriodscore.objects.filter(matchid=matchid,scoretype__in=[1,5]).delete()

            # 比分
            home_6_1 = int( row.get('home_6_1') )
            away_6_1 = int( row.get('away_6_1') )
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=6,scoretype=1,home=home_6_1,away=away_6_1 ,type=0) )
            if has_half2:
                home_100_1 = int( row.get('home_100_1') )
                away_100_1 = int( row.get('away_100_1') )
                home_7_1 = home_100_1 - home_6_1
                away_7_1 = away_100_1 - away_6_1
                if home_7_1 < 0  or away_7_1 < 0:
                    raise UserWarning('全场部分不能少于上半场比分')
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=7,scoretype=1,home=home_7_1,away=away_7_1 ,type=0) )
                if row.get('has_100_1'):
                    batch_create.append( TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,home=home_100_1,away=away_100_1 ,type=0) )

                accumulate_home = home_100_1
                accumulate_away = away_100_1
            if has_overtime:
                home_40_1 = int( row.pop('home_40_1') )
                away_40_1 = int( row.pop('away_40_1') )
                accumulate_home += home_40_1
                accumulate_away += away_40_1
                home_110_1 = accumulate_home
                away_110_1 = accumulate_away

                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=1,type=1,home=home_40_1,away=away_40_1)) 
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=110,scoretype=1,type=1,home=home_110_1,away=away_110_1) )
            #else:
                #if has_half2:
                    #batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=1,type=1,home=-1,away=-1)) 

            if has_penalty:
                home_50_1 = int( row.pop('home_50_1') )
                away_50_1 = int( row.pop('away_50_1') )
                home_120_1 = accumulate_home + home_50_1
                away_120_1 = accumulate_away + away_50_1

                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=50,scoretype=1,type=2,home=home_50_1,away=away_50_1 ) )
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=120,scoretype=1,type=2,home=home_120_1,away=away_120_1 ) )

            # 角球
            home_6_5 = int( row.get('home_6_5') )
            away_6_5 = int( row.get('away_6_5') )
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=6,scoretype=5,home=home_6_5,away=away_6_5 ,type=0) )
            if has_half2:
                home_100_5 = int( row.get('home_100_5') )
                away_100_5 = int( row.get('away_100_5') )

                home_7_5 = home_100_5 - home_6_5
                away_7_5 = away_100_5 - away_6_5

                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=7,scoretype=5,home=home_7_5,away=away_7_5 ,type=0) )
                if row.get('has_100_1'):
                    batch_create.append( TbPeriodscore(matchid=matchid,statuscode=100,scoretype=5,home=home_100_5,away=away_100_5 ,type=0) )
                if home_7_5 <0 or away_7_5 <0:
                    raise UserWarning('全场部分不能少于上半场角球')

            if has_overtime:
                home_40_5 = int( row.pop('home_40_5') )
                away_40_5 = int( row.pop('away_40_5') )
                home_110_5 = home_100_5 + home_40_5
                away_110_5 = away_100_5 + away_40_5
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=5,type=1,home=home_40_5,away=away_40_5) )
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=110,scoretype=5,type=1,home=home_110_5,away=away_110_5) )
            #else:
                #if has_half2:
                    #batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=5,type=1,home=-1,away=-1) )

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
        if row['pk'] in [9,195]:
            send_dc['Special'].append(
                {'Specifiers':'','MarketId':row['pk'],'OutcomeId':row['OutcomeId']}
            )

        if row['pk'] in [333,396,397,398,556,557,558]:
            outcome_list = json.loads(row.get('content','[]') )
            for item in outcome_list:
                send_dc['Special'].append(
                    {'Specifiers':'mapnr=%s|xth=%s'%(item.get('Specifiers_1'),item.get('Specifiers')),'OutcomeId':item['OutcomeId'],'MarketId':row['pk'],}
                )
        if row['pk'] in [555]:
            outcome_list = json.loads(row.get('content','[]') )
            for item in outcome_list:
                send_dc['Special'].append(
                    {'Specifiers':'mapnr=%s|hcp=%s'%(item.get('Specifiers'),item.get('Specifiers_1')),
                     'Score':'%s:%s'%(item.pop('OutcomeId'),item.pop('OutcomeId_1') ),
                     'MarketId':row['pk'],}
                )

        if row['pk'] == -2:
            # 普通篮球手动输入比分 （有四小节）
            send_dc['IsSettleByScore']=True
            dc = {}
            # 加时
            has_40_1 = row.pop('has_40_1',False)
            TbPeriodscore.objects.filter(matchid=matchid,scoretype=1).delete()
            if row.get('has_13_1'):
                home_13_1 = int( row.get('home_13_1') )
                away_13_1 = int( row.get('away_13_1') )
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=13,scoretype=1,home=home_13_1,away=away_13_1 ,type=0) )
            if row.get('has_14_1'):
                home_14_1 = int( row.get('home_14_1') )
                away_14_1 = int( row.get('away_14_1') )
                home_6_1 = home_13_1 + home_14_1
                away_6_1 = away_13_1 + away_14_1
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=14,scoretype=1,home=home_14_1,away=away_14_1 ,type=0) )
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=6,scoretype=1,home=home_6_1,away=away_6_1 ,type=0) )
                
            if row.get('has_15_1'):
                home_15_1 = int( row.get('home_15_1') )
                away_15_1 = int( row.get('away_15_1') )
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=15,scoretype=1,home=home_15_1,away=away_15_1 ,type=0) )
            if row.get('has_16_1'):
                home_16_1 = int( row.get('home_16_1') )
                away_16_1 = int( row.get('away_16_1') )

                home_7_1 = home_15_1 + home_16_1
                away_7_1 = away_15_1 + away_16_1
               
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=7,scoretype=1,home=home_7_1,away=away_7_1 ,type=0) )
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=16,scoretype=1,home=home_16_1,away=away_16_1 ,type=0) )
                
                if row.get('has_100_1'):
                    home_100_1 = home_6_1 + home_7_1
                    away_100_1 = away_6_1 + away_7_1
                    batch_create.append( TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,home=home_100_1,away=away_100_1 ,type=0) )

            if has_40_1:
                home_40_1 = int( row.pop('home_40_1') )
                away_40_1 = int( row.pop('away_40_1') )
                home_110_1 = home_100_1 + home_40_1
                away_110_1 = away_100_1 + away_40_1
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=1,type=1,home=home_40_1,away=away_40_1)) 
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=110,scoretype=1,type=1,home=home_110_1,away=away_110_1)) 

        if row['pk'] == -3:
            # NCAA 篮球手动输入比分 （只有上下半场,有加时赛）
            send_dc['IsSettleByScore']=True
            dc = {}
            has_overtime = row.pop('has_overtime',False)

            TbPeriodscore.objects.filter(matchid=matchid,scoretype=1).delete()

            home_6_1 = int( row.get('home_6_1') )
            away_6_1 = int( row.get('away_6_1') )
            
            batch_create.append( TbPeriodscore(matchid=matchid,statuscode=6,scoretype=1,home=home_6_1,away=away_6_1 ,type=0) )
            if  row.get('has_100_1') :
                home_100_1 = int( row.get('home_100_1') )
                away_100_1 = int( row.get('away_100_1') )
                home_7_1 = home_100_1 - home_6_1
                away_7_1 = away_100_1 - away_6_1
                batch_create.append( TbPeriodscore(matchid=matchid,statuscode=7,scoretype=1,home=home_7_1,away=away_7_1 ,type=0) )
                if row.get('has_finish'):
                    batch_create.append( TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,home=home_100_1,away=away_100_1 ,type=0) )

            if has_overtime:
                home_40_1 = int( row.pop('home_40_1') )
                away_40_1 = int( row.pop('away_40_1') )
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=40,scoretype=1,type=1,home=home_40_1,away=away_40_1)) 
                if row.get('has_finish'):
                    home_110_1 = home_100_1 + home_40_1
                    away_110_1 = away_100_1 + away_40_1
                    batch_create.append(TbPeriodscore(matchid=matchid,statuscode=110,scoretype=1,type=1,home=home_110_1,away=away_110_1)) 
                
        if row['pk'] == -109:
            send_dc['IsSettleByScore']=True
            TbPeriodscore.objects.filter(matchid=matchid,scoretype=1).delete()

            round_count = int( row.get('round_count') )
            home_round = 0
            away_round = 0
            for i in range(1,round_count+1):
                home = int(  row.get('home_14%s_1'%i) )
                away = int(  row.get('away_14%s_1'%i) )
                home_score = home
                away_score = away
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=int('14%s'%i),scoretype=1,type=1,home=home,away=away  ) ) 
                if row.get('has_overtime_14%s'%i):
                    home40 = int(  row.get('home_14%s40_1'%i) )
                    away40 = int(  row.get('away_14%s40_1'%i) )
                    home_score += home40
                    away_score += away40
                    batch_create.append(TbPeriodscore(matchid=matchid,statuscode=int('14%s40'%i),scoretype=1,type=1,home=home40,away=away40  ) ) 
                if home_score > away_score:
                    home_round += 1
                elif home_score == away_score:
                    raise UserWarning('请看清楚，每局比分不能相等。')
                else:
                    away_round +=1
            batch_create.append(TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,type=1,home=home_round,away=away_round  ) ) 
        if row['pk'] in [-110,-111]:
            send_dc['IsSettleByScore']=True
            TbPeriodscore.objects.filter(matchid=matchid,scoretype=1).delete()
            round_count = int( row.get('round_count') )
            home_round = 0
            away_round = 0
            for i in range(1,round_count+1):
                home = int(  row.get('home_14%s_1'%i) )
                if home:
                    home_round += 1
                else:
                    away_round +=1
                away = 0 if home else 1
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=int('14%s'%i),scoretype=1,type=1,home=home,away=away  ) ) 
            batch_create.append(TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,type=1,home=home_round,away=away_round  ) ) 
        if row['pk'] == -5:
            # 网球分数
            send_dc['IsSettleByScore'] =True
            TbPeriodscore.objects.filter(matchid=matchid,scoretype=1).delete()
            set_count = int( row.get('set_count') )
            home_set = 0
            away_set = 0
            for i in range(1,set_count+1):
                home = int(  row.get('home_%s_1'%(i+7) ) )
                away = int(  row.get('away_%s_1'%(i+7) ) )
                if home > away:
                    home_set += 1
                elif home < away:
                    away_set +=1
                else:
                    raise UserWarning('每盘比分不能相等')
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=int('%s'%(i+7)),scoretype=1,type=1,home=home,away=away  ) ) 
            if home_set == away_set:
                raise UserWarning('主客赢的盘数不能相等')
            batch_create.append(TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,type=1,home=home_set,away=away_set  ) ) 
        if row['pk']== -19:
            # 斯诺克
            send_dc['IsSettleByScore'] =True
            TbPeriodscore.objects.filter(matchid=matchid,scoretype=1).delete()
            set_count = int( row.get('set_count') )
            home_set = 0
            away_set = 0
            for i in range(1,set_count+1):
                home = int(  row.get('home_%s_1'%(i) ) )
                away = int(  row.get('away_%s_1'%(i) ) )
                if home > away:
                    home_set += 1
                elif home < away:
                    away_set +=1
                else:
                    raise UserWarning('每盘比分不能相等')
                batch_create.append(TbPeriodscore(matchid=matchid,statuscode=int('%s'%(i)),scoretype=1,type=1,home=home,away=away  ) ) 
            if home_set == away_set:
                raise UserWarning('主客赢的盘数不能相等')
            batch_create.append(TbPeriodscore(matchid=matchid,statuscode=100,scoretype=1,type=1,home=home_set,away=away_set  ) ) 
            
    TbPeriodscore.objects.bulk_create(batch_create)
    if send_dc.get('IsSettleByScore'):
        home_score =0
        away_score =0
        match = TbMatch.objects.get(matchid=matchid)

        for inst in batch_create:
            if inst.scoretype==1:
                #if match.sportid== 1 :
                if row['pk'] in [-1,-3]:
                    if inst.statuscode in [6,7,40,50]:
                        home_score += int(inst.home)
                        away_score += int(inst.away)
                #elif match.sportid== 2:
                elif row['pk'] == -2:
                    if inst.statuscode in [13,14,15,16,40,]:
                        home_score += int(inst.home)
                        away_score += int(inst.away)
                
                elif inst.statuscode==100:
                    home_score += int(inst.home)
                    away_score += int(inst.away)

 
            #if match.sportid in [1,2] and inst.scoretype==1 and inst.statuscode in [6,7,40,50]:
                #if inst.home >= 0 and inst.away >= 0:
                    #home_score += int(inst.home)
                    #away_score += int(inst.away)
            ##elif match.sportid in [109,110,111,5,19]:
            #else:
                #if inst.statuscode==100:
                    #home_score =inst.home
                    #away_score =inst.away
                    #break
                    
        statuscode_list = [x.statuscode for x in batch_create]
        
        if 100 in statuscode_list:
            match.score = '%s:%s'%(home_score,away_score)
            if home_score <away_score:
                match.winner = 2
            elif home_score > away_score:
                match.winner = 1
            else:
                match.winner = 3
    
            match.marketstatus=3
            
            statuscode= max([x for x in [100,110,120] if x in statuscode_list])
            match.statuscode = statuscode
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

@director_view('batch_recommand')
def batch_recommand(rows):
    sportid_dc={}
    matchlist = []
    for row in rows:
        sportid = row['sportid']
        if sportid not in sportid_dc:
            sportid_dc[sportid] = []
        sportid_dc[sportid] .append(row['matchid'])
        matchlist.append(row['matchid'])
#def batch_recommand(rows,new_row):
    #sportid_dc={}
    #matchlist = []
    #for row in rows:
        #sportid = row['sportid']
        #if sportid not in sportid_dc:
            #sportid_dc[sportid] = []
        #sportid_dc[sportid] .append(row['matchid'])
        #matchlist.append(row['matchid'])
        #row.update(new_row)
    #now = timezone.now()
    #for k,v in sportid_dc.items():
        #count = TbMatch.objects.filter(sportid=k,isrecommend=True,matchdate__gte=now).count()
        #if count + len(v) > 5:
            #raise UserWarning('每种体育类型最多5场推荐,但是经过这次操作后,%s已经超过了此限制.'% TbSporttypes.objects.get(sportid=k) )
    return  save_rows(rows)

   
        
    #TbMatch.objects.filter(matchid__in=matchlist).update(isrecommend = True)
    
        

@director_view('notify_match_recommend')
def notify_match_recommend(rows):
    ls =[x['pk'] for x in rows]
    msg = json.dumps(ls)
    notifyMatchRecommond(msg)

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
