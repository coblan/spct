from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from maindb.models import TbProductNotice

class ProductNoticePage(TablePage):
    def get_label(self):
        return '商品公告'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbProductNotice
        exclude =[]
        pop_edit_fields = ['id']
        
        def get_operation(self):
            ops = super().get_operation()
            out_ls =[]
            for op in ops:
                if op.get('name') !='delete_selected':
                    out_ls.append(op)
            return out_ls        

class ProductNoticeForm(ModelFields):
    class Meta:
        model = TbProductNotice
        exclude = []

director.update({
    'proudct_notice':ProductNoticePage.tableCls,
    'proudct_notice.edit':ProductNoticeForm,
})

page_dc.update({
    'proudct_notice':ProductNoticePage
})
