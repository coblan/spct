import pymongo
from django.conf import settings

myclient = pymongo.MongoClient(settings.MONGO_SERVER)
mydb = myclient["MatchData_SA"]

def updateMatchMongo(dc): 
    matchID = dc.pop('MatchID')
    match_col = mydb["Matches"]
    match_col.update({'MatchID': matchID}, {'$set': dc})
    

def updateMatchBasketMongo(dc): 
    matchID = dc.pop('MatchID')
    match_col = mydb["Matches_Basketball"]
    match_col.update({'MatchID': matchID}, {'$set': dc})