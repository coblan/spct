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
        fields_sort = ['banktypeid', 'banktypename', 'active', 'sort', 'img', 'bgimg']

        def get_operation(self):
            create = super().get_operation()[0]

            return [create,
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '启用',
                        'field': 'active',
                        'value': True,
                        'row_match': 'many_row',
                        'confirm_msg': '确认启用该银行卡类型吗?',
                        'visible': 'active' in self.permit.changeable_fields(),
                    },
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '禁用',
                        'field': 'active',
                        'value': False,
                        'row_match': 'many_row',
                        'confirm_msg': '确认禁用该银行卡类型吗?',
                        'visible': 'active' in self.permit.changeable_fields(),
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
                'banktypename': 160,
                'img': 120,
                'bgimg': 200,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head


class BankTypesForm(ModelFields):
    class Meta:
        model = TbBanktypes
        exclude = []

    hide_fields = ['active']

    def save_form(self):
        if 'active' in self.changed_data:
            if TbBankcard.objects.filter(banktypeid=self.instance.banktypeid).exists():
                raise UserWarning('已有用户绑定该银行卡类型，不能禁用！')
        if 'banktypename' in self.changed_data:
            if TbBankcard.objects.filter(banktypeid=self.instance.banktypeid).exists():
                raise UserWarning('已有用户绑定该银行卡类型，不能修名称！')
        super().save_form()

    def clean_banktypename(self):
        name = self.cleaned_data['banktypename']
        if 'banktypename' not in self.changed_data:
            return name
        if TbBanktypes.objects.filter(banktypename=name).exists():
            raise ValidationError("相同的银行卡类型已存在！")
        return name

    def dict_head(self, head):
        if head['name'] == 'img':
            head['up_url'] = '/d/upload?path=public/icon/banktypes'
        if head['name'] == 'bgimg':
            head['up_url'] = '/d/upload?path=public/icon/banktypes'
        return head


director.update({
    'banktypes': BankTypesPage.tableCls,
    'banktypes.edit': BankTypesForm
})

page_dc.update({
    'banktypes': BankTypesPage,
})
