from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, RowFilter, RowSort, RowSearch, Fields, ModelFields,director_view,director_element
from helpers.director.table.row_search import SelectSearch
from ..models import TbAccount,TbAgentrules,TbMerchants
from django.db import connections
from django.utils import timezone
from ..member.account import account_tab
from helpers.director.access.permit import has_permit
from django.core.exceptions import PermissionDenied
from ..alg import encode_paswd
from ..riskcontrol.black_users import AccountSelect
from dateutil.relativedelta import relativedelta
import logging
modelfields_log = logging.getLogger('ModelFields.save_form')
from maindb.member.account import UserPicker,can_touch,User
from hello.merchant_user import get_user_merchantid,MerchantInstancCheck
from helpers.director.access.permit import can_write

class AgentUser(TablePage):
    template = 'jb_admin/table.html'
    
    def check_permit(self): 
        if not has_permit(self.crt_user, 'agent'):
            raise PermissionDenied('没有权限访问代理用户列表')
    
    def get_label(self):
        return '代理用户'

    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid','createtime']
        fields_sort = ['accountid', 'NickName', 'SumActive',  'BeaeAmount', 'AgentRulePercentage','AgentAmount',
                       'BalanceLostAmount', 'SumLostAmount', 'bonusrate', 'SumBonusAmount', 'SumExpend',
                       'SumRechargeAmount', 'Poundage', 'SumBetAmount', 'SumWithdrawalAmount',
                       'SumTurnover', 'CreateTime']

        @classmethod
        def clean_search_args(cls, search_args):
            if not search_args.get('createtime'):
                today = timezone.now()
                #sp = timezone.timedelta(days=30)
                #last = today - sp
                #def_start = last.strftime('%Y-%m-%d')
                #def_end = today.strftime('%Y-%m-%d')
                #search_args['_start_createtime'] = search_args.get('_start_createtime') or def_start
                #search_args['_end_createtime'] = search_args.get('_end_createtime') or def_end
                search_args['createtime'] = today.strftime('%Y-%m')
            if not search_args.get('accounttype'):
                search_args['accounttype'] = 0
            return search_args
        
        
        class filters(RowFilter):
            #range_fields = ['createtime']
            names=['createtime']

            def dict_head(self, head):
                if head['name'] == 'createtime':
                    head['label'] = '产生时间'
                    head['editor']='com-filter-month'
                    head['show_label']= True
                return head
            
            def getExtraHead(self):
                return [
                    {'name':'MerchantId','label':'商户','editor':'com-filter-select','options':[
                        {'value':x.pk,'label':str(x)} for x in TbMerchants.objects.all()
                        ],'visible': not bool( self.crt_user.merchant )},
                    {'name':'accounttype','placeholder':'用户类型','editor':'com-filter-select','required':True,'options':[
                        #{'value':'NULL','label':'全部'},
                        {'value':'0','label':'普通'},
                        {'value':'1','label':'内部'}
                    ]}
                ]

        class sort(RowSort):
            names = ['AgentAmount', 'BeaeAmount', 'SumActive', 'BalanceLostAmount', 'SumLostAmount',
                     'SumBonusAmount', 'SumWithdrawalAmount', 'SumBetAmount', 'Poundage',
                     'SumTurnover', 'bonusrate', 'SumExpend', 'SumRechargeAmount','CreateTime']

        class search(SelectSearch):
            names = ['nickname']

            def get_option(self, name):
                if name == 'nickname':
                    return {'value': 'nickname', 'label': '用户昵称', }
                else:
                    return super().get_option(name)

        def getData(self):
            """
            @AccountID INT,    --用户编号  
            @PageIndex INT =1,    --页码   默认1  
            @PageSize INT =10,    --页条数 默认10  
            @BeginDate DATE=NULL,   --查询开始时间 默认上月今天  
            @EndDate DATE=NULL,   --查询结算时间 默认今天  
            @NickName VARCHAR(20) =NULL --帐号查询昵称 默认全部  
            @AccountType INT (NULL 0 1) 全部/普通/内部
            """
            order_by = self.search_args.get('_sort', '')
            par = self.search_args.get('_par', 0)
            nickname = self.search_args.get('_q', '')

            cach_par = self.search_args.get('_cach_par')
            cach_nickname = self.search_args.get('_cach_nickname')
            cach_sort = self.search_args.get('_cach_sort')

            self.search_args['_cach_nickname'] = nickname
            self.search_args['_cach_par'] = par
            self.search_args['_cach_sort'] = order_by
            
            
            if par != cach_par:
                # 点击的par
                nickname = ''
                order_by = ''
                self.search_args['_cach_op'] = 'click_par'
                self.search_args['_q'] =''

            elif nickname and cach_nickname != nickname:
                # 搜索昵称，第一次点击[搜索]
                par = 0
                order_by = ''
                self.search_args['_cach_op'] = 'search_nickname'
            elif order_by != cach_sort:
                # 排序
                cach_op = self.search_args.get('_cach_op')
                if cach_op == 'click_par':
                    nickname = ''
                elif cach_op == 'search_nickname':
                    par = 0
            else:
                # 点击 [搜索] 刷新
                pass

            if order_by.startswith('-'):
                order_by = order_by[1:] + ' DESC'
            
            createdate = timezone.datetime.strptime( self.search_args.get('createtime'),'%Y-%m')
            start_date = createdate.strftime('%Y-%m-%d')
            end_date = (createdate+ relativedelta(months=1) ).strftime('%Y-%m-%d')
            AccountType = self.search_args.get('accounttype')
            
            if self.crt_user.merchant:
                merchantid = self.crt_user.merchant.id
            else:
                merchantid = self.search_args.get('MerchantId','null')
            
            sql_args = {
                'MerchantId':merchantid,
                'AccountID': par,
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'BeginDate':start_date, #self.search_args.get('_start_createtime', ''),
                'EndDate':end_date, #self.search_args.get('_end_createtime', ''),
                'NickName': nickname,
                'AccountType':AccountType,
                'OrderBy': order_by,
            }

            sql = "exec dbo.SP_AgentUser %(MerchantId)s,%(AccountID)s,%(PageIndex)s,%(PageSize)s,'%(BeginDate)s','%(EndDate)s',%%s,%(AccountType)s,'%(OrderBy)s'" \
                  % sql_args
            
            #print(sql)
            
            with connections['Sports'].cursor() as cursor:
                self.parent_agents = []
                self.child_agents = []
                try:
                    cursor.execute(sql, [nickname])
                except Exception as e:
        
                    msg = str(e)
                    if  'The nickname was not found' in msg:
                        msg = '没有查到这个昵称'

                    #if '没有查到这个昵称' in msg:
                        #msg = '没有查到这个昵称'
                    raise UserWarning(msg)
                
                #print('顺利走过 execute')
                
                
                for par in cursor:
                    self.parent_agents.append({'value': par[3], 'label': par[1], })
                #print('获取到的代理数为 %s' % len(self.parent_agents))
                
                self.parent_agents.append({'value': 0, 'label': '根用户', })
                self.parent_agents.reverse()

                cursor.nextset()
                
                for row in cursor:
                    dc = {}
                    for index, desp_item in enumerate(cursor.description):
                        head_name = desp_item[0]
                        dc[head_name] = row[index]
                    self.child_agents.append(dc)
                if self.child_agents:
                    row1 = self.child_agents[0]
                    footer = {}
                    for k, v in row1.items():
                        if k != 'Total' and k.startswith('Total'):
                            normed_v = v or 0
                            footer[k[5:]] = round(normed_v, 2)
                    self.footer = footer #['合计'] + self.footer_by_dict(footer)
                            
            # 保持 _par参数为空状态，可以判断 前端操作是 搜索or点击

        def dict_head(self, head):
            if head['name'] == 'NickName': #'SumActive':
                head['editor'] = 'com-table-call-fun'
                head['fun'] = 'get_childs'
                head['arg_filter'] = 'field'
                head['field'] = 'accountid'
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'baseinfo'
                head['ctx_name'] = 'account_tabs'
            return head

        def getExtraHead(self):
            return [
                # {'name': 'accountid', 'label': '账号ID ', 'width': 100, },
                {'name': 'NickName', 'label': '昵称 ', 'width': 100, },
                # {'name': 'VIPLv', 'label': 'VIP等级', },
                {'name': 'SumActive', 'label': '活跃用户数', 'width': 100, },
                
                {'name': 'BeaeAmount', 'label': '佣金计算基数', 'width': 120, },
                #{'name': 'AgentRuleAmount', 'label': '佣金计算比例', 'width': 120, },
                {'name': 'AgentAmount', 'label': '预估佣金', },
                {'name': 'BalanceLostAmount', 'label': '累计净盈利', 'width': 100, },
                {'name': 'SumLostAmount', 'label': '本月净盈利', 'width': 100, },
                {'name': 'bonusrate', 'label': '返水比例', },
                {'name': 'SumBonusAmount', 'label': '返水', 'width': 80, },
                {'name': 'SumExpend', 'label': '系统红利', 'width': 80, },
                {'name': 'SumRechargeAmount', 'label': '充值金额', 'width': 100, },
                {'name': 'Poundage', 'label': '充值手续费', 'width': 100, },
                {'name': 'AgentRulePercentage', 'label': '佣金比例', },
                {'name': 'SumBetAmount', 'label': '投注金额', 'width': 120, },
                {'name': 'SumWithdrawalAmount', 'label': '提现金额', 'width': 100, },
                {'name': 'SumTurnover', 'label': '流水', 'width': 120, },
                {'name': 'CreateTime', 'label': '创建时间', 'width': 140, },
            ]

        def get_rows(self):
            self.getData()
            for row in self.child_agents:
                row['pk'] = row['AccountID']
                row['accountid'] = row['AccountID']
                row['NickName'] = row['NickName']
                row['BeaeAmount'] = round(row['BeaeAmount'] or 0, 2)
                row['bonusrate'] = round(row['BonusRate'] or 0, 3)
                row['Poundage'] = round(row['Poundage'] or 0, 2)
                #row['AgentRuleAmount'] = round(row['AgentRuleAmount'] or 0, 2)
                row['BalanceLostAmount'] = round(row['BalanceLostAmount'] or 0, 2)
                row['AgentAmount'] = round(row['AgentAmount'] or 0, 2)
                row['SumExpend'] = round(row['SumExpend'] or 0, 2)
                row['AgentRulePercentage'] = round(row['AgentRulePercentage'] or 0, 2)
                row['SumLostAmount'] = round(row['SumLostAmount']or 0, 2)
                row['SumBonusAmount'] = round(row['SumBonusAmount'] or 0, 2)
                row['SumBetAmount'] = round(row['SumBetAmount'] or 0, 2)
                row['SumRechargeAmount'] = round(row['SumRechargeAmount'] or 0, 2)
                row['SumWithdrawalAmount'] = round(row['SumWithdrawalAmount'] or 0, 2)
                row['SumTurnover'] = round(row['SumTurnover'] or 0, 2)

            return self.child_agents

        def getRowPages(self):
            if self.child_agents:
                total = self.child_agents[0]['Total']
            else:
                total = 0

            return {
                'crt_page': self.search_args.get('_page', 1),
                'total': total,
                'perpage': self.search_args.get('_perpage', 20)
            }

        # def get_context(self):
        # ctx = super().get_context()
        # ctx['parents'] = self.parent_agents
        # return ctx

        def getParents(self):
            return self.parent_agents

        def get_event_slots(self):
            ls = [
                {'event':'parent_changed','express':'scope.ps.search_args._q=""'}
              ]      
            return ls
        
        def get_context(self):
            ctx = super().get_context()
            ctx['named_ctx'] = account_tab(self)
            return ctx

        def get_operation(self):
            agent = NewAgentUserForm(crt_user= self.crt_user)
            yong = YongJingForm(crt_user=self.crt_user)
            par_form = ParentForm(crt_user=self.crt_user)
            changeable_fields = self.permit.changeable_fields()
            return [
                {'fun': 'add_new', 'editor': 'com-op-btn' ,
                 'after_save': 'rt=scope.ps.search()', #'preset':'rt={meta_only_add_root_next_level:1}',
                 'preset':'rt={meta_par:scope.ps.parents[scope.ps.parents.length-1].value}',
                 'disabled':'scope.ps.parents.length>2',
                 'label': '创建代理用户','fields_ctx': agent.get_head_context(),
                 'visible':can_write(TbAccount, self.crt_user),
                 }, 
                #{'fun': 'add_new', 'editor': 'com-op-btn' ,
                 #'after_save': 'rt=scope.search()',
                 #'label': '创建下级用户','fields_ctx': agent.get_head_context(),}, 
                 
                {'fun': 'selected_set_and_save', 
                 'editor': 'com-op-btn' ,
                 'after_save': 'rt=scope.ps.search()',
                 'row_match':'one_row',
                 'match_express':'scope.row.AgentStatus == 1',
                 'match_msg':'只有代理用户才能修改佣金比例',
                 'label': '修改佣金比例',
                 'fields_ctx': yong.get_head_context(),
                  'visible':can_write(TbAccount, self.crt_user),
                  }, 
                 
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', },
                
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn' ,
                 'after_save': 'rt=scope.ps.search()','row_match':'many_row',
                 'label': '修改上级','fields_ctx': par_form.get_head_context(),
                 'visible':has_permit(self.crt_user, 'agent.parent.edit')}, 
                {'editor':'com-op-btn','label':'选择客服',
                 'visible':  has_permit(self.crt_user, 'agent.csuserid-btn'),#'csuserid' in changeable_fields and can_touch(User,self.crt_user),
                 'table_ctx':UserPicker().get_head_context(),
                 'row_match':'many_row',
                 'action':''' cfg.pop_vue_com("com-table-panel",scope.head.table_ctx)
            .then((row)=>{
                cfg.show_load()
                var accounts = ex.map(scope.ps.selected,(item)=>{return item.AccountID})
                return ex.director_call("agent/change-customer-server",{accounts:accounts,csuserid:row.pk})
                
            }).then(()=>{
                cfg.hide_load()
                cfg.toast("操作完成")
                scope.ps.selected = []
                 })
                 
                 '''}
            ]

 #ex.each(scope.ps.selected,account=>{
                     #account.csuserid = row.pk
                     #account._csuserid_label = row.first_name+'('+ row.username +')'
                     #account.meta_change_fields='csuserid'
                 #})
                 #cfg.show_load()
                 
                 #return ex.director_call('d.save_rows',{rows:scope.ps.selected})


