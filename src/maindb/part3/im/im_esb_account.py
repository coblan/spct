from . im_account import ImAccountPage
from helpers.director.shortcut import ModelFields,page_dc,director,director_view
from maindb.models import TbImeaccount,TbImmoneyoutinfo
from django.utils import timezone
import time

class IMESBAccountPage(ImAccountPage):
    def get_label(self):
        return '电竞用户'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbImeaccount
        exclude = []
        redraw_left_money_director='imesb/redraw_left_money'

class IMesbAccountForm(ModelFields):
    class Meta:
        model = TbImeaccount
        exclude =[]


@director_view('imesb/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbImeaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbImmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,productid = 401) )
    TbImmoneyoutinfo.objects.bulk_create(out_list)

director.update({
    'im_esb_account':IMESBAccountPage.tableCls,
    
})

page_dc.update({
    'im_esb_account':IMESBAccountPage
})