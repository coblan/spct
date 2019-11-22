import pymongo
from django.conf import settings
import datetime
myclient = pymongo.MongoClient(settings.MONGO_SERVER)
mydb = myclient["MatchData_SA"]
spiderman = myclient["SpiderMan"]
def updateMatchMongo(dc): 
    #dc.update({
        #'CloseLiveBet': bool(dc['CloseLiveBet']),
    #})
    matchID = dc.pop('MatchID')
    match_col = mydb["Match"]
    match_col.update({'MatchID': matchID}, {'$set': dc})
    

def updateMatchBasketMongo(dc): 
    """篮球现在与足球用一张表了，这个函数无用了"""
    #dc.update({
        #'CloseLiveBet': bool(dc['CloseLiveBet']),
    #})    
    matchID = dc.pop('MatchID')
    match_col = mydb["Matches_Basketball"]
    match_col.update({'MatchID': matchID}, {'$set': dc})
    
    
beijin = datetime.timezone(datetime.timedelta(hours=8))
utc = datetime.timezone(datetime.timedelta(hours=0))

def add_tzinfo(dt):
    if not dt:
        return dt
    tmp = dt.replace(tzinfo=beijin)
    return tmp

def utc2local(dt):
    if not dt:
        return dt
    dd = dt.replace(tzinfo=utc)
    return dd.astimezone(beijin)

def tm2mongo(dt):
    if not dt:
        return dt
    tmp = dt.replace(tzinfo=beijin)
    #return tmp.astimezone(beijin)
    return tmp

def mongo2tm(dt):
    if not dt:
        return dt
    dd = dt.replace(tzinfo=utc)
    return dd.astimezone(beijin)