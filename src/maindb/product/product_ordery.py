from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director,RowFilter
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
        
        def get_operation(self):
            return []
        
        class filters(RowFilter):
            names = ['state','merchant']
            range_fields = ['createtime']

class ProdctOrderForm(ModelFields):
    class Meta:
        model = TbProductOrder
        exclude = []
    
    def dict_head(self, head):
        if head['name'] not in ['state','expressno']:
            head['readonly'] = True
        return head

director.update({
    'product_order':ProductOrderPage.tableCls,
    'product_order.edit':ProdctOrderForm,
})

page_dc.update({
    'product_order':ProductOrderPage
})