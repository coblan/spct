# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import director
from helpers.director.models import PermitModel
from django.conf import settings
import os
import sqlite3
from django.contrib.auth.models import Group,User
from django.db import connection
from helpers.director.models import KVModel,PermitModel
from maindb.models import TbTeammapping,TbMatch
from maindb.mongoInstance import mydb

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        
        matchid_list =[]
        match_dc ={}
        for item in mydb['ThirdPartEvent'].find({'MatchID':{'$ne':None}}):
            matchid_list.append(item.get('MatchID'))
        
        count = 1
        for batch_match_list in get_matchlist(matchid_list):
            print('查询 %s批 matchid'%count)
            count += 1
            for match in TbMatch.objects.filter(matchid__in=batch_match_list):
                match_dc[match.matchid] = match
            
        team_dc ={}
        for item in mydb['ThirdPartEvent'].find({'MatchID':{'$ne':None}}):
            match = match_dc.get(item.get('MatchID'))
            if not item.get('TeamSwap'):
                # 现在的外部球队来源都是 188 所以source都是2 ，
                # 注意item.get('Source') 是比赛来源，不要搞混了
                home={
                    'sourceteamnameen':item.get('Team1En'),
                    'sourceteamnamezh':item.get('Team1Zh'),
                    'teamnameen':match.team1en,
                    'teamnamezh':match.team1zh,
                    'teamid':match.team1id,
                    'sportid':item.get('SportId'),
                    'source':2,
                }
                away={
                    'sourceteamnameen':item.get('Team2En'),
                    'sourceteamnamezh':item.get('Team2Zh'),
                    'teamnameen':match.team2en,
                    'teamnamezh':match.team2zh,
                    'teamid':match.team2id,
                    'sportid':item.get('SportId'),
                    'source':2,
                }
            else:
                home={
                    'sourceteamnameen':item.get('Team2En'),
                    'sourceteamnamezh':item.get('Team2Zh'),
                    'teamnameen':match.team2en,
                    'teamnamezh':match.team2zh,
                    'teamid':match.team2id,
                    'sportid':item.get('SportId'),
                    'source':2,
                }
                away={
                    'sourceteamnameen':item.get('Team1En'),
                    'sourceteamnamezh':item.get('Team1Zh'),
                    'teamnameen':match.team1en,
                    'teamnamezh':match.team1zh,
                    'teamid':match.team1id,
                    'sportid':item.get('SportId'),
                    'source':2,
                }
            key1 = '%(sportid)s_%(source)s_%(sourceteamnameen)s_%(sourceteamnamezh)s'%home
            key2 = '%(sportid)s_%(source)s_%(sourceteamnameen)s_%(sourceteamnamezh)s'%away
            team_dc[key1] = home
            team_dc[key2] = away
            
        TbTeammapping.objects.all().delete() 
        rows =[]
        for k,v in team_dc.items():  
            rows.append(TbTeammapping(mappingkey=k,**v))
        TbTeammapping.objects.bulk_create(rows)
        

def get_matchlist(matchlist):
    rows =[]
    for matchid in matchlist:
        rows.append(matchid)
        if len(rows) > 1000:
            yield rows
            rows =[]
            