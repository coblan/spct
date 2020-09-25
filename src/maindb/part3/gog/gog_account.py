from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view
from ..im.im_account import ImAccountPage
from maindb.models import TbGrmoneyoutinfo,TbGraccount
from django.utils import timezone
import time

class GogAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbGraccount
        exclude =[]
        redraw_left_money_director = 'gog_account/redraw_left_money'

class GogAccountForm(ModelFields):
    class Meta:
        model = TbGraccount
        exclude =[]
   
   
@director_view('gog_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbGraccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbGrmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TbGrmoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'gog_account':GogAccountPage.tableCls,
    'gog_account.edit':GogAccountForm,
})

page_dc.update({
    'gog_account':GogAccountPage
})