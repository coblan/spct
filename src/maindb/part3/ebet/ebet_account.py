from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view
from ..im.im_account import ImAccountPage
from maindb.models import TbEbaccount,TbEbmoneyoutinfo
from django.utils import timezone
import time

class EbAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbEbaccount
        exclude =[]
        redraw_left_money_director = 'eb_account/redraw_left_money'

class EbAccountForm(ModelFields):
    class Meta:
        model = TbEbaccount
        exclude =[]
   
   
@director_view('eb_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbEbaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbEbmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TbEbmoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'eb_account':EbAccountPage.tableCls,
    'eb_account.edit':EbAccountForm,
})

page_dc.update({
    'eb_account':EbAccountPage
})