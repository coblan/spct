# encoding:utf-8
from __future__ import unicode_literals
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
        exclude = ['groupicon','channelicon']
        pop_edit_field = 'channeltype'

        class filters(RowFilter):
            names = ['active']

            def dict_head(self, head):
                return head

        class search(RowSearch):
            names = ['channeltype']

        class sort(RowSort):
            names = []

        def get_operation(self):
            return []

        def dict_head(self, head):
            dc = {
                'channelname':120,
                'channeltype': 120,
                'optionalamount':200,
                'memo':150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head


class PayChannelForm(ModelFields):
    readonly = ['channelname','channeltype','groupway','memo']

    class Meta:
        model = TbPaychannel
        exclude = ['groupicon','channelicon']

    def save_form(self):
        super().save_form()


director.update({
    'paychannel': PayChannelPage.tableCls,
    'paychannel.edit': PayChannelForm
})

page_dc.update({
    'paychannel': PayChannelPage,
})
