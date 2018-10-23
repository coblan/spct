# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter
from maindb.models import TbOperationlog
from helpers.director.base_data import director


class OperationLog(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '操作日志'

    class tableCls(ModelTable):
        model = TbOperationlog
        pop_edit_field = 'id'
        fields_sort = ['id', 'content', 'memo', 'createuser', 'createtime']

        class filters(RowFilter):
            range_fields = ['createtime']

            def dict_head(self, head):
                return head

        class search(RowSearch):
            names = ['createuser', 'content']

        class sort(RowSort):
            names = ['createtime']

        def dict_head(self, head):
            dc = {
                'content': 300,
                'memo': 100,
                'createuser': 100,
                'createtime': 150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def get_operation(self):
            return []


class OperationLogForm(ModelFields):
    class Meta:
        model = TbOperationlog
        exclude = ['type']

    readonly = ['type', 'content', 'memo', 'createuser', 'createtime']
    
    def get_operations(self):
        return []    


director.update({
    'OperationLog': OperationLog.tableCls,
    'OperationLog.edit': OperationLogForm

})

page_dc.update({
    'operation_log': OperationLog,
})
