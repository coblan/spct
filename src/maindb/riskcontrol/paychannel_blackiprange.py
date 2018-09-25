# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.base_data import director, page_dc
from helpers.director.shortcut import ModelTable, TablePage, ModelFields
from maindb.riskcontrol.black_users import ip2num
from ..models import TbPaychannelblackiprange


class PayChannelBlackIPRangeList(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值IP黑名单'

    class tableCls(ModelTable):
        model = TbPaychannelblackiprange
        exclude = []
        hide_fields = ['startipnum', 'endipnum']
        pop_edit_field = 'blackiprangelistid'

        def dict_head(self, head):
            dc = {
                'startip': 120,
                'endip': 120,
                'remark': 150,
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
            ls.extend( [
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '启用',
                        'field': 'iswork',
                        'value': True,
                        'row_match': 'one_row',
                        'confirm_msg': '确认启用该充值IP黑名单吗?', 
                        'visible': 'iswork' in self.permit.changeable_fields(),
                    },
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '禁用',
                        'field': 'iswork',
                        'value': False,
                        'row_match': 'one_row',
                        'confirm_msg': '确认禁用该充值IP黑名单吗?', 
                         'visible': 'iswork' in self.permit.changeable_fields(),
                    }
                    ])
            return ls
            


class PayChannelBlackIPRangeForm(ModelFields):
    hide_fields = ['startipnum', 'endipnum']

    class Meta:
        model = TbPaychannelblackiprange
        exclude = []

    def dict_head(self, head):
        if head['name'] in ['startip', 'endip']:
            head['fv_rule'] = 'ip'
        if head['name'] in ['startipnum', 'endipnum']:
            head['readonly'] = True
        if head['name']=='paychannelid':
            head['placeholder']='请选择'
        return head

    def clean_dict(self, dc):
        super().clean_dict(dc)
        if dc.get('startip'):
            dc['startipnum'] = ip2num(dc.get('startip'))
        else:
            dc['startipnum'] = 0

        if dc.get('endip'):
            dc['endipnum'] = ip2num(dc.get('endip'))
        else:
            dc['endipnum'] = 0
        return dc


director.update({
    'PayChannelBlackIPRangeList': PayChannelBlackIPRangeList.tableCls,
    'PayChannelBlackIPRangeList.edit': PayChannelBlackIPRangeForm
})

page_dc.update({
    'paychannel_blackip': PayChannelBlackIPRangeList,
})