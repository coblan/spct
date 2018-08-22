from .member.account_admin import AccountBalanceTable,AccountTransTable,AccountTicketTable,AccountLoginTable,\
     AccoutWithdrawLimitLogTable
from .models import TbBanner, TbAccount
from .marketing.admin_help import get_mtype_options
from .marketing.gen_help_file import gen_help_file
from .marketing.gen_notice import gen_notice_file
from .marketing.gen_activity_file import gen_activity_file
from .matches.matches import get_special_bet_value,save_special_bet_value_proc
import requests
import json
from .redisInstance import redisInst
from helpers.func.random_str import get_str
import hashlib
from django.db import connections

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

def set_banner_status(rows,status):
    for row in rows:
        banner = TbBanner.objects.get(pk= row['pk'])
        banner.status = status
        banner.save()
    #redisInst.delete('App:Cache:index:banners')
    return {'status':'success'}

def modify_pswd(row): 
    "*废弃* 修改用户密码"
    account = TbAccount.objects.get(pk = row.get('pk'))
    pswd = get_str(length= 6)
    m1 =  hashlib.md5()
    m1.update(pswd.encode("utf-8"))
    pswd = m1.hexdigest()
    salt = ':69257765ACB34A08A6D0D978E9CF39ED'
    pswd_str = pswd + salt
    m2 = hashlib.md5()
    m2.update(pswd_str.encode("utf-8"))#参数必须是byte类型，否则报Unicode-objects must be encoded before 
    pswd_db_str = m2.hexdigest().upper()
    account.password = pswd_db_str
    account.save()
    

def modify_money_pswd(row): 
    "*废弃* 修改用户金融密码"
    account = TbAccount.objects.get(pk = row.get('pk'))
    pswd = get_str(length= 6)  
    m1 =  hashlib.md5()
    m1.update(pswd.encode("utf-8"))
    pswd = m1.hexdigest()
    
    salt = ':69257765ACB34A08A6D0D978E9CF39ED'
    pswd_str = pswd + salt
    m2 = hashlib.md5()
    m2.update(pswd_str.encode("utf-8"))#参数必须是byte类型，否则报Unicode-objects must be encoded before 
    pswd_db_str = m2.hexdigest().upper()
    account.fundspassword = pswd_db_str
    account.save()

def invalid_odds(row): 
    sql = 'exec [dbo].[SP_CancelTicket] %(ticketid)s,30;' % row
    cursor = connections['Sports'].cursor()
    cursor.execute(sql)
    
    




    
