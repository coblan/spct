from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowSearch, ModelFields, RowFilter, field_map, \
     model_to_name
from ..models import TbLimit, TbMatches, TbOddstypegroup
from ..admin_riskcontrol.blanklist import AccountSelect
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from django import forms

class TbLimitPage(TablePage):
    template = 'jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    def get_label(self): 
        return '最大赔付'  # maxpayout
    
    class tableCls(ModelTable):
        model = TbLimit
        exclude = ['tid']
        pop_edit_field = 'matchid'
        def __init__(self, *args, **kw): 
            super().__init__(*args, **kw)
            self.oddstype_options = [{'value': x.oddstypegroup, 'label': x.oddstypenamezh,} for x in TbOddstypegroup.objects.filter(enabled = 1)]
            self.user_options = [
                {'value': 1, 'label': '等级一',}, 
                {'value': 2, 'label': '等级二',}, 
                {'value': 3, 'label': '等级三',}, 
                {'value': 4, 'label': '等级四',}, 
                {'value': 5, 'label': '等级五',}, 
            ]
        
        def getExtraHead(self): 
            return [
                {'name': 'match','label': '比赛',}
            ]
            
        def dict_head(self, head): 
            if head['name'] == 'relationno':
                head['editor'] = 'com-table-label-shower'
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-label-shower'
            
            return head
        
        def dict_row(self, inst): 
            if inst.limittype in [11, 21]:
                relationno_label = ''
            elif inst.limittype in [12, 22]:
                relationno_label = 'ERROR'
                for i in  self.oddstype_options:
                    if i['value'] == inst.relationno:
                        relationno_label = i['label']
                        break
            elif inst.limittype in [13 ]:
                relationno_label = 'ERROR'
                for i in  self.user_options:
                    if i['value'] == inst.relationno:
                        relationno_label = i['label']
                        break                
                
            return {
                '_relationno_label': relationno_label,
                'match': inst.matchid.team1zh,
            }
        
        class search(RowSearch):
            names = ['matchid']
            
class TbLimitForm(ModelFields):
    readonly = ['createtime', 'updatetime']
    class Meta:
        model = TbLimit
        exclude = []
    
    extra_mixins = ['maxpayout_form_logic']
    def __init__(self, *args, **kw): 
        super().__init__(*args, **kw)
        self.oddstype_options = [{'value': x.oddstypegroup, 'label': x.oddstypenamezh,} for x in TbOddstypegroup.objects.filter(enabled = 1)]
        self.user_options = [
            {'value': 1, 'label': '等级一',}, 
            {'value': 2, 'label': '等级二',}, 
            {'value': 3, 'label': '等级三',}, 
            {'value': 4, 'label': '等级四',}, 
            {'value': 5, 'label': '等级五',}, 
            ]
        
    def dict_head(self, head):
        
        if head['name'] =='matchid':
            table_obj = MatchSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
            head['options'] = []
        if head['name'] =='accountid':
            table_obj = AccountSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()  
            head['options'] = []
            
        if head['name'] == 'relationno':
            head['user_options'] = self.user_options
            head['oddstype_options'] = self.oddstype_options
        
        return head 
    
    def dict_row(self, inst): 
        if inst.limittype in [11, 21]:
                relationno_label = ''
        elif inst.limittype in [12, 22]:
            relationno_label = 'ERROR'
            for i in  self.oddstype_options:
                if i['value'] == inst.relationno:
                    relationno_label = i['label']
                    break
        elif inst.limittype in [13 ]:
            relationno_label = 'ERROR'
            for i in  self.user_options:
                if i['value'] == inst.relationno:
                    relationno_label = i['label']
                    break                
            
        return {
            '_relationno_label': relationno_label,
            'relationno': inst.relationno or 1,
            'createtime': inst.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            'updatetime': inst.updatetime.strftime('%Y-%m-%d %H:%M:%S'),
        }
    def clean_accountid(self): 
        data = self.cleaned_data['accountid']
        limittype = self.cleaned_data['limittype']
        if limittype in [21, 22] and not data:
            raise forms.ValidationError('必须填写一个用户')
        return data
    
    def clean_maxsinglepayout(self): 
        data = self.cleaned_data['maxsinglepayout']
        if float(data) <= 0:
            raise forms.ValidationError('必须大于0')
        return data
    
    
    

class MatchSelect(ModelTable):
    model = TbMatches
    include=['matchid','tournamentzh', 'team1zh', 'team2zh', 'matchdate']
    def dict_head(self, head):
        dc={
               'matchid':100,
               'tournamentzh': 150,
      
           }
        if dc.get(head['name']):
            head['width'] =dc.get(head['name'])
            
        if head['name']=='matchid':
            head['editor']='com-table-foreign-click-select'
        return head
    
    class search(RowSearch):
        names=['matchid', 'team1zh', 'team2zh']
        
    class filters(RowFilter):
        range_fields=['matchdate']

field_map.update({
    model_to_name(TbLimit) + '.status': IntBoolProc,
})

director.update({
    'sports.limit': TbLimitPage.tableCls,
    'sports.limit.edit': TbLimitForm,
    'sports.matchselect': MatchSelect,
})

page_dc.update({
    'sports.limit': TbLimitPage,
})