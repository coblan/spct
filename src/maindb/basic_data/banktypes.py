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
        pop_edit_field = 'banktypename'
        fields_sort = ['banktypeid', 'banktypename', 'active', 'sort']

        def get_operation(self):
            create = super().get_operation()[0]

            return [create,
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '启用',
                        'field': 'active',
                        'value': True,
                        'row_match': 'one_row',
                        'confirm_msg': '确认启用该银行卡类型吗?'
                    },
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '禁用',
                        'field': 'active',
                        'value': False,
                        'row_match': 'one_row',
                        'confirm_msg': '确认禁用该银行卡类型吗?'
                    }
                    ]

        class filters(RowFilter):
            names = ['active']

            def dict_head(self, head):
                return head

        class search(RowSearch):
            names = ['banktypename']

        class sort(RowSort):
            names = ['sort']

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

    hide_fields = ['active']

    def save_form(self):
        if 'active' in self.changed_data:
            if TbBankcard.objects.filter(banktypeid=self.instance.banktypeid).exists():
                raise UserWarning('已有用户绑定该银行卡类型，不能禁用！')
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
