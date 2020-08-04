# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.base_data import director, page_dc, field_map
from helpers.director.model_func.dictfy import model_to_name
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from helpers.director.shortcut import ModelTable, TablePage, ModelFields
from ..models import TbAreablacklist


class AreaBlackList(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '地区黑名单'

    class tableCls(ModelTable):
        model = TbAreablacklist
        exclude = []
        pop_edit_fields = ['id']

        def dict_head(self, head):
            dc = {
                'id': 120,
                'status': 120,
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
                    'confirm_msg': '确认启用该地区黑名单吗?',
                    'visible': 'status' in self.permit.changeable_fields(),
                },
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '禁用',
                    'field': 'status',
                    'value': False,
                    'row_match': 'many_row',
                    'confirm_msg': '确认禁用该地区黑名单吗?',
                    'visible': 'status' in self.permit.changeable_fields(),
                }
            ])
            return ls


class AreaBlackListForm(ModelFields):
    hide_fields = []

    class Meta:
        model = TbAreablacklist
        exclude = []

field_map[model_to_name(TbAreablacklist) + '.status'] = IntBoolProc


director.update({
    'AreaBlackList': AreaBlackList.tableCls,
    'AreaBlackList.edit': AreaBlackListForm
})

page_dc.update({
    'area_blacklist': AreaBlackList,
})
