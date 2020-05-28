from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view
from maindb.im.im_account import ImAccountPage
from maindb.models import TbVraccount,TBVRMoneyOutInfo
from django.utils import timezone
import time

class VrAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbVraccount
        exclude =[]
        redraw_left_money_director = 'vr_account/redraw_left_money'

class VRAccountForm(ModelFields):
    class Meta:
        model = TbVraccount
        exclude =[]
   
   
@director_view('vr_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbVraccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TBVRMoneyOutInfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TBVRMoneyOutInfo.objects.bulk_create(out_list)
    
   
director.update({
    'vr_account':VrAccountPage.tableCls,
    'vr_account.edit':VRAccountForm,
})

page_dc.update({
    'vr_account':VrAccountPage
})