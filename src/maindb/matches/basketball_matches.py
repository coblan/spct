from helpers.director.shortcut import page_dc, director, director_view
from .matches import MatchsPage, MatchForm, PeriodTypeForm, get_special_bet_value, produce_match_outcome, save_special_bet_value_proc, quit_ticket
from ..models import TbMatchesBasketball, TbOddsBasketball,TbTournamentBasketball
from maindb.mongoInstance import updateMatchBasketMongo
from .match_outcome_forms import  BasketPoints, Quarter, FirstBasket, LastBasket, HightestQuarterScore, FirstReachScore, TotalPoints, Shot3Points,BasketTwosection
from ..redisInstance import redisInst
#from datetime import timezone as org_timezone
#from django.utils.timezone import datetime
import datetime


class BasketMatchsPage(MatchsPage):
    
    def get_context(self):
        ctx = super().get_context()
        #ctx['extra_table_logic'] = 'match_logic'
        ls = [
            {'name': 'special_bet_value',
             'label': '盘口',
             'com': 'com-tab-special-bet-value',
             'update_director': 'basketball_get_special_bet_value',
             'save_director': 'basketball_save_special_bet_value',
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
    
    class tableCls(MatchsPage.tableCls):
        model = TbMatchesBasketball
        
        #def inn_filter(self, query):
            #return query.extra(
                #where=["TB_SportTypes.source= TB_Matches_Basketball.source","TB_SportTypes.SportID=1"],
                #tables=['TB_SportTypes'],
            #)        
        
        def get_operation(self):
            PeriodTypeForm_form =  PeriodTypeForm(crt_user= self.crt_user)
            
            points_form = BasketPoints(crt_user= self.crt_user)
            #quarter = Quarter(crt_user= self.crt_user)
            #firstbasket = FirstBasket(crt_user= self.crt_user)
            #lastbasket = LastBasket(crt_user= self.crt_user)
            #highest_quarter_score_team =  HightestQuarterScore(crt_user= self.crt_user)
            #totalpoint = TotalPoints(crt_user= self.crt_user)
            #shot3 = Shot3Points(crt_user= self.crt_user)
            #first_score = FirstReachScore(crt_user= self.crt_user)
            towsection = BasketTwosection(crt_user=self.crt_user)
            ops = [
                 {'fun': 'pop_panel',
                'editor': 'com-op-btn',
                'panel_express':'rt="com-form-produceMatchOutcomePanel"',
                #'panel_express': 'rt=manul_outcome_panel_express_parse(scope.kws.panel_map,scope.kws.play_type,scope.ts.selected[0].specialcategoryid)',
                'label': '手动结算',
                'row_match': 'one_row',
                'ctx_express': 'var row =ex.copy(scope.ts.selected[0]); var ctx =ex.isin(row.tournamentid,[698,7557])?scope.kws.ctx_dict.towsection:scope.kws.ctx_dict.normal;ctx.row=row;ctx.row.meta_type="manul_outcome";rt=ctx',
                #'ctx_express': 'rt=manul_outcome_panel_ctx(scope.ts.selected[0],scope.kws,scope.ts.selected[0].specialcategoryid)',
                #'play_type': {
                    #'normal': [0], 
                    #'Quarter': [170],
                    #'firstBasket': [171],  #  哪个球队先得分
                    #'lastBasket': [172],
                    #'highest_score': [174],
                    #'totalpoint': [175],
                    #'shot3': [176],
                    #'race-to-first-number-of-points': [185],
                    #},
                #'row_adapt': {
                    #'normal': 'rt=scope.adaptor.parse_score(scope.row)',
                    #'Quarter': 'rt=scope.adaptor.parse_score(scope.row)',
                    #},
                #'panel_map': {
                    #'normal': 'com-form-produceMatchOutcomePanel',
                    #'Quarter': 'com-panel-pop-fields',
                    #'firstBasket': 'com-panel-pop-fields',
                    #'lastBasket': 'com-panel-pop-fields',
                    #'highest_score': 'com-panel-pop-fields',
                    #'totalpoint': 'com-panel-pop-fields',
                    #'shot3': 'com-panel-pop-fields',
                    #'race-to-first-number-of-points': 'com-panel-pop-fields',
                    #},
                'ctx_dict': {
                    'normal': points_form.get_head_context(),
                    #'Quarter': quarter.get_head_context(),
                    #'firstBasket': firstbasket.get_head_context(),
                    #'lastBasket': lastbasket.get_head_context(),
                    #'highest_score': highest_quarter_score_team.get_head_context(),
                    #'totalpoint': totalpoint.get_head_context(),
                    #'shot3': shot3.get_head_context(),
                    #'race-to-first-number-of-points': first_score.get_head_context(),
                    'towsection':towsection.get_head_context(),
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
                  'director_name': 'basketball_quit_ticket',
                  'label': '退单', 'confirm_msg': '确认要退单吗？', 'row_match': 'one_row',
                  'pre_set': 'rt={PeriodType:2}',
                  #'after_save': 'rt=cfg.showMsg(scope.new_row.Message)',
                 'fields_ctx': PeriodTypeForm_form.get_head_context(),
                 'visible': 'ishidden' in self.permit.changeable_fields(), 
                 'show': 'rt=scope.ts.selected.length==0 || ex.isin(scope.ts.selected[0].specialcategoryid,[0])',},
                {'fun': 'director_call', 'editor': 'com-op-btn', 
                  'director_name': 'football_quit_ticket',
                  'label': '退单1', 'confirm_msg': '确认要退单吗？', 'row_match': 'one_row',
                  'pre_set': 'rt={PeriodType:1}',
                  #'after_save': 'rt=cfg.showMsg(scope.new_row.Message)',
                 #'fields_ctx': PeriodTypeForm_form.get_head_context(),
                 'visible': 'ishidden' in self.permit.changeable_fields(), 
                 'show': 'scope.ts.selected.length!=0 && ex.isin(scope.ts.selected[0].specialcategoryid,[170,171,172,174,175,176,185])',},

            ]
            return ops
        
        class filters(MatchsPage.tableCls.filters):
            def dict_head(self, head):
                head = super().dict_head(head)
                if head['name'] == 'tournamentid':
                    #head['director_name']='get_basketball_league_options'
                    head['options']=[
                        {'label':str(x) ,'value':x.tournamentid} for x in TbTournamentBasketball.objects.extra(
                            where=["TB_SportTypes.source= TB_Tournament_Basketball.source","TB_SportTypes.SportID=1"],
                            tables=['TB_SportTypes'])                        
                    ]
                return head
    

class BasketMatchForm(MatchForm):
    proc_map = {
        0: BasketPoints,
        170: Quarter,
        171: FirstBasket,
        172: LastBasket,
        174: HightestQuarterScore,
        175: TotalPoints,
        176: Shot3Points,
        185: FirstReachScore,
        #2: NumberOfCorner,
    }    
    #tournamentid=698
    
    class Meta(MatchForm.Meta):
        model = TbMatchesBasketball
        #exclude = ['marketstatus', 'maineventid']
    field_sort = ['matchid', 'team1zh', 'team2zh', 'matchdate','q1score','q2score','q3score','q4score','overtimescore']
    readonly=['q1score','q2score','q3score','q4score','overtimescore']
    
    def updateMongo(self): 
        match = self.instance
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
            'MatchDate':match.matchdate.replace(tzinfo=datetime.timezone.utc) ,#datetime.timezone(datetime.timedelta(hours=8))).astimezone(datetime.timezone.utc),
            'PreMatchDate':match.prematchdate.replace(tzinfo=datetime.timezone.utc) , #datetime.timezone(datetime.timedelta(hours=8))).astimezone(datetime.timezone.utc),            
        }
        
        updateMatchBasketMongo(dc) 
    
    def proc_redis(self): 
        if 'closelivebet' in self.changed_data:
            if self.instance.closelivebet == 0:
                redisInst.delete('Backend:Basketball:match:closelivebet:%(matchid)s' % {'matchid': self.instance.eventid})
            else:
                redisInst.set('Backend:Basketball:match:closelivebet:%(matchid)s' % {'matchid': self.instance.eventid}, 1,
                              60 * 1000 * 60 * 24 * 7)
                
    def save_form(self):
        msg = []
        if self.kw.get('meta_type') == 'manul_outcome':
            #specialcategoryid = self.kw.get('specialcategoryid')
            #ProcCls = self.proc_map.get(specialcategoryid)
            if self.kw.get('tournamentid')==698:
                ProcCls=BasketTwosection
            else:
                ProcCls=BasketPoints
            proc_obj = ProcCls(crt_user = self.crt_user)
            self.instance.settletime = datetime.datetime.now()
            rt_msg =  proc_obj.manul_outcome( self.kw, self.instance)
            msg.append(rt_msg)
        else:
            super().save_form()
            
        self.updateMongo()
        self.proc_redis()
        return {'msg': msg,}  
   


@director_view('basketball_quit_ticket')
def basketball_quit_ticket(rows, new_row): 
    return quit_ticket(rows, new_row, sportid = 1)

@director_view('basketball_get_special_bet_value')
def basketball_get_special_bet_value(matchid): 
    return get_special_bet_value(matchid,sportid = 1,oddsModel = TbOddsBasketball )

@director_view('basketball_save_special_bet_value')
def basketball_save_special_bet_value(matchid, match_opened, oddstype, specialbetvalue): 
    return save_special_bet_value_proc(matchid, match_opened, oddstype, specialbetvalue, sportid = 1)

@director_view('basketball_produce_match_outcome')
def basketball_produce_match_outcome(row): 
    return produce_match_outcome(row, MatchModel = TbMatchesBasketball, sportid = 1, half_end_code = 4, updateMongo= updateMatchBasketMongo)

director.update({
    'basketball_matchs': BasketMatchsPage.tableCls,
    'basketball_matchs.edit': BasketMatchForm,
})

page_dc.update({
    'basketball_matchs':BasketMatchsPage ,
})
