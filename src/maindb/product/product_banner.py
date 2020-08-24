from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from maindb.models import TbProductBanner

class ProductBannerPage(TablePage):
    def get_label(self):
        return '商品广告'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbProductBanner
        exclude = []
        pop_edit_fields = ['id']
    
class ProductBannerForm(ModelFields):
    class Meta:
        model = TbProductBanner
        exclude = []

director.update({
    'productBanner':ProductBannerPage.tableCls,
    'productBanner.edit':ProductBannerForm
})
    
page_dc.update({
    'productBanner':ProductBannerPage
})