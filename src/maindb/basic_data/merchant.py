from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director
from maindb.models import TbMerchants

class MerchantsPage(TablePage):
    def get_label(self):
        return '商户管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbMerchants
        exclude =['atmno','atmkey']
        pop_edit_fields = ['id']
        
        def get_operation(self):
            return []

class MerchantsForm(ModelFields):
    class Meta:
        model = TbMerchants
        exclude =['atmno','atmkey']

director.update({
    'merchants':MerchantsPage.tableCls,
     'merchants.edit':MerchantsForm
})

page_dc.update({
    'merchants':MerchantsPage,
   
})