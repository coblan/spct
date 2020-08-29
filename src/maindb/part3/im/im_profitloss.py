from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowFilter
from ..ag.profitloss import AgprofitlossPage
from maindb.models import TbImprofitloss,TbMerchants
from django.db.models import Sum


class IMProfitlossPage(TablePage):
    def get_label(self):
        return '投注列表'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(AgprofitlossPage.tableCls):
        model = TbImprofitloss
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
        
        class filters(RowFilter):
            range_fields=['profitlosstime']
            
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['gametype']
                else:
                    return ['account__merchant_id','gametype']
                
            def getExtraHead(self):
                if self.crt_user.merchant:
                    return []
                else:
                    return [{
                        'name':'account__merchant_id','label':'商户','editor':'com-filter-select','options':[
                            {'value':x.pk,'label':str(x)} for x in TbMerchants.objects.all()
                        ]
                     }]
            #class filters(RowFilter):
                #names = ['productid']
                #range_fields=['profitlosstime']
                ##gametype


director.update({
    'improfitloss':IMProfitlossPage.tableCls,
})

page_dc.update({
    'improfitloss':IMProfitlossPage
})