@director_view('agent/change-customer-server')
def change_customer_server(accounts,csuserid):
    TbAccount.objects.filter(accountid__in=accounts).update(csuserid=csuserid)



@director_element('YongJingForm')
class YongJingForm(Fields):
    """用于修改佣金"""
    def get_heads(self):
        return [
            {'name':'AgentRulePercentage','editor':'number','label':'佣金比例','step':0.01,'required':True,'fv_rule':'range(0~0.4),digit(2)'},
        ]
    
    def get_row(self):
        return self.kw
        
    def save_form(self):
        AgentRulePercentage = self.kw.get('AgentRulePercentage',0)
        agent_rule,_ = TbAgentrules.objects.get_or_create(accountid=self.kw.get('accountid'),status=1)
        agent_rule.percentage = AgentRulePercentage
        agent_rule.save()
        modelfields_log.info('修改账号%(accountid)s的佣金比例为%(percentage)s'%{'accountid':self.kw.get('accountid'),'percentage':AgentRulePercentage})

@director_element('agent.parentselect')
class ParentSelect(AccountSelect):
    def inn_filter(self, query):
        query = super().inn_filter(query)
        return query.filter(agentstatus=1)

@director_element('agent.ParentForm')
class ParentForm(Fields):
    """调整父亲"""
    #class Meta:
        #model=TbAccount
        ##exc=['parentid']
        #exclude=[]
    
    #def dict_head(self, head):
        
        #if head['name']=='parentid':
            #table_obj = AccountSelect(crt_user=self.crt_user)
            #head['editor']='com-field-pop-table-select'
            #head['select_field']='account'
            #head['required']=True
            #head['table_ctx']=table_obj.get_head_context()
            #head['options']=[]
        #return head
    
    def get_heads(self):
        table_obj = ParentSelect(crt_user=self.crt_user)
        return [
            {'name':'parentid',
             'editor':'com-field-pop-table-select',
             'label':'上级账号',
             'select_field':'account',
             'required':True,
             'table_ctx':table_obj.get_head_context(),'options':[]},
        ]
    
    def save_form(self):
        
        accout = TbAccount.objects.get(accountid=self.kw.get('AccountID') )
        if accout.accountid == self.kw.get('parentid'):
            raise UserWarning('不能选择自己作为自己的上级')
        old_parentid = accout.parentid
        old_source = accout.source
        accout.parentid = self.kw.get('parentid')
        accout.source = 4
        accout.save()
        modelfields_log.info('修改账号%(accountid)s的上级从%(old_parentid)s改为%(parentid)s,source从%(old_source)s为4'%{'accountid':accout.accountid,'parentid':accout.parentid,
                                                                                                                        'old_parentid':old_parentid,'old_source':old_source})
        
        
    


