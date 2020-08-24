from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director
from maindb.models import TbProductOrder

class ProductOrderPage(TablePage):
    def get_label(self):
        return '商品订单'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbProductOrder
        exclude = []
        pop_edit_fields = ['id']

class ProdctOrderForm(ModelFields):
    class Meta:
        model = TbProductOrder
        exclude = []

director.update({
    'product_order':ProductOrderPage.tableCls,
    'product_order.edit':ProdctOrderForm,
})

page_dc.update({
    'product_order':ProductOrderPage
})