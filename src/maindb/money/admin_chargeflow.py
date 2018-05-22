# encoding:utf-8
from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowFilter,field_map,BaseFieldProc,model_to_name
from helpers.director.model_func.field_procs.datetimeproc import DateTimeProc
from ..models import TbChargeflow

class ChargeFlowPage(TablePage):
    template='jb_admin/table.html'
    
    def get_label(self):
        return '充值记录'
    
    class tableCls(ModelTable):
        model = TbChargeflow
        exclude=[]
        
        def inn_filter(self, query):
            return query.select_related('channel','accountid')
        
        class filters(RowFilter):
            range_fields=['createtime']

class CreateTimeProc(BaseFieldProc):
    
    def filter_get_range_head(self, name, model):
        return DateTimeProc.filter_get_range_head(self,name, model)
    
    def filter_dict_query_args(self, dc, name):
        return DateTimeProc.filter_dict_query_args(self,dc, name)

field_map.update({
    '%s.%s'%(model_to_name(TbChargeflow),'createtime'):CreateTimeProc
})

director.update({
    'ChargeFlow':ChargeFlowPage.tableCls
})

page_dc.update({
    'ChargeFlow':ChargeFlowPage,
})