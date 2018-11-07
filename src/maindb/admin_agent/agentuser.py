from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, RowFilter, RowSort, RowSearch, Fields, ModelFields
from helpers.director.table.row_search import SelectSearch
from ..models import TbAccount
from django.db import connections
from django.utils import timezone
from ..member.account import account_tab
from helpers.director.access.permit import has_permit
from django.core.exceptions import PermissionDenied
from ..alg import encode_paswd

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
        fields_sort = ['accountid', 'NickName', 'SumActive', 'AgentAmount', 'BeaeAmount', 'AgentRuleAmount',
                       'BalanceLostAmount', 'SumLostAmount', 'BonusRate', 'SumBonusAmount', 'SumExpend',
                       'SumRechargeAmount', 'Poundage', 'AgentRulePercentage', 'SumBetAmount', 'SumWithdrawalAmount',
                       'SumTurnover', 'CreateTime']

        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')
            search_args['_start_createtime'] = search_args.get('_start_createtime') or def_start
            search_args['_end_createtime'] = search_args.get('_end_createtime') or def_end
            return search_args
        
        
        class filters(RowFilter):
            range_fields = ['createtime']

            def dict_head(self, head):
                if head['name'] == 'createtime':
                    head['label'] = '产生时间'
                return head

        class sort(RowSort):
            names = ['AgentAmount', 'BeaeAmount', 'SumActive', 'AgentRuleAmount', 'BalanceLostAmount', 'SumLostAmount',
                     'SumBonusAmount', 'SumWithdrawalAmount', 'SumBetAmount', 'Poundage',
                     'SumTurnover', 'BonusRate', 'SumExpend', 'SumRechargeAmount', 'AgentRulePercentage']

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
            sql_args = {
                'AccountID': par,
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'BeginDate': self.search_args.get('_start_createtime', ''),
                'EndDate': self.search_args.get('_end_createtime', ''),
                'NickName': nickname,
                'OrderBy': order_by,
            }

            sql = "exec dbo.SP_AgentUser %(AccountID)s,%(PageIndex)s,%(PageSize)s,'%(BeginDate)s','%(EndDate)s',%%s,'%(OrderBy)s'" \
                  % sql_args
            
            #print(sql)
            
            with connections['Sports'].cursor() as cursor:
                self.parent_agents = []
                self.child_agents = []
                try:
                    cursor.execute(sql, [nickname])
                except Exception as e:
                    print(e)
                    msg = str(e)
                    if '没有查到这个昵称' in msg:
                        msg = '没有查到这个昵称'
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
                    self.footer = ['合计'] + self.footer_by_dict(footer)
                            
            # 保持 _par参数为空状态，可以判断 前端操作是 搜索or点击

        def dict_head(self, head):
            if head['name'] == 'SumActive':
                head['editor'] = 'com-table-call-fun'
                head['fun'] = 'get_childs'
                head['field'] = 'accountid'
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'baseinfo'
            return head

        def getExtraHead(self):
            return [
                # {'name': 'accountid', 'label': '账号ID ', 'width': 100, },
                {'name': 'NickName', 'label': '昵称 ', 'width': 100, },
                # {'name': 'VIPLv', 'label': 'VIP等级', },
                {'name': 'SumActive', 'label': '活跃用户数', 'width': 100, },
                {'name': 'AgentAmount', 'label': '预估佣金', },
                {'name': 'BeaeAmount', 'label': '佣金计算基数', 'width': 120, },
                {'name': 'AgentRuleAmount', 'label': '佣金计算金额', 'width': 120, },
                {'name': 'BalanceLostAmount', 'label': '累计净盈利', 'width': 100, },
                {'name': 'SumLostAmount', 'label': '本月净盈利', 'width': 100, },
                {'name': 'BonusRate', 'label': '返水比例', },
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
                row['accountid'] = row['AccountID']
                row['NickName'] = row['NickName']
                row['BeaeAmount'] = round(row['BeaeAmount'] or 0, 2)
                row['BonusRate'] = round(row['BonusRate'] or 0, 3)
                row['Poundage'] = round(row['Poundage'] or 0, 2)
                row['AgentRuleAmount'] = round(row['AgentRuleAmount'] or 0, 2)
                row['BalanceLostAmount'] = round(row['BalanceLostAmount'] or 0, 2)
                row['AgentAmount'] = round(row['AgentAmount'] or 0, 2)
                row['SumExpend'] = round(row['SumExpend'] or 0, 2)
                row['AgentRulePercentage'] = round(row['AgentRulePercentage'] or 0, 3)
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

        def get_context(self):
            ctx = super().get_context()
            ctx['tabs'] = account_tab(self)
            return ctx

        def get_operation(self):
            agent = NewAgentUserForm(crt_user= self.crt_user)
            return [
                {'fun': 'create_child_row', 'par_field': 'parentid','editor': 'com-op-btn' ,
                 'after_save': 'refresh',
                 'label': '创建下级用户','fields_ctx': agent.get_head_context(),}, 
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]

class NewAgentUserForm(ModelFields):
    hide_fields = ['accountid']
    class Meta:
        model = TbAccount
        fields = ['phone', 'nickname', 'bonusrate', 'accountid']
    
    def getExtraHeads(self): 
        return [
            {'name':'pswd','editor':'password','label':'密码','required':True,'fv_rule':'密码:', 'help_text': '请不要输入过于简单的密码，否则会禁止用户登录',},
            {'name':'pswd2','editor':'password','label':'确认密码','required':True,'fv_rule':'match(pswd)'},
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
    
    def clean(self): 
        phone = self.cleaned_data.get('phone')
        if TbAccount.objects.filter(phone = phone).exists():
            self.add_error('phone', '手机号码已经存在')
        nickname =  self.cleaned_data.get('nickname')
        if TbAccount.objects.filter(nickname = nickname).exists():
            self.add_error('nickname', '昵称已经存在')
        parentid = self.kw.get('carry_parents')[-1]['value']
        parent = TbAccount.objects.get(accountid = parentid)
        self.catch_parent = parent
        
        if parent.bonusrate < self.cleaned_data.get('bonusrate'):
            self.add_error('bonusrate', '反水不能超过上级用户的反水：%s' % parent.bonusrate)
        
    def clean_dict(self, dc): 
        dc = super().clean_dict(dc)
        if not dc.get('accountid'):
            sql = 'SELECT NEXT VALUE FOR  dbo.SQ_AccountID'
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                bb = cursor.fetchall()           
                dc['accountid'] = bb[0][0]
        
        return dc
    
    def clean_save(self): 
        parentid = self.kw.get('carry_parents')[-1]['value']
        self.instance.parentid = parentid
        self.instance.account = self.instance.phone
        self.instance.agent = self.catch_parent.agent
        self.instance.password = encode_paswd(self.kw.get('pswd'))
        self.instance.status = 1

    

director.update({
    'AgentUser': AgentUser.tableCls,
    'new_AgentUser': NewAgentUserForm,
})

page_dc.update({
    'agent_user': AgentUser,
})
