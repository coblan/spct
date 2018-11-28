from helpers.director.shortcut import page_dc, director, director_view
from .matches import MatchsPage, MatchForm, PeriodTypeForm, get_special_bet_value, produce_match_outcome, save_special_bet_value_proc, quit_ticket
from ..models import TbMatchesBasketball, TbOddsBasketball

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
                     'ops': [{"fun": 'produce_match_outcome', 'label': '保存', 'editor': 'com-field-op-btn', }, ],
                     'produce_match_outcome_director': 'basketball_produce_match_outcome                     me',
                     
                    #'option': {
                           #'ops': [{"fun": 'produce_match_outcome', 'label': '保存', 'editor': 'com-field-op-btn', }, ],
                           #'produce_match_outcome_director': 'basketball_produce_match_outcome',
                        #},
                     #'form': 'com-form-produceMatchOutcomePanel',
                     
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
                  'director_name': 'basketball_quit_ticket',
                  'label': '退单', 'confirm_msg': '确认要退单吗？', 'row_match': 'one_row',
                  'pre_set': 'rt={PeriodType:2}',
                  #'after_save': 'rt=cfg.showMsg(scope.new_row.Message)',
                 'fields_ctx': PeriodTypeForm_form.get_head_context(),
                 'visible': 'ishidden' in self.permit.changeable_fields()},

            ]
            return ops


class BasketMatchForm(MatchForm):
    class Meta:
        model = TbMatchesBasketball
        exclude = ['marketstatus']
    
    def proc_redis(self): 
        if 'closelivebet' in self.changed_data:
            if self.instance.closelivebet == 0:
                redisInst.delete('Backend:Basketball:match:closelivebet:%(matchid)s' % {'matchid': self.instance.eventid})
            else:
                redisInst.set('Backend:Basketball:match:closelivebet:%(matchid)s' % {'matchid': self.instance.eventid}, 1,
                              60 * 1000 * 60 * 24 * 7)    


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
    return produce_match_outcome(row, MatchModel = TbMatchesBasketball, sportid = 1)

director.update({
    'basketball_matchs': BasketMatchsPage.tableCls,
    'basketball_matchs.edit': BasketMatchForm,
})

page_dc.update({
    'basketball_matchs':BasketMatchsPage ,
})
