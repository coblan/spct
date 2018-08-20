from helpers.director.shortcut import ModelTable, ModelFields, TablePage, page_dc, director
from helpers.director.table.table import RowSearch, RowFilter
from ..models import TbBankcard
from django.db.models import Q, fields


class BankCard(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '银行卡管理'

    class tableCls(ModelTable):
        model = TbBankcard
        exclude = ['account']
        pop_edit_field = 'bankcardid'

        # filters=['active']

        def getExtraHead(self):
            return [
                # {'name': 'nickname', 'label': "昵称"}
            ]

        def dict_head(self, head):
            dc = {
                'cardno': 200,
                'bankaccountname': 140
            }
            if head['name'] in dc:
                head['width'] = dc.get(head['name'])
            return head

        def dict_row(self, inst):
            tmp = list(inst.cardno)
            tmp[0:-4] = '*' * (len(tmp) - 4)
            out_str = ''.join(tmp)
            return {
                'cardno': out_str
            }

        class search(RowSearch):
            names = ['cardno', 'accountid__nickname']

            def get_context(self):
                return {'search_tip': '卡号，昵称',
                        'editor': 'com-search-filter',
                        'name': '_q'
                        }

            def get_query(self, query):
                if self.q:
                    exp = None
                    ls = self.valid_name + ['accountid__nickname']
                    for name in ls:
                        kw = {}
                        kw['%s__icontains' % name] = self.q
                        if exp is None:
                            exp = Q(**kw)
                        else:
                            exp = exp | Q(**kw)
                    return query.filter(exp)
                else:
                    return query

        class filters(RowFilter):
            names = ['active']


class BankCardForm(ModelFields):
    class Meta:
        model = TbBankcard
        exclude = []


director.update({
    'BankCards': BankCard.tableCls,
    'BankCards.edit': BankCardForm
})

page_dc.update(
    {
        'BankCards': BankCard
    }
)
