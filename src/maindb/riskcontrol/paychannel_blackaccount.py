from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,director
from ..models import TbPaychannelblackaccount

class PaychannelblackaccountPage(TablePage):
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    def get_label(self):
        return '充值账号黑名单'
    
    class tableCls(ModelTable):
        model = TbPaychannelblackaccount
        exclude=[]

class PaychannelblackaccountForm(ModelFields):
    class Meta:
        model = TbPaychannelblackaccount
        exclude = []

director.update({
    'Paychannelblackaccount':PaychannelblackaccountPage.tableCls,
    'Paychannelblackaccount.edit':PaychannelblackaccountForm
})

page_dc.update({
    'Paychannelblackaccount':PaychannelblackaccountPage,
})