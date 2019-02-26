from helpers.director.shortcut import TablePage,ModelFields,page_dc
from ..models import TbBonuslog,TbBonuslog

class BonusPage(object):
    def __init__(self,request,engin):
        self.request = request
        
    def get_template(self,prefer=None):
        return 'jb_admin/tabs.html'
    
    def get_label(self):
        return '红利发放'
    
    def get_context(self):
        bonus_form = BonuslogForm(crt_user=self.request.user)
        ctx ={
            'named_ctx' :{
                'bonustabs':[
                    {
                        'name':'bonus-form',
                        'label':'红利发放',
                        'com': 'com-tab-fields',
                        'heads': bonus_form.get_heads(),
                        'ops': bonus_form.get_operations()
                    }
                ]
            },
            'tab_ctx':'bonustabs',
            'tab_name':'bonus-form'
        }
        return ctx
    
class BonuslogForm(ModelFields):
    class Meta:
        model = TbBonuslog
        exclude=[]


page_dc.update({
    'bonuspage':BonusPage
})