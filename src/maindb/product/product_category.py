from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from maindb.models import TbProductCategory

class ProductCategoryPage(TablePage):
    def get_label(self):
        return '商品分类'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbProductCategory
        exclude = []
        pop_edit_fields = ['id']
        
        def get_operation(self):
            ops = super().get_operation()
            out_ls =[]
            for op in ops:
                if op.get('name') !='delete_selected':
                    out_ls.append(op)
            return out_ls        

class ProdctCategoryForm(ModelFields):
    class Meta:
        model = TbProductCategory
        exclude = []

director.update({
    'product_category':ProductCategoryPage.tableCls,
    'product_category.edit':ProdctCategoryForm,
})

page_dc.update({
    'product_category':ProductCategoryPage
})