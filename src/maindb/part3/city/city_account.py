from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view,SelectSearch
from ..im.im_account import ImAccountPage
from maindb.models import TbLcityaccount,TbLcitymoneyoutinfo
from django.utils import timezone
import time

class LcityAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbLcityaccount
        exclude =[]
        redraw_left_money_director = 'lcity_account/redraw_left_money'
        

class LcityAccountForm(ModelFields):
    class Meta:
        model = TbLcityaccount
        exclude =[]
   
   
@director_view('lcity_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbLcityaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbLcitymoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TbLcitymoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'lcityaccount':LcityAccountPage.tableCls,
    'lcityaccount.edit':LcityAccountForm,
})

page_dc.update({
    'lcityaccount':LcityAccountPage
})