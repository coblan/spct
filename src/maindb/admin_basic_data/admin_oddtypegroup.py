from helpers.director.shortcut import TablePage, ModelTable, ModelFields, page_dc, director
from ..models import TbOddstypegroup
from ..rabbitmq_instance import updateSpread
import json
from helpers.maintenance.update_static_timestamp import js_stamp_dc

class TbOddstypeGroupPage(TablePage):
    template = 'jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    
    def get_label(self): 
        return '水位设置'
    
    class tableCls(ModelTable):
        model = TbOddstypegroup
        exclude = []
        fields_sort = ['bettype','oddstypenamezh', 'periodtype',  'spread']
        pop_edit_field = 'oddstypenamezh'
        
        def inn_filter(self, query): 
            return query.filter(enabled = 1)
        
        def get_operation(self): 
            return []
        
        def dict_head(self, head): 
            dc = {
                'oddstypenamezh': 200,
            }
            if dc.get( head['name'] ):
                head['width'] = dc.get( head['name'] )
            return head

class TbOddstypeGroupForm(ModelFields):
    class Meta:
        model = TbOddstypegroup
        exclude = []
    readonly = ['bettype','oddstypenamezh', 'periodtype']
    field_sort = ['bettype','oddstypenamezh', 'periodtype', 'spread']
    
    def dict_head(self, head): 
        if head['name'] == 'spread':
            head['fv_rule'] = 'range(0~1);two_valid_digit'
            head['step'] = 0.01
        return head
    
    def save_form(self): 
        rt = super().save_form()
        
        ls = [
            {'BetType': self.instance.bettype,
             'PeriodType': self.instance.periodtype,
             'Spread':float( self.instance.spread )
             }
        ]
        
        updateSpread(json.dumps(ls))
        
        return rt
        

director.update({
    'maindb.TbOddstypeGroupPage': TbOddstypeGroupPage.tableCls,
    'maindb.TbOddstypeGroupPage.edit': TbOddstypeGroupForm,
})

page_dc.update({
    'maindb.TbOddstypeGroupPage': TbOddstypeGroupPage,
})