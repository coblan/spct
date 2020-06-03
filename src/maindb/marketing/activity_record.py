from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter,has_permit
from maindb.models import TbActivityRecord,TbMerchants,TbActivityV2
from hello.merchant_user import get_user_merchantid,MerchantInstancCheck
from django.db.models import F

class ActivityRecoredPage(TablePage):
    def get_label(self):
        return '活动记录'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbActivityRecord
        exclude = []
        
        def dict_head(self, head):
            width ={
                'activity':130,
                'account':130,
                'amount':100,
                'bonus':120,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head
        
        def inn_filter(self, query):
            query= query.annotate(account__merchant__name=F('account__merchant__name'))
            if self.crt_user.merchant:
                query = query.filter(account__merchant = self.crt_user.merchant)
            return query
        
        def getExtraHead(self):
            return [
                {'name':'account__merchant__name','label':'商户'}
            ]
        
        def dict_row(self, inst):
            return {
                'account__merchant__name':inst.account__merchant__name,
            }
        
        class filters(RowFilter):
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['account__nickname','activity']
                else:
                    return ['account__merchant','account__nickname','activity']
                    
            range_fields=['createtime']
            icontains = ['account__nickname']
            
            def getExtraHead(self):
                return [
                    {'name':'account__nickname','label':'用户昵称'},
                    {'name':'account__merchant','label':'商户','editor':'com-filter-select','options':[
                        {'value':x.pk ,'label':str(x)} for x in TbMerchants.objects.all()
                        ],'visible':not self.crt_user.merchant},
                ]
            
            def dict_head(self, head):
                if head['name'] == 'activity' and self.crt_user.merchant:
                    head['options'] = [
                        {'value':x.pk,'label':str(x)} for x in TbActivityV2.objects.filter(merchant = self.crt_user.merchant)
                    ]
                return head

director.update({
    'activity_record':ActivityRecoredPage.tableCls,
})

page_dc.update({
    'activity_record':ActivityRecoredPage
})