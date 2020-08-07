from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,director
from ..models import TbPaychannelblackaccount,TbAccount
from . black_users import AccountSelect

class PaychannelblackaccountPage(TablePage):
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    def get_label(self):
        return '充值用户黑名单'
    
    class tableCls(ModelTable):
        pop_edit_fields = ['blackaccountid']
        model = TbPaychannelblackaccount
        exclude=[]

class PaychannelblackaccountForm(ModelFields):
    #hide_fields=['account']
    
    @property
    def hide_fields(self):
        if self.crt_user.merchant:
            return ['merchant','account',]
        else:
            return ['account',]
    
    class Meta:
        model = TbPaychannelblackaccount
        exclude = []
    
    def clean_save(self):     
        self.instance.account = self.instance.accountid.account
    
    def dict_head(self, head):
        if head['name'] == 'accountid':
            table_obj = AccountSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
        return head    

director.update({
    'Paychannelblackaccount':PaychannelblackaccountPage.tableCls,
    'Paychannelblackaccount.edit':PaychannelblackaccountForm
})

page_dc.update({
    'Paychannelblackaccount':PaychannelblackaccountPage,
})