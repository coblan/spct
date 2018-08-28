# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter
from maindb.models import TbBanktypes
from helpers.director.base_data import director


class BankTypesPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '银行卡类型'

    class tableCls(ModelTable):
        model = TbBanktypes
        exclue = []
        pop_edit_field = 'banktypename'
        fields_sort = ['banktypeid', 'banktypename', 'active']

        class filters(RowFilter):
            names = ['active']

            def dict_head(self, head):
                return head

        class search(RowSearch):
            names = ['banktypename']

        class sort(RowSort):
            names = []

        def dict_head(self, head):
            dc = {
                'banktypename': 160
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head


class BankTypesForm(ModelFields):
    class Meta:
        model = TbBanktypes
        exclude = ['img']

    def save_form(self):
        super().save_form()


director.update({
    'banktypes': BankTypesPage.tableCls,
    'banktypes.edit': BankTypesForm
})

page_dc.update({
    'banktypes': BankTypesPage,
})