from helpers.director.shortcut import FieldsPage,Fields,page_dc,director,TablePage,ModelTable,PlainTable
from ..models import TbSetting
import json

class RiskcontrolSetting(TablePage):
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_label(self): 
        return '风险控制设置'
    
    class tableCls(PlainTable):
        
        def get_heads(self):
            riskform=RiskcontrolForm(crt_user=self.crt_user)
            
            return [
                {'name':'Level','label':'用户等级','editor':'com-table-pop-fields',
                 'fields_ctx':riskform.get_head_context(),'get_row':{'fun':'get_table_row'},'after_save':{'fun':'update_or_insert'}},
                {'name':'Memo','label':'备注'},
                {'name':'Sort','label':'排序'},
                {'name':'RechargeDays','label':'充值天数'},
            ]
        
        def get_rows(self):
            inst = TbSetting.objects.get(settingname='RiskControlLevel')
            ls = json.loads(inst.settingvalue)
            for row in ls:
                row['_director_name']='RiskcontrolForm'
            return ls

class RiskcontrolForm(Fields):
    def get_heads(self):
        return [
            {'name':'Level','label':'用户等级','editor':'number'},
            {'name':'Memo','label':'备注','editor':'linetext'},
            {'name':'Sort','label':'排序','editor':'number'},
            {'name':'RechargeDays','label':'充值天数','editor':'number'},
        ]
    
    def save_form(self):
        inst = TbSetting.objects.get(settingname='RiskControlLevel')
        ls = json.loads(inst.settingvalue)
        self.kw.pop('_director_name')
        for item in ls:
            if item['Level']==self.kw.get('Level'):
                item.update(self.kw)
        inst.settingvalue=json.dumps('')
        print('here')
    
    #class fieldsCls(Fields):
        #def get_heads(self): 
            #return [
                #{'name': 'quickamount','label': '快速投注金额','editor': 'linetext','help_text': '逗号分隔大于0的数(10,100,1000)','required': True,'fv_rule': 'dot_split_int',}, 
                #{'name': 'MinStakeAmount','label': '单注最低投注','editor': 'number','required': True,'fv_rule': 'range(0~)',}, 
                #{'name': 'MaxSinglePayout','label': '单注最高赔付','editor': 'number','required': True,'fv_rule': 'range(0~)'}, 
                #{'name': 'MaxMatchPayout','label': '单场最高赔付','editor': 'number','required': True,'fv_rule': 'range(0~)'}, 
                #{'name': 'SeriesMaxSinglePayout','label': '串关最大赔付','editor': 'number','required': True,'fv_rule': 'range(0~)'},
                #{'name':'MaxMatchUserBet','label':'用户单场<br>最大投注','editor':'number','required': True,'fv_rule': 'range(0~)'},
            #]


director.update({
    'RiskcontrolSetting':RiskcontrolSetting.tableCls,
    'RiskcontrolForm':RiskcontrolForm,
})

page_dc.update({
    'RiskcontrolSetting':RiskcontrolSetting
})