# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.base_data import director, page_dc, field_map
from helpers.director.model_func.dictfy import model_to_name
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.shortcut import ModelTable, TablePage, ModelFields
from maindb.riskcontrol.black_users import ip2num
from ..models import TbPaychannelblackiprange, TbRechargeareablacklist


class PayChannelAreaBlackList(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值地区黑名单'

    class tableCls(ModelTable):
        model = TbRechargeareablacklist
        exclude = []
        pop_edit_field = 'id'

        def dict_head(self, head):
            dc = {
                'area': 150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def get_operation(self):
            opes = super().get_operation()
            ls = []
            if opes:
                create = opes[0]
                ls.append(create)
            ls.extend([
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '启用',
                    'field': 'status',
                    'value': True,
                    'row_match': 'many_row',
                    'confirm_msg': '确认启用该充值地区黑名单吗?',
                    'visible': 'status' in self.permit.changeable_fields(),
                },
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '禁用',
                    'field': 'status',
                    'value': False,
                    'row_match': 'many_row',
                    'confirm_msg': '确认禁用该充值地区黑名单吗?',
                    'visible': 'status' in self.permit.changeable_fields(),
                }
            ])
            return ls


class PayChannelAreaBlackListForm(ModelFields):
    hide_fields = []

    class Meta:
        model = TbRechargeareablacklist
        exclude = []

    def dict_head(self, head):
        if head['name'] == 'paychannelid':
            head['placeholder'] = '请选择'
        return head


field_map[model_to_name(TbRechargeareablacklist) + '.status'] = IntBoolProc

director.update({
    'PayChannelAreaBlackList': PayChannelAreaBlackList.tableCls,
    'PayChannelAreaBlackList.edit': PayChannelAreaBlackListForm
})

page_dc.update({
    'paychannel_area_blacklist': PayChannelAreaBlackList,
})
