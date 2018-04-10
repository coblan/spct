from account_admin import AccountBalanceTable,AccountTransTable,AccountTicketTable,AccountLoginTable,\
     AccoutWithdrawLimitLogTable,AccountTokenCodeTable
from .models import TbBanner

def get_global():
    return globals()

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
    return {'status':'success'}
