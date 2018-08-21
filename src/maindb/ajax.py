from .account_admin import AccountBalanceTable,AccountTransTable,AccountTicketTable,AccountLoginTable,\
     AccoutWithdrawLimitLogTable
from .models import TbBanner
from .marketing.admin_help import get_mtype_options
from .marketing.gen_help_file import gen_help_file
from .marketing.gen_notice import gen_notice_file
from .marketing.gen_activity_file import gen_activity_file
from .admin_games.matches import get_special_bet_value,save_special_bet_value_proc
import requests
import json
from .redisInstance import redisInst

def get_global():
    return globals()

def get_help_options():
    return get_mtype_options()

def update_help_file():
    gen_help_file()
    return {'status':'success'}

def update_notice_file():
    gen_notice_file()
    #redisInst.delete('App:Cache:index:notices')
    
    return {'status':'success'}

def produce_match_outcome(row):
    """
    手动结算
    """
    #url = 'http://192.168.40.103:9001/Match/ManualResulting'
    url = 'http://192.168.40.103:9022/Match/ManualResulting'
    data ={
        'MatchID':row.get('matchid'),
        'Team1Score':row.get('home_score', 0),
        'Team2Score':row.get('away_score', 0),
        'Team1HalfScore':row.get('home_half_score', 0),
        'Team2HalfScore':row.get('away_half_score', 0),        
        'Team1Corner':row.get('home_corner', 0),
        'Team2Corner':row.get('away_corner', 0),
        'Terminator': 'adminSys',
        'PeriodType': 2,
        
    }    
    
    rt = requests.post(url,data=data)
    #print(rt.text)
    return json.loads( rt.text )
    
def update_activity_file():
    gen_activity_file()
    return {'status':'success'}


def update_special_bet_value(matchid):
    return get_special_bet_value(matchid)

def save_special_bet_value(matchid, match_opened,oddstype,specialbetvalue):
    return save_special_bet_value_proc(matchid,match_opened, oddstype,
                                       specialbetvalue)


#def get_balance_log(account_pk,user,searchargs={}):
    #dc={'account_pk':account_pk}
    #dc.update(searchargs)
    #actable = AccountBalanceTable.gen_from_search_args(dc, user)
    #return actable.get_data_context()

#def get_account_trans(account_pk,user,searchargs={}):
    #dc={'account_pk':account_pk}
    #dc.update(searchargs)
    #actable = AccountTransTable.gen_from_search_args(dc, user)
    ##(pk=account_pk,row_filter=searchargs,crt_user=user)
    #return actable.get_data_context()


#def get_account_ticket(account_pk,user,searchargs={}):
    #dc={'account_pk':account_pk}
    #dc.update(searchargs)
    #actable = AccountTicketTable.gen_from_search_args(dc, user)
    ##(pk=account_pk,row_filter=searchargs,crt_user=user)
    #return actable.get_data_context()

#def get_account_login(account_pk,user,searchargs={}):
    #dc={'account_pk':account_pk}
    #dc.update(searchargs)
    #actable = AccountLoginTable.gen_from_search_args(dc, user)
    ##(pk=account_pk,row_filter=searchargs,crt_user=user)
    #return actable.get_data_context()

#def get_account_withdrawlimitlog(account_pk,user,searchargs={}):
    #dc={'account_pk':account_pk}
    #dc.update(searchargs)
    #actable = AccoutWithdrawLimitLogTable.gen_from_search_args(dc, user)
    ##(pk=account_pk,row_filter=searchargs,crt_user=user)
    #return actable.get_data_context()

#def get_account_tokencode(account_pk,user,searchargs={}):
    #dc={'account_pk':account_pk}
    #dc.update(searchargs)
    #actable = AccountTokenCodeTable.gen_from_search_args(dc, user)
    ##(pk=account_pk,row_filter=searchargs,crt_user=user)
    #return actable.get_data_context()

def set_banner_status(rows,status):
    for row in rows:
        banner = TbBanner.objects.get(pk= row['pk'])
        banner.status = status
        banner.save()
    #redisInst.delete('App:Cache:index:banners')
    return {'status':'success'}
