from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..ag.gamemoneyoutinfo import GamemoneyoutinfoPage
from maindb.models import TbImmoneyoutinfo,TbMerchants

class IMmoneyOutInfoPage(TablePage):
    def get_label(self):
        return '资金转出'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GamemoneyoutinfoPage.tableCls):
        model = TbImmoneyoutinfo
        exclude =[]
        
        class filters(RowFilter):
            range_fields=['ordertime']
            
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['status','productid']
                else:
                    return ['account__merchant_id','status','productid']
                
            def getExtraHead(self):
                if self.crt_user.merchant:
                    return []
                else:
                    return [{
                        'name':'account__merchant_id','label':'商户','editor':'com-filter-select','options':[
                            {'value':x.pk,'label':str(x)} for x in TbMerchants.objects.all()
                        ]
                    }]

director.update({
    'immoneyout':IMmoneyOutInfoPage.tableCls,
    
})
page_dc.update({
    'immoneyout':IMmoneyOutInfoPage
})