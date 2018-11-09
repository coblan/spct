from helpers.director.shortcut import FieldsPage, Fields, page_dc, director
from ..models import TbSetting
import json
from helpers.func.sim_signal import sim_signal
class ParameterPage(FieldsPage):
    template = 'jb_admin/fields.html'
    def get_label(self): 
        return '参数管理'
    
    class fieldsCls(Fields):
        def get_heads(self): 
            return [
                {'name': 'quickamount','label': '快速投注金额','editor': 'linetext','help_text': '逗号分隔大于0的数(10,100,1000)','required': True,'fv_rule': 'dot_split_int',}, 
                {'name': 'MinStakeAmount','label': '单注最低投注','editor': 'number','required': True,'fv_rule': 'range(0~)',}, 
                {'name': 'MaxSinglePayout','label': '单注最高赔付','editor': 'number','required': True,'fv_rule': 'range(0~)'}, 
                {'name': 'MaxMatchPayout','label': '单场最高赔付','editor': 'number','required': True,'fv_rule': 'range(0~)'}, 
                {'name': 'SeriesMaxSinglePayout','label': '串关最大赔付','editor': 'number','required': True,'fv_rule': 'range(0~)'}
            ]
        
        def get_row(self): 
            quick = TbSetting.objects.get(settingname = 'Static:QuickAmount')
            quick_str =  ','.join( [str(x) for x in json.loads( quick.settingvalue ) ])
            payout = TbSetting.objects.get(settingname = 'Static:SinglePayout')
            payout_dc = json.loads(payout.settingvalue)
            payout_dc.update( {
                'quickamount': quick_str,
                '_director_name': self.get_director_name(),
            })
            return payout_dc
        
        def save_form(self): 
            quickamount = self.kw.get('quickamount')
            quickamount_str = '[%s]' % quickamount
            TbSetting.objects.filter(settingname = 'Static:QuickAmount').update(settingvalue = quickamount_str)
            sim_signal.send('tbsetting.quickamount.changed')
            payout = {}
            for k in ['MinStakeAmount', 'MaxSinglePayout', 'MaxMatchPayout', 'SeriesMaxSinglePayout']:
                payout[k] = float(self.kw.get(k))
            TbSetting.objects.filter(settingname = 'Static:SinglePayout').update(settingvalue = json.dumps(payout))
            sim_signal.send('tbsetting.maxpayout.changed')

director.update({
    'ParameterForm': ParameterPage.fieldsCls,
})

page_dc.update({
    'ParameterPage': ParameterPage,
})