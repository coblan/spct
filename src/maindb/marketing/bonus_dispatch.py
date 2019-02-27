from helpers.director.shortcut import TablePage,ModelFields,page_dc,ModelTable,director,RowFilter,RowSearch
from ..models import TbBonuslog,TbBonustype,TbBalancelog
from ..riskcontrol.black_users import AccountSelect
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import Q
import json
import logging
modelfields_log = logging.getLogger('ModelFields.save_form')

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
                        'ops': bonus_form.get_operations(),
                        'row_express':'rt={_director_name:"bonuslog_list.edit"}',
                        'after_save_express':'rt=scope.vc.row={_director_name:"bonuslog_list.edit"}'
                    },
                    #{
                        #'name':'bonus-type-form',
                        #'label':'红利类型',
                        #'com': 'com-tab-fields',
                        #'heads': bonus_type_form.get_heads(),
                        #'ops': bonus_type_form.get_operations()                        
                    #},
                    {'name': 'bonustype-list',
                     'label': '红利类型',
                     'com': 'com-tab-table',
                     'table_ctx': BonusTypeTable(crt_user=self.request.user).get_head_context(),
                     'visible': True#can_touch(TbBalancelog, self.crt_user),
                    },
                    {'name': 'bonuselog_list',
                     'label': '红利日志',
                     'com': 'com-tab-table',
                     'table_ctx': BonuslogTable(crt_user=self.request.user).get_head_context(),
                     'visible': True#can_touch(TbBalancelog, self.crt_user),
                    },
                ]
            },
            'tab_ctx':'bonustabs',
            'tab_name':'bonus-form'
        }
        return ctx
    
class BonuslogForm(ModelFields):
    hide_fields=['createuser','withdrawlimitamount']
    class Meta:
        model = TbBonuslog
        exclude=[]
    
    def clean_dict(self, dc):
        dc['createuser']=self.crt_user.pk
        if dc.get('bonustypeid'):
            amount = dc.get('amount')
            bonustype = TbBonustype.objects.get(bonustypeid=dc.get('bonustypeid'))
            multi = bonustype.withdrawlimitmultiple
            total_mount = Decimal(amount)  * multi
            dc['withdrawlimitamount'] =  total_mount 
        return dc
    
    def dict_head(self, head):
        if head['name'] == 'accountid':
            table_obj = AccountSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
            head['options'] = []
        return head
    
    def get_operations(self):
        ops = super().get_operations()
        if ops:
            ops[0].update({
                'label':'发放红利',
                'class':'btn btn-sm btn-primary',
                'icon':'',
            })

        return ops
    
    def clean_save(self):
        account = self.instance.accountid
        before = account.amount
        account.amount += self.instance.withdrawlimitamount
        account.save()
        ban = TbBalancelog.objects.create(accountid=self.instance.accountid,
                                    categoryid_id=37,
                                    cashflow=1,
                                    account=self.instance.accountid.account,
                                    beforeamount=before,
                                    afteramount = account.amount,amount=self.instance.withdrawlimitamount,
                                    creater=str(self.crt_user),
                                    memo='红利发放'
                                    )
        self.op_log.update({
            'clean_save_desp':'生成了对应的TbBalancelog.pk=%s,计算了用户余额'%ban.pk
        })
    
    

class BonuslogTable(ModelTable):
    model = TbBonuslog
    exclude=[]
    
    def get_operation(self):
        return []
    
    def dict_head(self, head):
        dc={
            'bonustypeid':200,
            'createtime':160,
            'accountid':120,
        }
        if dc.get(head['name']):
            head['width']=dc.get(head['name'])
        return head
    
    class filters(RowFilter):
        names=['bonustypeid','createuser']
        range_fields=['createtime']
        
        def dict_head(self, head):
            if head['name']=='createuser':
                for user_dc in TbBonuslog.objects.values('createuser').distinct():
                    user = User.objects.get(pk = user_dc.get('createuser'))
                    head['options'].append(
                        {'value':user.pk,'label':str(user)}
                    )
                    head['label']='创建人'
            return head
    
    class search(RowSearch):
        names = [ 'accountid__nickname']

        def get_context(self):
            return {'search_tip': '用户昵称',
                    'editor': 'com-search-filter',
                    'name': '_q'
                    }

        def get_query(self, query):
            if self.q:
                exp = None
                ls = self.valid_name + ['accountid__nickname']
                for name in ls:
                    kw = {}
                    kw['%s__icontains' % name] = self.q
                    if exp is None:
                        exp = Q(**kw)
                    else:
                        exp = exp | Q(**kw)
                return query.filter(exp)
            else:
                return query
  

class BonusTypeTable(ModelTable):
    model = TbBonustype
    exclude=[]
    pop_edit_field='bonustypeid'
    
    def dict_row(self, inst):
        return {
            'createtime':str(inst.createtime)
        }
    
    def dict_head(self, head):
        dc={
            'bonustypename':250,
            'createtime':160,
        }
        if dc.get(head['name']):
            head['width']=dc.get(head['name'])
        return head    
    

class BonusTypeForm(ModelFields):
    hide_fields=['createuser']
    class Meta:
        model = TbBonustype
        exclude=[]
        
    def clean_dict(self, dc):
        dc['createuser']=self.crt_user.pk
        return super().clean_dict(dc)    

director.update({
    'bonuslog_list':BonuslogTable,
    'bonuslog_list.edit':BonuslogForm,
    
    'bonustype':BonusTypeTable,
    'bonustype.edit':BonusTypeForm,
})

page_dc.update({
    'bonuspage':BonusPage
})