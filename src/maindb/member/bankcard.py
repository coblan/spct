from helpers.director.shortcut import ModelTable, ModelFields, TablePage, page_dc, director,RowSort
from helpers.director.table.table import RowSearch, RowFilter
from ..models import TbBankcard
from django.db.models import Q, fields


class BankCard(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '银行卡管理'

    class tableCls(ModelTable):
        model = TbBankcard
        exclude = ['account', 'banktypeid']
        fields_sort = ['bankcardid', 'accountid', 'cardno', 'bankaccountname', 'bankaccountmobil', 'banktypename',
                       'bankprovince', 'bankcity', 'banksitename','createtime', 'active']
        pop_edit_field='bankcardid'

        def get_operation(self):
            return [
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '作废',
                    'field': 'active',
                    'value': False,
                    'row_match': 'one_row',
                    'confirm_msg': '确认作废该银行卡吗?', 
                    'visible': 'active' in self.permit.changeable_fields()
                }
            ]

        def dict_head(self, head):
            dc = {
                'accountid': 150,
                'cardno': 160,
                'bankaccountname': 140,
                'createtime': 150,
                'bankaccountmobil': 120,
                'banktypename': 120,
                'banksitename': 150
            }
            if head['name'] in dc:
                head['width'] = dc.get(head['name'])
            return head

        def dict_row(self, inst):
            tmp = list(inst.cardno)
            tmp[0:-4] = '*' * (len(tmp) - 4)
            out_str = ''.join(tmp)

            mobile = list(inst.bankaccountmobil)
            mobile[0:-4] = '*' * (len(mobile) - 4)
            mobile_str = ''.join(mobile)
            return {
                'cardno': out_str,
                'bankaccountmobil': mobile_str
            }

        class search(RowSearch):
            names = ['cardno', 'bankaccountname', 'accountid__nickname']

            def get_context(self):
                return {'search_tip': '用户昵称,卡号,开户人',
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
        
        class sort(RowSort):
            names = ['createtime']


class BankCardForm(ModelFields):
    hide_fields=['active']
    show_pk=True
    class Meta:
        model = TbBankcard
        #exclude = ['account', 'banktypeid']
        fields = ['bankaccountname','active','bankprovince','bankcity','banksitename']
    
    def dict_head(self, head):
        if head['name'] in ['bankcardid','bankaccountname']: #not in ['active']:
            head['readonly'] = True
        return head
    

        


director.update({
    'BankCards': BankCard.tableCls,
    'BankCards.edit': BankCardForm
})

page_dc.update(
    {
        'bankcards': BankCard
    }
)