class NewAgentUserForm(MerchantInstancCheck,ModelFields):
    """新建"""
    hide_fields = ['accountid']
    
    @property
    def field_sort (self):
        if self.crt_user.merchant:
            return ['phone', 'nickname', 'accountid','AgentRulePercentage','groupid','pswd','pswd2']
        else:
            return  ['merchant','phone', 'nickname', 'accountid','AgentRulePercentage','groupid','pswd','pswd2']
    #field_sort=['phone', 'nickname', 'accountid','AgentRulePercentage','groupid','pswd','pswd2']
    class Meta:
        model = TbAccount
        fields = ['phone', 'nickname', 'accountid','groupid','merchant']
    
    def getExtraHeads(self): 
        return [
            {'name':'pswd','editor':'password','label':'密码','required':True,'fv_rule':'密码:', 'help_text': '请不要输入过于简单的密码，否则会禁止用户登录',},
            {'name':'pswd2','editor':'password','label':'确认密码','required':True,'fv_rule':'match(pswd)'},
            
            {'name':'AgentRulePercentage','editor':'number','label':'佣金比例','required':True,'fv_rule':'range(0~0.4)'},
        ]
    
    def dict_head(self, head): 
        if head['name'] == 'phone':
            head['required'] = True
            head['fv_rule'] = 'mobile'
        if head['name'] == 'nickname':
            head['required'] = True
        if head['name'] == 'bonusrate':
            head['fv_rule'] = 'range(0~0.01)'
            head['step'] = 0.001
        return head
    
    #def get_heads(self): 
        #return [
            #{'name':'Phone','editor':'linetext','label':'手机号码','required':True,'fv_rule':'mobile'},
            #{'name':'pswd','editor':'password','label':'密码','required':True,'fv_rule':'密码:'},
            #{'name':'pswd2','editor':'password','label':'确认密码','required':True,'fv_rule':'match(pswd)'},
            #{'name':'NickName','editor':'linetext','label':'昵称','width':120,'required':True},
            #{'name':'BonusRate','editor':'number','label':'反水','step':0.001,'fv_rule':'range(0~0.01)'},
        #]
    
    #def get_row(self): 
        #return {
            #'_director_name': self.get_director_name(),
        #}
        
    def dict_row(self, inst):
        return {
            'NickName':inst.nickname,
            'CreateTime':inst.createtime,
            'AgentStatus':inst.agentstatus,
        }
    
    def clean(self): 
        super().clean()
        phone = self.cleaned_data.get('phone')
        if TbAccount.objects.filter(phone = phone,merchant_id = self.kw.get('merchant')).exists():
            self.add_error('phone', '手机号码已经存在')
        nickname =  self.cleaned_data.get('nickname',)
        if TbAccount.objects.filter(nickname = nickname,merchant_id = self.kw.get('merchant')).exists():
            self.add_error('nickname', '昵称已经存在')
        if False : #self.kw.get('meta_only_add_root_next_level'):
            parentid = 0
            parent = TbAccount.objects.get(accountid = parentid)
        else:
            #  老的  创建下级用户的逻辑 --- 现在又恢复了。
            parentid = self.kw.get('meta_par', 0)
            parent = TbAccount.objects.get(accountid = parentid)
            #if parent.bonusrate < self.cleaned_data.get('bonusrate'):
                #self.add_error('bonusrate', '反水不能超过上级用户的反水：%s' % parent.bonusrate)
        self.catch_parent = parent
        
    def clean_dict(self, dc): 
        dc = super().clean_dict(dc)
        if not dc.get('accountid'):
            sql = 'SELECT NEXT VALUE FOR  dbo.SQ_AccountID'
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                bb = cursor.fetchall()           
                dc['accountid'] = bb[0][0]
        if self.crt_user.merchant:
            dc['merchant'] = self.crt_user.merchant.id
        return dc
    
    def clean_save(self): 
        #parentid = self.kw.get('meta_par', 0)
        self.instance.parentid = self.catch_parent.accountid
        self.instance.account = self.instance.phone
        self.instance.agent = self.catch_parent.agent
        self.instance.password = encode_paswd(self.kw.get('pswd'))
        self.instance.status = 1
        self.instance.agentstatus=1
        agent_rule,_ = TbAgentrules.objects.get_or_create(accountid=self.instance.accountid,status=1)
        agent_rule.minamount=1
        agent_rule.maxamount=999999999
        agent_rule.status=1
        agent_rule.percentage= self.kw.get('AgentRulePercentage',0)
        agent_rule.save()
        modelfields_log.info('创建账号%(accountid)s的佣金比例为%(percentage)s'%{'accountid':agent_rule.accountid,'percentage':agent_rule.percentage})

    

director.update({
    'AgentUser': AgentUser.tableCls,
    'new_AgentUser': NewAgentUserForm,
})

page_dc.update({
    'agent_user': AgentUser,
})
