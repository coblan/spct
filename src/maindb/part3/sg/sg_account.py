from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view
from ..im.im_account import ImAccountPage
from maindb.models import TbSgaccount,TbSgmoneyoutinfo
from django.utils import timezone
import time

class SgAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbSgaccount
        exclude =[]
        redraw_left_money_director = 'sg_account/redraw_left_money'

class SgAccountForm(ModelFields):
    class Meta:
        model = TbSgaccount
        exclude =[]
   
   
@director_view('sg_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbSgaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbSgmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TbSgmoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'sg_account':SgAccountPage.tableCls,
    'sg_account.edit':SgAccountForm,
})

page_dc.update({
    'sg_account':SgAccountPage
})