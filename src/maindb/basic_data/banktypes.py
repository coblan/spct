# encoding:utf-8
from __future__ import unicode_literals

from django.core.exceptions import ValidationError

from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter
from maindb.models import TbBanktypes, TbBankcard
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

        # def get_operation(self):
        #     ops = super().get_operation()
        #     return [ops[0]]

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

    def del_form(self):
        if TbBankcard.objects.filter(banktypeid=self.instance.banktypeid).exists():
            raise UserWarning('已有用户绑定该银行类型，不能删除')
        else:
            super().del_form()

    def save_form(self):
        super().save_form()

    def clean_banktypename(self):
        name = self.cleaned_data['banktypename']
        if 'banktypename' not in self.changed_data:
            return name
        if TbBanktypes.objects.filter(banktypename=name).exists():
            raise ValidationError("相同的银行卡类型已存在！")
        return name


director.update({
    'banktypes': BankTypesPage.tableCls,
    'banktypes.edit': BankTypesForm
})

page_dc.update({
    'banktypes': BankTypesPage,
})
