import pymongo
from django.conf import settings

myclient = pymongo.MongoClient(settings.MONGO_SERVER)
mydb = myclient["MatchData_SA"]

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