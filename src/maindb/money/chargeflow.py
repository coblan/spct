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
        
        def dict_head(self, head): 
            dc={
                'id':120,
                'createtime':150,
                'callbacktime':150,
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
            return head
        
        def inn_filter(self, query):
            return query.select_related('channel','accountid')
        
        class filters(RowFilter):
            range_fields=['createtime']

class CreateTimeProc(BaseFieldProc):
    
    def filter_get_range_head(self, name, model):
        return DateTimeProc.filter_get_range_head(self,name, model)
    
    def filter_clean_filter_arg(self, f_str):
        return DateTimeProc.filter_clean_filter_arg(f_str)

field_map.update({
    '%s.%s'%(model_to_name(TbChargeflow),'createtime'):CreateTimeProc
})

director.update({
    'ChargeFlow':ChargeFlowPage.tableCls
})

page_dc.update({
    'ChargeFlow':ChargeFlowPage,
})