from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from maindb.models import TbProduct

class ProductPage(TablePage):
    def get_label(self):
        return '商品管理'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbProduct
        exclude =[]
        pop_edit_fields=['id']
        
        def get_operation(self):
            ops = super().get_operation()
            out_ls =[]
            for op in ops:
                if op.get('name') !='delete_selected':
                    out_ls.append(op)
            return out_ls

class ProductForm(ModelFields):
    class Meta:
        model = TbProduct
        exclude = []
    
    def dict_head(self, head):
        if head['name'] =='inventory':
            head['fv_rule'] = 'integer(+0)'
        if head['name'] =='price':
            head['fv_rule'] = 'range(0~, false)'
        return head

director.update({
    'product':ProductPage.tableCls,
    'product.edit':ProductForm,
})

page_dc.update({
    'product':ProductPage
})