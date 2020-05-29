from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view,SelectSearch
from ..im.im_account import ImAccountPage
from maindb.models import TbSportaccount,TbSportmoneyoutinfo
from django.utils import timezone
import time

class SbAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbSportaccount
        exclude =[]
        redraw_left_money_director = 'sb_account/redraw_left_money'
        

class SbAccountForm(ModelFields):
    class Meta:
        model = TbSportaccount
        exclude =[]
   
   
@director_view('sb_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbSportaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbSportmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TbSportmoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'sportaccount':SbAccountPage.tableCls,
    'sportaccount.edit':SbAccountForm,
})

page_dc.update({
    'sportaccount':SbAccountPage
})