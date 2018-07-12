from helpers.director.shortcut import TablePage, ModelTable, ModelFields, page_dc, director
from ..models import TbOddstypegroup
from ..rabbitmq_instance import updateSpread
import json

class TbOddstypeGroupPage(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '水位设置'
    
    class tableCls(ModelTable):
        model = TbOddstypegroup
        exclude = []
        fields_sort = ['oddstypenamezh', 'periodtype', 'spread']
        pop_edit_field = 'oddstypenamezh'
        
        def inn_filter(self, query): 
            return query.filter(enabled = 1)
        
        def get_operation(self): 
            return []

class TbOddstypeGroupForm(ModelFields):
    class Meta:
        model = TbOddstypegroup
        exclude = []
    readonly = ['oddstypenamezh', 'periodtype']
    field_sort = ['oddstypenamezh', 'periodtype', 'spread']
    
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