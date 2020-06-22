from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view
from maindb.im.im_account import ImAccountPage
from maindb.models import TbPpaccount,TbPpmoneyoutinfo
from django.utils import timezone
import time

class PPAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbPpaccount
        exclude =[]
        redraw_left_money_director = 'pp_account/redraw_left_money'

class PPAccountForm(ModelFields):
    class Meta:
        model = TbPpaccount
        exclude =[]
   
   
@director_view('pp_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbPpaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbPpmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TbPpmoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'pp_account':PPAccountPage.tableCls,
    'pp_account.edit':PPAccountForm,
})

page_dc.update({
    'pp_account':PPAccountPage
})