from helpers.director.shortcut import ModelTable, ModelFields, TablePage, page_dc, director
from helpers.director.table.table import RowSearch
from ..models import TbBankcard


class BankCard(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '银行卡管理'

    class tableCls(ModelTable):
        model = TbBankcard
        exclude = []
        pop_edit_field = 'bankcardid'

        # fields_sort = ['bankcardno','nickname']
        def getExtraHead(self):
            return [
                {'name': 'nickname', 'label': "Nickname"}
            ]

        def dict_row(self, inst):
            tmp = list(inst.cardno)
            tmp[3:6] = '***'
            out_str = ''.join(tmp)
            return {
                'cardno': out_str,
                'nickname': inst.accountid.nickname
            }

        class search(RowSearch):
            names = ['cardno', 'bankaccountname']


class BankCardForm(ModelFields):
    class Meta:
        model = TbBankcard
        exclude = []


director.update({
    'BankCards': BankCard.tableCls,
    'BankCards.edit':BankCardForm
})

page_dc.update(
    {
        'BankCards': BankCard
    }
)
