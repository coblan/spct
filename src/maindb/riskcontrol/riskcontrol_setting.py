from helpers.director.shortcut import FieldsPage,Fields,page_dc,director,TablePage,ModelTable,PlainTable
from ..models import TbSetting,TbMerchantproperties,TbMerchants
import json
from helpers.director.access.permit import has_permit
from django.core.exceptions import PermissionDenied

class RiskcontrolSetting(object):
    def __init__(self,request,engin):
        self.request = request
        
    def get_template(self, prefer=None):
        return 'jb_admin/tabs.html'
    
    def get_label(self): 
        return '风险控制设置'
    
    def get_context(self):
        first = TbMerchants.objects.first()
        ctx ={
            'tab_ctx':'riskcontral-tab',
            'tab_name': str( first.id )         
        }
        ctx['named_ctx']={
            'riskcontral-tab':[
                {'name':str( x.id ),
                 'label':x.merchantname,
                 'editor':'com-tab-table',
                 'table_ctx':{**RiskContralTab().get_head_context(),
                              'search_args':{'merchant':x.id}},
                 } for x in TbMerchants.objects.all()
            ]
        }
        
        return ctx
    
class RiskContralTab(PlainTable):
    
    def custom_permit(self):
        if not has_permit(self.crt_user, 'risk.RiskcontrolSetting'):
            raise PermissionDenied('没有权限访问风险控制设置')
        
    def get_heads(self):
        riskform=RiskcontrolForm(crt_user=self.crt_user)
        
        fields_ctx = riskform.get_head_context()
        fields_ctx.update({
            'init_express':'ex.vueAssign(scope.row,scope.vc.par_row)',
            'after_save':'ex.vueAssign( scope.vc.par_row,scope.row)',
            'ops_loc':'bottom'
        })
        
        return [
            {'name':'Level',
             'label':'风控等级',
             'editor':'com-table-click',
             'fields_ctx':fields_ctx,
             'action':'scope.head.fields_ctx.title=scope.row._label;scope.head.fields_ctx.par_row=scope.row;cfg.pop_vue_com("com-form-one",scope.head.fields_ctx)',
             },
            #{'name':'Level','label':'风控等级','editor':'com-table-pop-fields',
             #'fields_ctx':riskform.get_head_context(),'get_row':{'fun':'get_table_row'},'after_save':{'fun':'update_or_insert'}},
            #{'name':'Level','label':'风控等级',},
            {'name':'Memo','label':'备注'},
            {'name':'RechargeDays','label':'充值天数'},
            {'name':'RechargeCount','label':'充值次数'},
            {'name':'RechargeAmount','label':'充值金额'},
            #{'name':'PossibleWinAmount','label':'可赢额','width':150,},
            #{'name':'DelaySec','label':'投注延时(秒)','width':150,}
        ]
    
    def get_rows(self):
        prop = TbMerchantproperties.objects.get(merchant_id = self.search_args.get('merchant'))
        ls = json.loads(prop.riskcontrollevel)
        #inst = TbSetting.objects.get(settingname='RiskControlLevel')
        #ls = json.loads(inst.settingvalue)
        for row in ls:
            row['_director_name']='RiskcontrolForm'
            row['pk']=row['Level']
            row['meta_merchant'] = self.search_args.get('merchant')
        return ls

class RiskcontrolForm(Fields):
    def get_heads(self):
        return [
            {'name':'Level','label':'风控等级','editor':'number','readonly':True},
            {'name':'Memo','label':'备注','editor':'linetext','readonly':True},
            {'name':'RechargeDays','label':'充值天数','editor':'com-field-number','required':True,'fv_rule':'number'},
            {'name':'RechargeCount','label':'充值次数','editor':'com-field-number','required':True,'fv_rule':'number'},
            {'name':'RechargeAmount','label': '充值金额','editor':'com-field-number','required':True,'fv_rule':'number'},
            #{'name':'PossibleWinAmount','label':'可赢额','editor':'com-field-number','required':True,'fv_rule':'number'},
            #{'name':'DelaySec','label':'投注延时(秒)','editor':'com-field-number','required':True,'fv_rule':'number'}
        ]
    
    def save_form(self):
        prop = TbMerchantproperties.objects.get(merchant_id = self.kw.pop('meta_merchant'))
        ls = json.loads(prop.riskcontrollevel)
        for item in ls:
            if item['Level'] == self.kw.get('Level'):
                item.update({
                    'RechargeDays':self.kw.get('RechargeDays'),
                    'RechargeCount':self.kw.get('RechargeCount'),
                    'RechargeAmount':self.kw.get('RechargeAmount'),
                })
                self.rt_value = item
        prop.riskcontrollevel = json.dumps(ls,ensure_ascii=False)
        prop.save()
        
        #inst = TbSetting.objects.get(settingname='RiskControlLevel')
        #ls = json.loads(inst.settingvalue)
        #self.kw.pop('_director_name')
        #for item in ls:
            #if item['Level']==self.kw.get('Level'):
                #item.update(self.kw)
                #self.rt_value =item
        #inst.settingvalue=json.dumps(ls)
        #inst.save()
        #self.instance = inst
    
    def get_row(self):
        return self.rt_value
    
    
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
    'RiskcontrolSetting':RiskContralTab,
    'RiskcontrolForm':RiskcontrolForm,
})

page_dc.update({
    'RiskcontrolSetting':RiskcontrolSetting
})