from helpers.director.shortcut import TablePage,ModelTable,page_dc,director
from ..ag.profitloss import AgprofitlossPage
from ..models import TbLcityprofitloss
from django.db.models import Sum

class SportProfitlossPage(TablePage):
    def get_label(self):
        return '投注列表'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(AgprofitlossPage.tableCls):
        model = TbLcityprofitloss
        exclude = ['profitlosstype','refid','parentid','bettime','savetime']
        
        def statistics(self, query):
            dc = query.aggregate(total_profitlossmoney=Sum('profitlossmoney'),
                                 total_prizemoney=Sum('prizemoney'),
                                 total_winmoney=Sum('winmoney')
                                 )
     
            #for k in dc:
                #dc[k] = str(round(dc.get(k, 0) or 0, 2))
            normed_dc = {k[6:]: v for (k, v) in dc.items()}
            normed_dc.update({
                '_label':'合计'
            })
            self.footer = normed_dc
            return query


director.update({
    'lcityprofitloss':SportProfitlossPage.tableCls,
})

page_dc.update({
    'lcityprofitloss':SportProfitlossPage
})