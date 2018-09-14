# encoding:utf-8
from __future__ import unicode_literals

from django.core.exceptions import ValidationError

from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter
from maindb.models import TbBanktypes, TbPaychannel
from helpers.director.base_data import director


class PayChannelPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值渠道'

    class tableCls(ModelTable):
        model = TbPaychannel
        # exclude = ['channelicon']
        pop_edit_field = 'paychannelid'
        fields_sort = ['paychannelid', 'channelgroupid', 'channelname', 'channeltype', 'active', 'minamount',
                       'maxamount', 'optionalamount', 'channelicon', 'memo']

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
                        'confirm_msg': '确认启用该充值渠道吗?'
                    },
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '禁用',
                        'field': 'active',
                        'value': False,
                        'row_match': 'one_row',
                        'confirm_msg': '确认禁用该充值渠道吗?'
                    }
                    ]

        class filters(RowFilter):
            names = ['active']

            def dict_head(self, head):
                return head

        class search(RowSearch):
            names = ['channeltype']

        class sort(RowSort):
            names = []

        def dict_head(self, head):
            dc = {
                'channelgroupid': 120,
                'channelname': 120,
                'channeltype': 120,
                'optionalamount': 200,
                'channelicon': 150,
                'memo': 150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head


class PayChannelForm(ModelFields):
    # readonly = ['channelname','channeltype','groupway','memo']

    def dict_head(self, head):
        if head['name'] == 'channelgroupid':
            head['placeholder'] = '请选择'
        return head

    class Meta:
        model = TbPaychannel
        exclude = ['memo']

    def clean_channelname(self):
        name = self.cleaned_data['channelname']
        if 'channelname' not in self.changed_data:
            return name
        if TbPaychannel.objects.filter(channelname=name).exists():
            raise UserWarning("相同的Apolo渠道【{}】已存在！".format(name))
        return name

    def save_form(self):
        super().save_form()


director.update({
    'paychannel': PayChannelPage.tableCls,
    'paychannel.edit': PayChannelForm
})

page_dc.update({
    'paychannel': PayChannelPage,
})
