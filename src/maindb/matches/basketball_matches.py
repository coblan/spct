from helpers.director.shortcut import page_dc, director, director_view,director_element
from .matches import MatchsPage, MatchForm ,quit_ticket,PeriodScoreTab#get_special_bet_value, produce_match_outcome, save_special_bet_value_proc, 
from ..models import TbMatch,TbTournament,TbPeriodscore
from maindb.mongoInstance import updateMatchBasketMongo
#from .match_outcome_forms import  BasketPoints, Quarter, FirstBasket, LastBasket, HightestQuarterScore, FirstReachScore, TotalPoints, Shot3Points,BasketTwosection
from ..redisInstance import redisInst
import datetime
from .matches import OutcomeTab
from helpers.director.access.permit import can_touch,has_permit

class BasketMatchsPage(MatchsPage):
    
    def get_context(self):
        ctx = super().get_context()
        #ctx['extra_table_logic'] = 'match_logic'
        ls = [
       
        ]
        ctx['named_ctx'] = {
            'match_closelivebet_tabs': ls,
        }
        
        match_form = BasketMatchForm(crt_user=self.crt_user)
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
                 'visible': can_touch(TbPeriodscore, self.crt_user), 
             },
            {'name': 'special_bet_value',
             'label': '封盘',
             'com': 'com-tab-special-bet-value',
             'update_director': 'get_special_bet_value',
             'save_director': 'save_special_bet_value',
             'ops': [
                 {'fun': 'save', 'label': '保存', 'editor': 'com-op-plain-btn', 'icon': 'fa-save','class':'btn-primary' },
                 {'fun': 'refresh', 'label': '刷新', 'editor': 'com-op-plain-btn', 'icon': 'fa-refresh', }, 
                 {'fun':'filter_name','label':'玩法过滤','editor':'com-op-search',
                  'icon':'fa-refresh','btn_text':False},
             ],
             'visible': has_permit(self.crt_user, 'manual_specialbetvalue'), 
            }, {
                'name':'manul_outcome',
                'label':'手动结算',
                'com':'com-tab-table',
                'par_field': 'matchid',
                'table_ctx': BasketOutcome(crt_user=self.crt_user).get_head_context(),
                'visible': has_permit(self.crt_user, 'manual_outcome'), 
            },
                  
        ]
        
        ctx['named_ctx'] = {
            #'match_closelivebet_tabs': ls,
            'match_tabs':match_tabs,
                    }
        return ctx
    
    class tableCls(MatchsPage.tableCls):
        sportid = 2
        model = TbMatch
 
        class filters(MatchsPage.tableCls.filters):
            def dict_head(self, head):
                #head = super().dict_head(head)
                
                if head['name']=='statuscode':
                    head['options']=list( filter(lambda x:x['value'] in [0,13,14,15,16,31,32,40,100,110],head['options']) )
                if head['name'] == 'tournamentid':
                    head['options']=[
                        {'value':x.tournamentid,'label':str(x)} for x in TbTournament.objects.filter(sportid=2)                    
                    ]
                return head
            

class BasketMatchForm(MatchForm):
          
    def save_form(self):
        msg = []
        #if self.kw.get('meta_type') == 'manul_outcome':
            ##specialcategoryid = self.kw.get('specialcategoryid')
            ##ProcCls = self.proc_map.get(specialcategoryid)
            #if self.kw.get('tournamentid')==698:
                #ProcCls=BasketTwosection
            #else:
                #ProcCls=BasketPoints
            #proc_obj = ProcCls(crt_user = self.crt_user)
            #self.instance.settletime = datetime.datetime.now()
            #rt_msg =  proc_obj.manul_outcome( self.kw, self.instance)
            #msg.append(rt_msg)
        #else:
        super().save_form()
            
        self.updateMongo()
        self.proc_redis()
        return {'msg': msg,}  
   
@director_element('basketball.manul_outcome')
class BasketOutcome(OutcomeTab):
    def inn_filter(self, query):
        # 291 是篮球的
        return query.filter(enabled=True,marketid__in = [291])
    
    def get_rows(self):
        if self.kw.get('matchid'):
            match = TbMatch.objects.get(matchid = self.kw.get('matchid'))
            if match.tournamentid == 698:
                bf = [
                    {'marketid':'','pk':-3,'marketname':'score','marketnamezh':'比分型'}
                ]
            else:
                bf = [
                    {'marketid':'','pk':-2,'marketname':'score','marketnamezh':'比分型'}
                ]
        rows = super(OutcomeTab,self).get_rows()
        return bf+rows


director.update({
    'basketball_matchs': BasketMatchsPage.tableCls,
    'basketball_matchs.edit': BasketMatchForm,
})

page_dc.update({
    'basketball_matchs':BasketMatchsPage ,
})
