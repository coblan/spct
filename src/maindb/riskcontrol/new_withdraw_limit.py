from helpers.director.shortcut import TablePage, ModelTable, ModelFields, page_dc, director, RowSearch, RowFilter, RowSort
from ..models import TbParameterinfo
class WithDrawLimitContralPage(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '提现控制'
    
    class tableCls(ModelTable):
        pop_edit_field = 'memo'
        fields_sort = ['memo', 'isactive','value',  'daysnumber','leveltype', 'tag',  ]
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
                {'fun':'RapidOpen','editor':'com-op-btn','icon': 'fa-plus','label':'急速提现开',},
                {'fun':'RapidClose','editor':'com-op-btn','icon': 'fa-plus','label':'急速提现关',},
                {'fun':'WithdrawOpen','editor':'com-op-btn','icon': 'fa-plus','label':'普通提现开',},
                {'fun':'WithdrawClose','editor':'com-op-btn','icon': 'fa-plus','label':'普通提现关',},
            ]
        
        class search(RowSearch):
            names = ['memo']
            
        class filters(RowFilter):
            names = ['isactive', 'leveltype']
            
        class sort(RowSort):
            names = ['tag', 'memo']
        

class WithDrawForm(ModelFields):
    readonly = ['tid', 'tag', 'memo','leveltype']
    field_sort = ['memo', 'leveltype','isactive', 'value', 'daysnumber']
    class Meta:
        model = TbParameterinfo
        exclude = []
        
    def dict_head(self, head): 
        if head['name'] == 'value':
            head['editor'] = 'number'
            head['fv_rule'] = 'integer(+)'
        return head
    

director.update({
    'parameterinfo': WithDrawLimitContralPage.tableCls,
    'parameterinfo.edit': WithDrawForm,
})

page_dc.update({
    'parameterinfo': WithDrawLimitContralPage,
})