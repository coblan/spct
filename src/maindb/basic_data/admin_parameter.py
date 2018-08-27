from helpers.director.shortcut import FieldsPage, page_dc, director, ModelFields, Fields, director
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from ..models import TbParameterinfo

class Parameter(FieldsPage):
    template = 'jb_admin/fields.html'
    extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]
    
    
    class fieldsCls(Fields):
        extra_mixins = ['parameter_form_logic']
        def get_heads(self): 
            heads =   [
                {'name': 'IsEnableWithdraw','label': '平台提现总开关','editor': 'com-field-int-bool', 'check_label': '开启',}, 
                {'name': 'MaxWithdrawAmount','label': '单次最大提现金额','editor': 'com-field-number','fv_rule': 'range(1~500000)',}, 
                {'name': 'MinWithdrawAmount','label': '单次最小提现金额','editor': 'com-field-number','fv_rule': 'range(1~500000)',}, 
                {'name': 'MaxWithdrawCount','label': '每天最大提现次数','editor': 'com-field-number','fv_rule': 'range(1~1000)',}, 
                {'name': 'BetRechargeRate','label': '投注充值比率','editor': 'com-field-number','fv_rule': 'range(0~1)','help_text': '投注充值比率，防止用户套现',}, 
                {'name': 'WithdrawRrechargeDifference','label': '提现充值差额','editor': 'com-field-number','fv_rule': 'range(1~500000)','help_text': '提现充值差额，超过此差额不允许自动提现',}, 
                {'name': 'ProfitRechargeDifference','label': '盈利充值差额','editor': 'com-field-number','fv_rule': 'range(0~10000)','help_text': '盈利充值差额，超过此差额不允许自动提现',}, 
                {'name': 'PrizeBetRate','label': '派奖金额/投注金额比率','editor': 'com-field-number','fv_rule': 'range(1~1000)', 'help_text': '派奖金额/投注金额比率，超过此比率不允许自动提现',}, 
                {'name': 'WithdrawIntervalMinutes','label': '提现频率','editor': 'com-field-pinglue','fv_rule': 'range(1~1000)', 'help_text': 'xx分钟内xx次提现',}, 
               
            
            ]
            for head in heads:
                if head['name'] not in ['IsEnableWithdraw']:
                    head['subhead'] = dict(head)
                    head['editor'] = 'com-field-parameter'
            
            return heads
        
        def get_row(self): 
            query = TbParameterinfo.objects.all()
            dc = {
                '_director_name': self.get_director_name(),
                'active_names': [],
            }
            
            for info in query:
                if info.isactive:
                    dc['active_names'].append(info.tag)
                dc[info.tag] = info.value
            
            return dc
        
        def save_form(self): 
            infos =  list( TbParameterinfo.objects.all() )
            active_names = self.front_dc['active_names']
            if 'WithdrawIntervalMinutes' in active_names:
                active_names.append('WithdrawIntervalCount')
            else:
                active_names.remove('WithdrawIntervalCount')

            for info in infos:
                value = info.value
                for k, v in self.front_dc.items():
                    if info.tag == k:
                        value = v
                        break
                if info.tag in active_names:
                    isactive = True
                else:
                    isactive = False
                
                if info.value != value or info.isactive != isactive:
                    info.value = value
                    info.isactive = isactive
                    info.save()
                    
            
            
                
        


director.update(
    {'Parameter': Parameter.fieldsCls,}
)

page_dc.update({
    'Parameter': Parameter,
})
        
    
