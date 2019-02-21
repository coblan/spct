from helpers.director.shortcut import Fields, get_request_cache
from ..models import TbMatches, TbMatchesBasketball
from maindb.mongoInstance import updateMatchMongo
from helpers.director.model_func.dictfy import to_dict
import urllib
import requests
import json
from django.conf import settings
from django.db import IntegrityError, transaction

import logging
op_log = logging.getLogger('operation_log')

# 足球
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
            {'name': 'home_half1_score', 'label': '上半场得分', 'editor': 'com-field-linetext' ,'required':True,'fv_rule': 'integer(+0);length(~6)',},
            {'name': 'away_half1_score', 'label': '上半场得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            {'name': 'home_half2_score', 'label': '下半场得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            {'name': 'away_half2_score', 'label': '下半场得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            
            {'name': 'home_half1_corner', 'label': '半场角球', 'editor': 'com-field-linetext' ,'required':True,'fv_rule': 'integer(+0);length(~6)',},
            {'name': 'away_half1_corner', 'label': '半场角球', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            {'name': 'home_half2_corner', 'label': '下半场角球', 'editor': 'com-field-linetext' ,'required':True,'fv_rule': 'integer(+0);length(~6)',},
            {'name': 'away_half2_corner', 'label': '下半场角球', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            
            #{'name': 'home_corner', 'label': '主队角球', 'editor': 'linetext'},
            #{'name': 'away_corner', 'label': '客队角球', 'editor': 'linetext'},
            ]
    
    def manul_outcome(self, row, match): 
        #match = self.MatchModel.objects.get(matchid = row.get('matchid'))
        org_match = to_dict(match)
    
        if match.settlestatus ==3:
            raise UserWarning('比赛已经结算,请不要重复结算!')
        
        match.ishidden = True
        
        home_half1_score = int( row.get('home_half1_score') )
        away_half1_score = int( row.get('away_half1_score') )
        home_half2_score = int( row.get('home_half2_score'))
        away_half2_score = int( row.get('away_half2_score'))
        
        home_half1_corner=int( row.get('home_half1_corner') )
        away_half1_corner=int( row.get('away_half1_corner'))
        home_half2_corner=int( row.get('home_half2_corner'))
        away_half2_corner=int( row.get('away_half2_corner'))
        
        match.period1score = '%s:%s' % (home_half1_score,away_half1_score )
        match.matchscore = '%s:%s' % (home_half1_score + home_half2_score, away_half1_score + away_half2_score )
        match.homescore = home_half1_score + home_half2_score
        match.awayscore = away_half1_score + away_half2_score 
        
        match.period1cornerkicks='%s:%s'%(home_half1_corner,away_half1_corner)
        match.cornerkicks = '%s:%s'%(home_half1_corner+away_half1_corner,away_half1_corner+away_half2_corner)
        match.statuscode = 100
        match.settlestatus =3
        
        if row.get('home_score') > row.get('away_score'):
            match.winner = 1
        elif row.get('home_score') < row.get('away_score'):
            match.winner = 2
        else:
            match.winner = 3        
        
        #crt_settlestatus = 0 if not match.settlestatus else match.settlestatus
        #settlestatus = crt_settlestatus
        #if crt_settlestatus < 1 and row.get('home_half_score', '') != '' and row.get('away_half_score', '') != '':
            #match.period1score = '%s:%s' % (row.get('home_half_score'), row.get('away_half_score'))
            #match.statuscode = self.half_end_code
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
            
        match.save()
        try:
            self.notfiy_service(row)
        except UserWarning as e:
            for k in org_match:
                if not k.startswith('_'):
                    setattr(match, k, org_match[k])
                match.save()
            op_log.info('手动结算足球比赛%(matchid)s的%(type)s，未成功,错误消息:%(msg)s' % {'matchid': match.matchid, 
                                                                                        'type': settle_dict.get(match.settlestatus),
                                                                                        'msg': str(e),
                                                                                        })
            raise e
        #self.update_mongo(match)

        op_log.info('手动结算%(matchtype)s比赛%(matchid)s，结算后比分为:上半场:%(period1score)s,全场:%(matchscore)s' % {'matchid': match.matchid, 
                                                         'matchtype': self.matchtype,
                                                         #'type': settle_dict.get(match.settlestatus),
                                                         'period1score': match.period1score,
                                                         'matchscore': match.matchscore,})
        #rt_dc['row'] = to_dict(match)
    
    def notfiy_service(self, row): 
        catch = get_request_cache()
        data = {
            'SportID': self.sportid, 
            'MatchID': row.get('matchid'),
            'PeriodType': row.get('PeriodType',2),
            'OrderBack': False,
        }
        url = urllib.parse.urljoin( settings.CENTER_SERVICE, '/Match/ManualResulting')
        rt = requests.post(url,json=data)
        rt_dc = json.loads( rt.text )
        if not rt_dc.get('Success'):   
            raise UserWarning( rt_dc.get('Message', '手动结算后端发生问题'))
        catch['msg'].append(rt_dc.get('Message'))

        
class NumberOfCorner(FootBallPoints):
    #2  全场半场 角球
    def get_heads(self): 
        return [
            #{'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
            {'name': 'home_half_score', 'label': '半场角球数', 'editor': 'com-field-linetext' ,'fv_rule': 'integer(+0);length(~6)',},
            {'name': 'away_half_score', 'label': '半场角球数', 'editor': 'com-field-linetext','fv_rule': 'integer(+0);length(~6)'},
            
            {'name': 'home_score', 'label': '全场角球数', 'editor': 'com-field-linetext','fv_rule': 'integer(+0);length(~6)'},
            {'name': 'away_score', 'label': '全场角球数', 'editor': 'com-field-linetext','fv_rule': 'integer(+0);length(~6)'},
            
            ]    


# 篮球
#--------------------------------------

class BasketPoints(FootBallPoints):
    sportid = 1
    MatchModel = TbMatchesBasketball
    matchtype = '篮球'
    half_end_code = 4
    
    def get_heads(self): 
        return [
            #{'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
            {'name': 'home_1_score', 'label': '一小节得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)',},
            {'name': 'away_1_score', 'label': '一小节得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            {'name': 'home_2_score', 'label': '二小节得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)',},
            {'name': 'away_2_score', 'label': '二小节得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            {'name': 'home_3_score', 'label': '三小节得分', 'editor': 'com-field-linetext' ,'required':True,'fv_rule': 'integer(+0);length(~6)',},
            {'name': 'away_3_score', 'label': '三小节得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            {'name': 'home_4_score', 'label': '四小节得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            {'name': 'away_4_score', 'label': '四小节得分', 'editor': 'com-field-linetext','required':True,'fv_rule': 'integer(+0);length(~6)'},
            {'name': 'home_5_score', 'label': '加时赛得分', 'editor': 'com-field-linetext','fv_rule': 'integer(+0);length(~6)'},
            {'name': 'away_5_score', 'label': '加时赛得分', 'editor': 'com-field-linetext','fv_rule': 'integer(+0);length(~6)'},
            ]     
    
    def manul_outcome(self, row, match): 
        #match = self.MatchModel.objects.get(matchid = row.get('matchid'))
        if match.settlestatus ==3: # and match.settlestatus >= 1:
            raise UserWarning('篮球赛已经结算,请不要重复结算!')   
        
        #org_match = to_dict(match)
        try:
            with transaction.atomic():
                match.ishidden = True
                home_half_score= row.get('home_1_score')+row.get('home_2_score')
                away_half_score= row.get('away_1_score')+row.get('away_2_score')
                homescore = int( row.get('home_1_score') )+int( row.get('home_2_score') )+ int( row.get('home_3_score') )+int( row.get('home_4_score') )+ int( row.get('home_5_score',0))
                awayscore = int( row.get('away_1_score') )+int( row.get('away_2_score') ) + int( row.get('away_3_score') )+int( row.get('away_4_score') )+int( row.get('away_5_score',0))
                
                match.q1score='%s:%s'%(row.get('home_1_score'),row.get('away_1_score'))
                match.q2score='%s:%s'%(row.get('home_2_score'),row.get('away_2_score'))
                match.q3score='%s:%s'%(row.get('home_3_score'),row.get('away_3_score'))
                match.q4score='%s:%s'%(row.get('home_4_score'),row.get('away_4_score'))
                match.overtimescore='%s:%s'%(row.get('home_5_score',0),row.get('away_5_score',0))
                
                match.homescore = homescore
                match.awayscore = awayscore
                match.period1score = '%s:%s'%(home_half_score,away_half_score)
                match.matchscore = '%s:%s' % (match.homescore, match.awayscore)
                match.settlestatus = 1
                match.statuscode = 100
                match.save()
                row['PeriodType'] = 2      
                self.notfiy_service(row)
        except UserWarning as e:
            #for k in org_match:
                #if not k.startswith('_'):
                    #setattr(match, k, org_match[k])
                #match.save()
            op_log.info('手动结算篮球比赛%(matchid)s，未成功,错误消息:%(msg)s' % {'matchid': match.matchid, 
                                                                                        #'type': settle_dict.get(match.settlestatus),
                                                                                        'msg': str(e),
                                                                                                })
            raise e
        op_log.info('手动结算%(matchtype)s比赛%(matchid)s,最终比分%(matchscore)s' % {'matchid': match.matchid, 
                                                         'matchtype': self.matchtype,
                                                         'matchscore': match.matchscore,})       
    
    

class Quarter(BasketPoints):
    # 170  单结比分
    def get_heads(self): 
        return [
            {'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
            {'name': 'home_score', 'label': '主队得分','editor': 'com-field-linetext','required': True,'fv_rule': 'integer(+0);length(~6)',}, 
            {'name': 'away_score', 'label': '客队得分','editor': 'com-field-linetext','required': True,'fv_rule': 'integer(+0);length(~6)',}, 
        ]
    
    def manul_outcome(self, row, match): 
        #match = self.MatchModel.objects.get(matchid = row.get('matchid'))
        if match.settlestatus and match.settlestatus >= 1:
            raise UserWarning('单节比分已经结算,请不要重复结算!')    
        
        self.org_match = to_dict(match)
        
        match.ishidden = True
        match.homescore = row.get('home_score')
        match.awayscore = row.get('away_score')
        match.period1score = ''
        match.matchscore = '%s:%s' % (match.homescore, match.awayscore)
        match.settlestatus = 1
        match.statuscode = 100
        match.save()
        
        row['PeriodType'] = 0
        try:
            self.notfiy_service(row)
        except UserWarning as e:
            for k in org_match:
                if not k.startswith('_'):
                    setattr(match, k, org_match[k])
                match.save()
            op_log.info('手动结算篮球比赛%(matchid)s的%(type)s，未成功,错误消息:%(msg)s' % {'matchid': match.matchid, 
                                                                                        'type': settle_dict.get(match.settlestatus),
                                                                                        'msg': str(e),
                                                                                                })
            raise e
        op_log.info('手动结算%(matchtype)s比赛%(matchid)s,最终比分%(matchscore)s' % {'matchid': match.matchid, 
                                                         'matchtype': self.matchtype,
                                                         'matchscore': match.matchscore,})    

class FirstBasket(BasketPoints):
    #171 最先得分  主队，客队  "1:0" "0:1"  homeScore  awayScore
    def get_heads(self): 
        return [
            {'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
            {'name': 'matchscore', 'label': '先得分球队','editor': 'com-field-select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                ],'required': True,}
        ]
    
    def manul_outcome(self, row, match): 
        #match = self.MatchModel.objects.get(matchid = row.get('matchid'))
        if match.settlestatus and match.settlestatus >= 1:
            raise UserWarning('已经结算,请不要重复结算!')    
        
        self.org_match = to_dict(match)
        
        match.ishidden = True
        match.period1score = ''
        match.settlestatus = 1
        match.statuscode = 100
        match.save()
        
        row['PeriodType'] = 0
        try:
            self.notfiy_service(row)
        except UserWarning as e:
            for k in org_match:
                if not k.startswith('_'):
                    setattr(match, k, org_match[k])
                match.save()
            op_log.info('手动结算篮球比赛%(matchid)s的%(type)s，未成功,错误消息:%(msg)s' % {'matchid': match.matchid, 
                                                                                        'type': settle_dict.get(match.settlestatus),
                                                                                        'msg': str(e),
                                                                                                })
            raise e
        op_log.info('手动结算%(matchtype)s比赛%(matchid)s,最终比分%(matchscore)s' % {'matchid': match.matchid, 
                                                         'matchtype': self.matchtype,
                                                         'matchscore': match.matchscore,})       
    
class LastBasket(FirstBasket):
    #172 最后得分 主队，客队  "1:0" "0:1"
    def get_heads(self): 
        return [
            {'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
            {'name': 'matchscore', 'label': '最后得分球队','editor': 'com-field-select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                ],'required': True,}
        ]

class HightestQuarterScore(FirstBasket):
    #174  最高单节得分
    def get_heads(self): 
        return [
            {'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
           {'name': 'matchscore', 'label': '最高单节<br>得分球队','editor': 'com-field-select','options': [
               {'value': '1:0', 'label': '主队',}, 
               {'value': '0:1', 'label': '客队',}, 
               ],'required': True,}
        ]

class TotalPoints(Quarter):
    #175   主队多少分，客队多少分   matchscore
    pass

class Shot3Points(Quarter):
    #176 三分球 主队 客队 分别填写
    def get_heads(self):
        return [
            {'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
            {'name': 'home_score', 'label': '主队三分球','editor': 'com-field-linetext','required': True,'fv_rule': 'integer(+0);length(~6)',}, 
            {'name': 'away_score', 'label': '客队三分球','editor': 'com-field-linetext','required': True,'fv_rule': 'integer(+0);length(~6)',}, 
        ]
    

class FirstReachScore(FirstBasket):
    # 185  谁先得多少分
    def get_heads(self): 
        return [
            {'name': 'matchid', 'label': '比赛', 'editor': 'com-field-label-shower', 'readonly': True},
            {'name': 'matchscore', 'label': '球队先得X分','editor': 'com-field-select','options': [
                {'value': '1:0', 'label': '主队',}, 
                {'value': '0:1', 'label': '客队',}, 
                {'value': '0:0', 'label': '都不',}
                ],'required': True,}
        ]

