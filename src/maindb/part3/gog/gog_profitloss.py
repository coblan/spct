from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowFilter
from ..ag.profitloss import AgprofitlossPage
from maindb.models import TbGrprofitloss
from django.db.models import Sum

class GogProfitlossPage(TablePage):
    def get_label(self):
        return '投注列表'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(AgprofitlossPage.tableCls):
        model = TbGrprofitloss
        exclude = ['profitlosstype','refid','parentid','bettime','savetime']
        
        def statistics(self, query):
            dc = query.aggregate(total_profitlossmoney=Sum('profitlossmoney'),
                                 total_prizemoney=Sum('prizemoney'),
                                 total_winmoney=Sum('winmoney'),
                                 total_turnover=Sum('turnover'),
                                 )
     
            normed_dc = {k[6:]: v for (k, v) in dc.items()}
            normed_dc.update({
                '_label':'合计'
            })
            self.footer = normed_dc
            return query
        
        #class filters(RowFilter):
            #range_fields=['profitlosstime']


director.update({
    'gog_profitloss':GogProfitlossPage.tableCls,
})

page_dc.update({
    'gog_profitloss':GogProfitlossPage
})