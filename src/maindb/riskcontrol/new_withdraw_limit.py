from helpers.director.shortcut import TablePage, ModelTable, ModelFields, page_dc, director, RowSearch, RowFilter, \
    RowSort
from ..models import TbParameterinfo


class WithDrawLimitContralPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '提现控制'

    class tableCls(ModelTable):
        pop_edit_field = 'memo'
        fields_sort = ['memo',  'value', 'daysnumber', 'leveltype','isactive', ]
        model = TbParameterinfo
        exclude = []

        def dict_head(self, head):
            if head['name'] == 'memo':
                head['width'] = 200
            if head['name'] == 'tag':
                head['width'] = 140
            return head

        def get_operation(self):
            return [
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '启用', 'field': 'isactive','row_match': 'many_row',
                 'value': True, 'confirm_msg': '确认启用这些设置项？', 'visible': 'isactive' in self.permit.changeable_fields(),},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '禁用', 'field': 'isactive','row_match': 'many_row',
                 'value': False, 'confirm_msg': '确认禁用这些设置项？', 'visible': 'isactive' in self.permit.changeable_fields()}
            ]

        class search(RowSearch):
            names = ['memo']

        class filters(RowFilter):
            names = ['isactive', 'leveltype']

        class sort(RowSort):
            names = ['tag', 'memo']


class WithDrawForm(ModelFields):
    readonly = ['tid', 'tag', 'memo', 'leveltype']
    field_sort = ['memo', 'leveltype', 'isactive', 'value', 'daysnumber']

    class Meta:
        model = TbParameterinfo
        exclude = []

    def dict_head(self, head):
        if head['name'] in ['daysnumber', 'value']:
            head['editor'] = 'number'
            head['fv_rule'] = 'integer(+)'
        if head['name'] == 'value':
            head['show'] = "scope.row.tag !='IsRapidWithdraw' && scope.row.tag !='IsEnableWithdraw'"
        if head['name'] == 'daysnumber':
            head['show'] = "scope.row.tag !='IsRapidWithdraw' && scope.row.tag !='IsEnableWithdraw'"        
        return head


director.update({
    'parameterinfo': WithDrawLimitContralPage.tableCls,
    'parameterinfo.edit': WithDrawForm,
})

page_dc.update({
    'parameterinfo': WithDrawLimitContralPage,
})
