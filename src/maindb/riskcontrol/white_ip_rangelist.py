# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.base_data import director, page_dc, field_map
from helpers.director.model_func.dictfy import model_to_name
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.shortcut import ModelTable, TablePage, ModelFields
from maindb.riskcontrol.black_users import ip2num
from ..models import TbAreablacklist, TbWhiteiprangelist


class WhiteIPRangeList(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return 'IP白名单'

    class tableCls(ModelTable):
        model = TbWhiteiprangelist
        exclude = []
        hide_fields = ['startipnum', 'endipnum']
        pop_edit_field = 'id'

        def dict_head(self, head):
            dc = {
                'startip': 120,
                'endip': 120
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def get_operation(self):
            create = super().get_operation()[0]
            return [create,
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '启用',
                        'field': 'iswork',
                        'value': True,
                        'row_match': 'many_row',
                        'confirm_msg': '确认启用该IP白名单范围吗?',
                        'visible': 'iswork' in self.permit.changeable_fields(),
                    },
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '禁用',
                        'field': 'iswork',
                        'value': False,
                        'row_match': 'many_row',
                        'confirm_msg': '确认禁用该IP白名单范围吗?',
                        'visible': 'iswork' in self.permit.changeable_fields(),
                    }
                    ]


class WhiteIPRangeForm(ModelFields):
    hide_fields = ['startipnum', 'endipnum']

    class Meta:
        model = TbWhiteiprangelist
        exclude = []

    def dict_head(self, head):
        if head['name'] in ['startip', 'endip']:
            head['fv_rule'] = 'ip'
        if head['name'] in ['startipnum', 'endipnum']:
            head['readonly'] = True
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


field_map[model_to_name(TbAreablacklist) + '.status'] = IntBoolProc

director.update({
    'WhiteIPRangeList': WhiteIPRangeList.tableCls,
    'WhiteIPRangeList.edit': WhiteIPRangeForm
})

page_dc.update({
    'white_ip_rangelist': WhiteIPRangeList,
})
