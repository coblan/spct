from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view
from maindb.im.im_account import ImAccountPage
from maindb.models import TbImchessaccount,TBIMChessMoneyOutInfo
from django.utils import timezone
import time

class IMchessAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbImchessaccount
        exclude =[]
        redraw_left_money_director = 'imchess_account/redraw_left_money'

class ImChessAccountForm(ModelFields):
    class Meta:
        model = TbImchessaccount
        exclude =[]
   
   
@director_view('imchess_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbImchessaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TBIMChessMoneyOutInfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TBIMChessMoneyOutInfo.objects.bulk_create(out_list)
    
   
director.update({
    'imchess_account':IMchessAccountPage.tableCls,
    'imchess_account.edit':ImChessAccountForm,
})

page_dc.update({
    'imchess_account':IMchessAccountPage
})