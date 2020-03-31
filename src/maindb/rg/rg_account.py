from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view
from maindb.im.im_account import ImAccountPage
from ..models import TbRgaccount,TbRgmoneyoutinfo

class RgAccountPage(TablePage):
    def get_label(self):
        return 'RG账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbRgaccount
        exclude =[]
        redraw_left_money_director = 'rgaccount/redraw_left_money'

class RgAccountForm(ModelFields):
    class Meta:
        model = TbRgaccount
        exclude =[]
   
   
@director_view('rgaccount/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbRgaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbRgmoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.username,ordertime=now,orderid=orderid,) )
    TbRgmoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'rgaccount':RgAccountPage.tableCls,
    'rgaccount.edit':RgAccountForm,
})

page_dc.update({
    'rgaccount':RgAccountPage
})