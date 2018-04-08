# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Alltournamentsidcn(models.Model):
    serialnumber = models.AutoField(db_column='SerialNumber', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportId')  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CategoryId')  # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentId')  # Field name made lowercase.
    uniquetournamentid = models.IntegerField(db_column='UniqueTournamentId')  # Field name made lowercase.
    sport = models.TextField(db_column='Sport')  # Field name made lowercase.
    category = models.TextField(db_column='Category')  # Field name made lowercase.
    tournament = models.TextField(db_column='Tournament')  # Field name made lowercase.
    uniquetournamentname = models.TextField(db_column='UniqueTournamentName')  # Field name made lowercase.
    teamid = models.BigIntegerField(db_column='TeamId')  # Field name made lowercase.
    teamname = models.TextField(db_column='TeamName')  # Field name made lowercase.
    superteamid = models.BigIntegerField(db_column='SuperTeamId')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AllTournamentsIDCN'


class Alltournamentsids(models.Model):
    serialnumber = models.AutoField(db_column='SerialNumber', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportId')  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CategoryId')  # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentId')  # Field name made lowercase.
    uniquetournamentid = models.IntegerField(db_column='UniqueTournamentId')  # Field name made lowercase.
    sport = models.TextField(db_column='Sport', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    category = models.TextField(db_column='Category', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    tournament = models.TextField(db_column='Tournament', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    uniquetournamentname = models.TextField(db_column='UniqueTournamentName', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    teamid = models.BigIntegerField(db_column='TeamId')  # Field name made lowercase.
    teamname = models.TextField(db_column='TeamName', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    superteamid = models.BigIntegerField(db_column='SuperTeamId')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AllTournamentsIDs'


class Category(models.Model):
    categoryid = models.IntegerField(db_column='CategoryId', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=200)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportId')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Category'


class Competitors(models.Model):
    competitorsid = models.AutoField(db_column='CompetitorsId', primary_key=True)  # Field name made lowercase.
    id = models.BigIntegerField(db_column='ID')  # Field name made lowercase.
    superid = models.BigIntegerField(db_column='SuperID')  # Field name made lowercase.
    competitorbet = models.CharField(db_column='CompetitorBet', max_length=100)  # Field name made lowercase.
    competitorzh = models.CharField(db_column='CompetitorZh', max_length=100)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Competitors'


class LcooOdds(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.IntegerField(db_column='MatchID')  # Field name made lowercase.
    oddstype = models.IntegerField(db_column='OddsType')  # Field name made lowercase.
    oddsdata = models.CharField(db_column='OddsData', max_length=8000)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lcoo_Odds'


class LcooOddsresult(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    oddsresult = models.CharField(db_column='Oddsresult', max_length=8000)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lcoo_OddsResult'


class LcooOnmatch(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    msgnr = models.BigIntegerField(db_column='MsgNr')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    sportbet = models.CharField(db_column='SportBet', max_length=50)  # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentID')  # Field name made lowercase.
    tournamentbet = models.CharField(db_column='TournamentBet', max_length=50)  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CategoryID')  # Field name made lowercase.
    categorybet = models.CharField(db_column='CategoryBet', max_length=50)  # Field name made lowercase.
    messagetime = models.DateTimeField(db_column='MessageTime')  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='MatchDate')  # Field name made lowercase.
    fixturejs = models.TextField(db_column='FixtureJs')  # Field name made lowercase.
    oddsjs = models.TextField(db_column='OddsJs')  # Field name made lowercase.
    tournamentjs = models.TextField(db_column='TournamentJs')  # Field name made lowercase.
    sportjs = models.TextField(db_column='SportJs')  # Field name made lowercase.
    entirejs = models.TextField(db_column='EntireJs')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lcoo_OnMatch'


class LcooOnoutright(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    sportbet = models.CharField(db_column='SportBet', max_length=50)  # Field name made lowercase.
    eventinfobet = models.CharField(db_column='EventInfoBet', max_length=50)  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CategoryID')  # Field name made lowercase.
    categorybet = models.CharField(db_column='CategoryBet', max_length=50)  # Field name made lowercase.
    messagetime = models.DateTimeField(db_column='MessageTime')  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='MatchDate')  # Field name made lowercase.
    fixturejs = models.TextField(db_column='FixtureJs')  # Field name made lowercase.
    oddsjs = models.TextField(db_column='OddsJs')  # Field name made lowercase.
    sportjs = models.TextField(db_column='SportJs')  # Field name made lowercase.
    entirejs = models.TextField(db_column='EntireJs')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lcoo_OnOutRight'


class Liveoddsdata(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    jsondata = models.TextField(db_column='JsonData')  # Field name made lowercase.
    codeevent = models.CharField(db_column='CodeEvent', max_length=50)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    msgnr = models.BigIntegerField(db_column='MsgNr')  # Field name made lowercase.
    replynr = models.BigIntegerField(db_column='ReplyNr')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LiveOddsData'


class LiveoddsBetstatus(models.Model):
    tid = models.AutoField(db_column='Tid', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    betstatus = models.SmallIntegerField(db_column='BetStatus')  # Field name made lowercase.
    betstopreason = models.CharField(db_column='BetStopReason', max_length=50)  # Field name made lowercase.
    stopreasonid = models.IntegerField(db_column='StopReasonId')  # Field name made lowercase.
    stopreason = models.CharField(db_column='StopReason', max_length=50)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    score = models.CharField(max_length=10)
    redcardshome = models.IntegerField()
    redcardsaway = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'LiveOdds_BetStatus'


class Livescore(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchId')  # Field name made lowercase.
    betradarmatchid = models.BigIntegerField(db_column='BetradarMatchId')  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='MatchDate')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportId')  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CategoryId')  # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentId')  # Field name made lowercase.
    team1id = models.BigIntegerField(db_column='Team1Id')  # Field name made lowercase.
    superteam1id = models.BigIntegerField(db_column='SuperTeam1Id')  # Field name made lowercase.
    team2id = models.BigIntegerField(db_column='Team2Id')  # Field name made lowercase.
    superteam2id = models.BigIntegerField(db_column='SuperTeam2Id')  # Field name made lowercase.
    matchscore = models.CharField(db_column='MatchScore', max_length=8)  # Field name made lowercase.
    winner = models.IntegerField(db_column='Winner')  # Field name made lowercase.
    statuscode = models.IntegerField(db_column='StatusCode')  # Field name made lowercase.
    serializedata = models.TextField(db_column='SerializeData')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    generatedat = models.DateTimeField(db_column='GeneratedAt')  # Field name made lowercase.
    roundinfo = models.IntegerField(db_column='RoundInfo', blank=True, null=True)  # Field name made lowercase.
    uniquetournamentid = models.BigIntegerField(db_column='UniqueTournamentId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LiveScore'


class Livescoutsoccerevent(models.Model):
    livescoutsoccereventid = models.AutoField(db_column='LiveScoutSoccerEventId', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchId')  # Field name made lowercase.
    eventid = models.BigIntegerField(db_column='EventId')  # Field name made lowercase.
    typeid = models.IntegerField(db_column='TypeId')  # Field name made lowercase.
    scoutfeedtype = models.IntegerField(db_column='ScoutFeedType')  # Field name made lowercase.
    betstatus = models.IntegerField(db_column='BetStatus')  # Field name made lowercase.
    info = models.TextField(db_column='Info')  # Field name made lowercase.
    side = models.IntegerField(db_column='Side')  # Field name made lowercase.
    matchtime = models.CharField(db_column='MatchTime', max_length=24)  # Field name made lowercase.
    matchscore = models.CharField(db_column='MatchScore', max_length=12)  # Field name made lowercase.
    servertime = models.DateTimeField(db_column='ServerTime')  # Field name made lowercase.
    player1 = models.BigIntegerField(db_column='Player1')  # Field name made lowercase.
    player2 = models.BigIntegerField(db_column='Player2')  # Field name made lowercase.
    posx = models.IntegerField(db_column='PosX')  # Field name made lowercase.
    posy = models.IntegerField(db_column='PosY')  # Field name made lowercase.
    extrainfo = models.BigIntegerField(db_column='ExtraInfo')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LiveScoutSoccerEvent'


class LivescoutOddssuggestion(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    description = models.TextField(db_column='Description')  # Field name made lowercase.
    specialoddsvalue = models.CharField(db_column='SpecialOddsValue', max_length=500)  # Field name made lowercase.
    subtype = models.IntegerField(db_column='SubType')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    validdate = models.DateTimeField(db_column='ValidDate')  # Field name made lowercase.
    oddsvalues = models.TextField(db_column='OddsValues')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LiveScout_OddsSuggestion'


class LivescoutOnmatchupdate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    sportbet = models.CharField(db_column='SportBet', max_length=50)  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CategoryID')  # Field name made lowercase.
    categorybet = models.CharField(db_column='CategoryBet', max_length=50)  # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentID')  # Field name made lowercase.
    tournamentbet = models.CharField(db_column='TournamentBet', max_length=50)  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='MatchDate', blank=True, null=True)  # Field name made lowercase.
    matchheadjs = models.TextField(db_column='MatchHeadJs')  # Field name made lowercase.
    scouteventjs = models.TextField(db_column='ScoutEventJs')  # Field name made lowercase.
    matchupdatejs = models.TextField(db_column='MatchUpdateJs')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LiveScout_OnMatchUpdate'


class LivescoutOnmatchupdatedelta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    eventid = models.BigIntegerField(db_column='EventID')  # Field name made lowercase.
    scouteventjs = models.TextField(db_column='ScoutEventJs')  # Field name made lowercase.
    matchupdatejs = models.TextField(db_column='MatchUpdateJs')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LiveScout_OnMatchUpdateDelta'


class LivescoutOnmatchupdatedeltaupdate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    eventid = models.BigIntegerField(db_column='EventID')  # Field name made lowercase.
    scouteventjs = models.TextField(db_column='ScoutEventJs')  # Field name made lowercase.
    matchupdatejs = models.TextField(db_column='MatchUpdateJs')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LiveScout_OnMatchUpdateDeltaUpdate'


class LivescoutOnmatchupdatefull(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    matchid = models.BigIntegerField(db_column='MatchID')  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    sportbet = models.CharField(db_column='SportBet', max_length=50)  # Field name made lowercase.
    categoryid = models.BigIntegerField(db_column='CategoryID')  # Field name made lowercase.
    categorybet = models.CharField(db_column='CategoryBet', max_length=50)  # Field name made lowercase.
    tournamentid = models.IntegerField(db_column='TournamentID')  # Field name made lowercase.
    tournamentbet = models.CharField(db_column='TournamentBet', max_length=50)  # Field name made lowercase.
    matchdate = models.DateTimeField(db_column='MatchDate', blank=True, null=True)  # Field name made lowercase.
    matchheadjs = models.TextField(db_column='MatchHeadJs')  # Field name made lowercase.
    scouteventjs = models.TextField(db_column='ScoutEventJs')  # Field name made lowercase.
    matchupdatejs = models.TextField(db_column='MatchUpdateJs')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LiveScout_OnMatchUpdateFull'


class MainOddstypes(models.Model):
    oddstypesid = models.AutoField(db_column='OddsTypesId', primary_key=True)  # Field name made lowercase.
    sportid = models.IntegerField(db_column='SportID')  # Field name made lowercase.
    oddsid = models.IntegerField(db_column='OddsID')  # Field name made lowercase.
    oddskind = models.SmallIntegerField(db_column='OddsKind')  # Field name made lowercase.
    oddstypegroup = models.SmallIntegerField(db_column='OddsTypeGroup')  # Field name made lowercase.
    oddstypeid = models.IntegerField(db_column='OddsTypeID')  # Field name made lowercase.
    subtype = models.IntegerField(db_column='Subtype', blank=True, null=True)  # Field name made lowercase.
    oddstypename = models.CharField(db_column='OddsTypeName', max_length=50)  # Field name made lowercase.
    oddstypenamezh = models.CharField(db_column='OddsTypeNameZH', max_length=10)  # Field name made lowercase.
    oddsoutcome = models.CharField(db_column='OddsOutcome', max_length=20)  # Field name made lowercase.
    outcome = models.IntegerField(db_column='Outcome')  # Field name made lowercase.
    outcomedesc = models.CharField(db_column='OutcomeDesc', max_length=200)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Main_OddsTypes'


class Oddscomparison(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    bookid = models.CharField(db_column='BookID', max_length=50)  # Field name made lowercase.
    bookname = models.CharField(db_column='BookName', max_length=50)  # Field name made lowercase.
    sport = models.CharField(db_column='Sport', max_length=100)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=100)  # Field name made lowercase.
    tournamentid = models.CharField(db_column='TournamentID', max_length=50)  # Field name made lowercase.
    tournamentname = models.CharField(db_column='TournamentName', max_length=100)  # Field name made lowercase.
    matchid = models.CharField(db_column='MatchID', max_length=50)  # Field name made lowercase.
    matchdate = models.CharField(db_column='MatchDate', max_length=50)  # Field name made lowercase.
    hteam = models.CharField(db_column='HTeam', max_length=150)  # Field name made lowercase.
    ateam = models.CharField(db_column='ATeam', max_length=150)  # Field name made lowercase.
    oddstype = models.CharField(db_column='OddsType', max_length=50)  # Field name made lowercase.
    oddscontent = models.CharField(db_column='OddsContent', max_length=500)  # Field name made lowercase.
    generateat = models.CharField(db_column='GenerateAt', max_length=50)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OddsComparison'


class Players(models.Model):
    playersid = models.AutoField(db_column='PlayersId', primary_key=True)  # Field name made lowercase.
    id = models.BigIntegerField(db_column='ID')  # Field name made lowercase.
    superid = models.BigIntegerField(db_column='SuperID')  # Field name made lowercase.
    international = models.CharField(db_column='International', max_length=100)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Players'


class Sport(models.Model):
    sportid = models.IntegerField(db_column='SportID', primary_key=True)  # Field name made lowercase.
    sportname = models.CharField(db_column='SportName', max_length=200)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sport'


class TbBetstopreason(models.Model):
    reasonid = models.IntegerField(db_column='ReasonID', primary_key=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=100)  # Field name made lowercase.
    dangerousstatus = models.SmallIntegerField(db_column='DangerousStatus')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_BetStopReason'


class TbStatuscode(models.Model):
    statuscodeid = models.AutoField(db_column='StatusCodeId', primary_key=True)  # Field name made lowercase.
    sportid = models.SmallIntegerField(db_column='SportID')  # Field name made lowercase.
    statuscode = models.IntegerField(db_column='StatusCode')  # Field name made lowercase.
    livestatus = models.SmallIntegerField(db_column='LiveStatus')  # Field name made lowercase.
    text = models.CharField(db_column='Text', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TB_StatusCode'


class Tournament(models.Model):
    tournamentid = models.IntegerField(db_column='TournamentID', primary_key=True)  # Field name made lowercase.
    tournamentname = models.CharField(db_column='TournamentName', max_length=200)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tournament'
