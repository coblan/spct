from helpers.director.shortcut import Fields, get_request_cache
from ..models import TbMatches
from maindb.mongoInstance import updateMatchMongo
from helpers.director.model_func.dictfy import to_dict
import urllib
import requests
import json
from django.conf import settings


import logging
op_log = logging.getLogger('operation_log')

# 足球,篮球
#--------------------------------
class FootBallPoints(Fields):
    # 0 全场半场比分
    MatchModel = TbMatches
    sportid = 0
    matchtype = '足球'
    half_end_code = 31
    def get_heads(self): 
        return [
            #{'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
            {'name': 'home_half_score', 'label': '半场得分', 'editor': 'com-field-linetext' ,'fv_rule': 'integer(+0);length(~6)',},
            {'name': 'away_half_score', 'label': '半场得分', 'editor': 'com-field-linetext','fv_rule': 'integer(+0);length(~6)'},
            
            {'name': 'home_score', 'label': '全场得分', 'editor': 'com-field-linetext','fv_rule': 'integer(+0);length(~6)'},
            {'name': 'away_score', 'label': '全场得分', 'editor': 'com-field-linetext','fv_rule': 'integer(+0);length(~6)'},
            
            #{'name': 'home_corner', 'label': '主队角球', 'editor': 'linetext'},
            #{'name': 'away_corner', 'label': '客队角球', 'editor': 'linetext'},
            ]
    
    def manul_outcome(self, row): 
        match = self.MatchModel.objects.get(matchid = row.get('matchid'))
        self.org_match = to_dict(match)
        
        match.ishidden = True
        crt_settlestatus = 0 if not match.settlestatus else match.settlestatus
        settlestatus = crt_settlestatus
        if crt_settlestatus < 1 and row.get('home_half_score', '') != '' and row.get('away_half_score', '') != '':
            match.period1score = '%s:%s' % (row.get('home_half_score'), row.get('away_half_score'))
            match.statuscode = self.half_end_code
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
            
        
        match.save()
        
        rt_dc = self.notfiy_service(row)
        #self.update_mongo(match)

        op_log.info('手动结算%(matchtype)s比赛%(matchid)s的%(type)s，结算后比分为:上半场:%(period1score)s,全场:%(matchscore)s' % {'matchid': match.matchid, 
                                                         'matchtype': self.matchtype,
                                                         'type': settle_dict.get(match.settlestatus),
                                                         'period1score': match.period1score,
                                                         'matchscore': match.matchscore,})
        #rt_dc['row'] = to_dict(match)
    
    def notfiy_service(self, row): 
        catch = get_request_cache()
        data = {
            'SportID': self.sportid, 
            'MatchID': row.get('matchid'),
            'PeriodType': row.get('PeriodType'),
            'OrderBack': False,
        }
        url = urllib.parse.urljoin( settings.CENTER_SERVICE, '/Match/ManualResulting')
        rt = requests.post(url,json=data)
        rt_dc = json.loads( rt.text )
        if not rt_dc.get('Success'):
            for k in self.org_match:
                if not k.startswith('_'):
                    setattr(match, k, self.org_match[k])
                match.save()
            op_log.info('手动结算足球比赛%(matchid)s的%(type)s，未成功,错误消息:%(msg)s' % {'matchid': match.matchid, 
                                                             'type': settle_dict.get(match.settlestatus),
                                                            'msg': rt_dc.get('Message',''),})
                
            raise UserWarning( rt_dc.get('Message', '手动结算后端发生问题'))
        catch['msg'].append(rt_dc.get('Message'))

        
    #def update_mongo(self, match): 
        #dc = {
            #'MatchID': match.matchid,
            #'IsRecommend': match.isrecommend,
            #'IsHidden': match.ishidden,
            #'CloseLiveBet': match.closelivebet, 
            #'Team1ZH': match.team1zh,
            #'Team2ZH': match.team2zh,
            #'StatusCode': match.statuscode,
            #'Period1Score': match.period1score,
            #'MatchScore': match.matchscore,
            #'Winner': match.winner,
        #}
        #updateMatchMongo(dc)
        
        

# 足球
#--------------------------------
class NumberOfCorner(Fields):
    #2  全场半场
    def get_heads(self): 
        return [

            {'name': 'matchscore', 'label': '球队先得<br>多少分','editor': 'sim_select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                {'value': '0:0', 'label': '都不',}
                ],'required': True,}
        ]

# 篮球
#--------------------------------------

class Basket

class Quarter(Fields):
    # 170  单结比分
    def get_heads(self): 
        return [

            {'name': 'matchscore', 'label': '球队先得<br>多少分','editor': 'sim_select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                {'value': '0:0', 'label': '都不',}
                ],'required': True,}
        ]

class FirstBasket(Fields):
    #171 最先得分  主队，客队  "1:0" "0:1"  homeScore  awayScore
    def get_heads(self): 
        return [

            {'name': 'matchscore', 'label': '球队先得<br>多少分','editor': 'sim_select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                {'value': '0:0', 'label': '都不',}
                ],'required': True,}
        ]
class LastBasket(Fields):
    #172 最后得分 主队，客队  "1:0" "0:1"
    def get_heads(self): 
        return [

            {'name': 'matchscore', 'label': '球队先得<br>多少分','editor': 'sim_select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                {'value': '0:0', 'label': '都不',}
                ],'required': True,}
        ]

class HightestQuarterScore(Fields):
    #174  最高单结得分
    pass

class TotalPoints(Fields):
    #175   主队多少分，客队多少分   matchscore
    def get_heads(self): 
        return [

            {'name': 'matchscore', 'label': '球队先得<br>多少分','editor': 'sim_select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                {'value': '0:0', 'label': '都不',}
                ],'required': True,}
        ]

class Shot3Points(Fields):
    #176 三分球 主队 客队 分别填写
    pass

class FirstScore(Fields):
    # 185  谁先得多少分
    def get_heads(self): 
        return [
            {'name': 'matchscore', 'label': '球队先得<br>多少分','editor': 'sim_select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                {'value': '0:0', 'label': '都不',}
                ],'required': True,}
        ]

