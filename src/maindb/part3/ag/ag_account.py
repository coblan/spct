from helpers.director.shortcut import TablePage,page_dc,director,ModelFields,director_view,SelectSearch
from ..im.im_account import ImAccountPage
from maindb.models import TbAgaccount,TbGamemoneyoutinfo
from django.utils import timezone
import time

class AgAccountPage(TablePage):
    def get_label(self):
        return '账号管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ImAccountPage.tableCls):
        model = TbAgaccount
        exclude =[]
        redraw_left_money_director = 'ag_account/redraw_left_money'
        
        class search(SelectSearch):
            #names = ['account__nickname','agusername']
            exact_names=['account__nickname','agusername','account',]
            
            def get_option(self, name):
                if name == 'account':
                    return {'value':name,'label':'账号ID'}
                elif name == 'account__nickname':
                    return {'value': name,
                                    'label': '账号', }
                else:
                    return super().get_option(name)

class AgAccountForm(ModelFields):
    class Meta:
        model = TbAgaccount
        exclude =[]
   
   
@director_view('ag_account/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbAgaccount.objects.filter(account_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbGamemoneyoutinfo(account=inst.account,amount= inst.availablescores ,status=0,username=inst.agusername,ordertime=now,orderid=orderid,) )
    TbGamemoneyoutinfo.objects.bulk_create(out_list)
    
   
director.update({
    'agaccount':AgAccountPage.tableCls,
    'agaccount.edit':AgAccountForm,
})

page_dc.update({
    'agaccount':AgAccountPage
})