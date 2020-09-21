from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view
from ..im.im_account import ImAccountPage
from maindb.models import TbPtaccount,TbPtmoneyoutinfo
from django.utils import timezone
import time

class PtAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbPtaccount
        exclude =[]
        redraw_left_money_director = 'pt_account/redraw_left_money'

class PtAccountForm(ModelFields):
    class Meta:
        model = TbPtaccount
        exclude =[]
   
   
@director_view('pt_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbPtaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbPtmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TbPtmoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'pt_account':PtAccountPage.tableCls,
    'pt_account.edit':PtAccountForm,
})

page_dc.update({
    'pt_account':PtAccountPage
})