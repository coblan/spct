# encoding:utf-8
from __future__ import unicode_literals

import re

from django.db.models import Sum, Case, When, F,Count,OuterRef,Subquery
from django.utils.translation import ugettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter, director,field_map,model_to_name,Fields,get_request_cache,PlainTable,director_element
from helpers.director.table.row_search import SelectSearch
from maindb.matches.matches_statistics import MatchesStatisticsPage
from maindb.money.balancelog import BalancelogPage
from ..models import TbAccount, TbBalancelog, TbLoginlog, TbTicketmaster, TbBankcard, TbRecharge, TbWithdraw, TbMatch,TbBetfullrecord,TbUserLog
from helpers.func.collection.container import evalue_container
from helpers.director.access.permit import can_touch,has_permit
from helpers.func.random_str import get_str, get_random_number
from helpers.director.model_func.field_procs.decimalproc import DecimalProc
from django.db import connections
import hashlib
from decimal import Decimal
from ..matches.ticket_master import TicketMasterPage
from ..member.bankcard import BankCard, BankCardForm
from ..money.recharge import RechargePage
from ..money.withdraw import WithdrawPage
from .loginlog import LoginLogPage
from ..report.user_statistics import UserStatisticsPage
from maindb.send_phone_message import send_message_password, send_message_fundspassword
from django.db.models import DecimalField
from ..models import TbMoneyCategories,TbSetting,TbRisklevellog,TbAgprofitloss
import json
from maindb.rabbitmq_instance import notifyAccountFrozen
from helpers.case.jb_admin.admin import UserPicker
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from . relevent_user import ReleventUserPage
from ..ag.profitloss import AgprofitlossPage
from django.conf import settings
from .userlog import UserlogPage

def account_tab(self):
    baseinfo = AccoutBaseinfo(crt_user=self.crt_user)
    ls = [
        {'name':'dashborad',
         'label':'数据看板',
         'editor':'com-tab-chart',
         'table_ctx':SingleUserStatistic().get_head_context(),
         'pre_set':'rt={accountid:scope.par_row.accountid}',
         'foot_heads':[{'name':'Profit','label':'盈利'},{'name':'BetAmount','label':'投注金额'},
                       {'name':'BetOutcome','label':'派奖金额'},{'name':'ProfitRate','label':'盈利率'},
                       {'name':'WinRate','label':'中注率'},
                       {'name':'RechargeAmount','label':'充值'},{'name':'WithdrawAmount','label':'提现'}],
         'chart_heads':[
            {'name':'xx','editor':'com-chart-plain','xdata':'Date','ydata':[{'name':'BetAmount','label':'投注金额','type':'line',},
                                                                              {'name':'BetOutcome','label':'派奖金额','type':'line','color':'#27B6AC'},
                                                                              {'name':'Profit','label':'盈利','type':'line',},
                                                                              ],}, #'color':'#27B6AC'
          
              
            {'name':'bb','editor':'com-chart-plain','xdata':'Date','ydata':[{'name':'ProfitRate','label':'盈利率','type':'bar','color':'#27B6AC'}]},
            {'name':'bb','editor':'com-chart-plain','xdata':'Date','ydata':[{'name':'WinRate','label':'中注率','type':'bar','color':'#27B6AC'}]},
            {'name':'bb','editor':'com-chart-plain','xdata':'Date','ydata':[{'name':'RechargeAmount','label':'充值金额','type':'line'},
                                                                              {'name':'WithdrawAmount','label':'提现金额','type':'line'}]},
            
            {'name':'ss','editor':'com-chart-plain','source_rows':'rt=scope.ps.option.chart_data_sporttype_group',
             'xdata':'SportNameZH','ydata':[{'name':'SumBetAmount','label':'投注金额','type':'bar'},
                                            {'name':'SumBetOutcome','label':'派奖金额','type':'bar'},
                                            #{'name':'SumTurnOver','label':'','type':'bar'},
                                            #{'name':'SumBetBonus','label':'','type':'bar'},
                                            {'name':'SumProfit','label':'盈利','type':'bar'}
                                            ]},
              {'name':'bb','editor':'com-chart-plain','xdata_express':'rt=["串关","单注"]',
               'title':'注单统计',
              'source_rows':'rt=scope.ps.option.chart_data_ticket_amount',
              'ydata_express':'''(function(){
              if(scope.rows.length ==0){
                 return
              }
              var row=scope.rows[0];
            scope.ydata_list.splice(0,scope.ydata_list.length,...[
              {name:'投注金额',type:'bar',data:[row.SumParlayBetAmount,row.SumSingleBetAmount],barMaxWidth: 30,},
              {name:'派奖金额',type:'bar',data:[row.SumParlayBetOutcome,row.SumSingleBetOutcome],barMaxWidth: 30,},
              {name:'盈利',type:'bar',data:[row.SumParlayProfit,row.SumSingleProfit],barMaxWidth: 30,}
              ])
              scope.legend_list.splice(0, scope.legend_list.length,...['投注金额','派奖金额','盈利'])
              })()''',
           
              },
            {'name':'bb','title':'划单率','editor':'com-chart-plain',
             'source_rows':'rt=scope.ps.option.chart_data_void_rate',
               'xdata':'VoidReason','ydata':[{'name':'VoidRate','label':'划单率','type':'bar'},]},
             {'name':'ss','editor':'com-chart-plain','source_rows':'rt=scope.ps.option.chart_data_market_data',
              'title':'玩法',
              'style':{'heigth':'600px','width':'1000px'},
              'echarts_option':{
                  'xAxis':{
                        'axisLabel':{
                            'interval':0,
                            'fontSize':10,
                            'rotate':20,
                          },
                        'splitLine':{
                            'show':True
                        },
                  }
                
                  },
             'xdata':'MarketNameZH','ydata':[
                 {'name':'SumBetAmount','label':'投注金额','type':'bar'},
                 {'name':'SumBetOutcome','label':'派奖金额','type':'bar'}, 
                  {'name':'SumProfit','label':'盈利','type':'bar'}
                                           ]},
            #{'name':'ss','editor':'com-chart-radar',
             #'title':'基础图',
             #'source_rows':'rt=scope.ps.option.chart_data_market_data',
             #'xdata':'MarketNameZH','ydata':[
                 #{'name':'SumBetAmount','label':'投注金额','type':'radar'},
                 #{'name':'SumBetOutcome','label':'派奖金额','type':'radar'}, 
                  #{'name':'SumProfit','label':'盈利','type':'radar'}
                                           #]},
            {'name':'ss','editor':'com-chart-plain','source_rows':'rt=scope.ps.option.chart_data_league_group',
             'title':'联赛组',
              'style':{'heigth':'600px','width':'1000px'},
              'echarts_option':{
                  'xAxis':{
                        'axisLabel':{
                            'interval':0,
                            'fontSize':10,
                            'rotate':20,
                          },
                        'splitLine':{
                            'show':True
                        },
                  }
                
                  },
             'xdata':'GroupName','ydata':[
                 {'name':'SumBetAmount','label':'投注金额','type':'bar'},
                 {'name':'SumBetOutcome','label':'派奖金额','type':'bar'}, 
                  {'name':'SumProfit','label':'盈利','type':'bar'}
                                           ]},
            
         ]
        },
        {'name': 'baseinfo',
         'label': _('Basic Info'),
         'com': 'com-tab-fields',
         'get_data': {
             'fun': 'get_row',
             'kws': {
                 'director_name': AccoutBaseinfo.get_director_name(),
                 'relat_field': 'accountid',
             }
         },
         'after_save': {
             'fun': 'update_or_insert'
         },
         'heads': baseinfo.get_heads(),
         'ops': baseinfo.get_operations()
         },
        {'name': 'balance_log',
         'label': '账目记录',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': AccountBalanceTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbBalancelog, self.crt_user),
         },
        {'name': 'backcard',
         'label': '银行卡',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': UserBankCard(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbBankcard, self.crt_user),
         },
        {'name': 'UserRecharge',
         'label': '充值记录',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': UserRecharge(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbRecharge, self.crt_user),
         },
        {'name': 'UserWithdraw',
         'label': '提现记录',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': UserWithdraw(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbWithdraw, self.crt_user),
         },

        {'name': 'account_ticket',
         'label': _('Ticket'),
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': AccountTicketTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbTicketmaster, self.crt_user),
         },
        {'name': 'account_login',
         'label': _('Login Log'),
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': AccountLoginTable(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbLoginlog, self.crt_user), },
        {'name':'userlog',
         'label':'用户日志',
         'editor':'com-tab-table',
         'pre_set':'rt={accountid:scope.par_row.accountid}',
         'table_ctx':UserlogTab().get_head_context(),
         'visible':can_touch(TbUserLog,self.crt_user)},
        {'name': 'UserStatistics',
         'label': '会员统计',
         'com': 'com-tab-table',
         'par_field': 'accountid',
         'table_ctx': UserStatisticsTab(crt_user=self.crt_user).get_head_context(),
         'visible': True},
        {'name': 'MatchesStatistics',
         'label': '赛事统计',
         #'com': 'com-tab-table',
         'par_field': 'accountid',
         'editor':'com-tab-lazy-wrap',
         'lazy_init':'cfg.show_load();ex.director_call("d.get_head_context",{director_name:"account.matches_statistics"}).then(resp=>{cfg.hide_load();scope.head.editor="com-tab-table";scope.head.table_ctx=resp})',
         #'table_ctx': MatchesStatisticsTab(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbMatch, self.crt_user)},
        {'name':'BetFullRecordTab',
         'label':'限额记录',
         'com':'com-tab-table',
         'pre_set':'rt={accountid:scope.par_row.accountid}',
         'table_ctx': BetFullRecordTab(crt_user=self.crt_user).get_head_context(),
         'visible': can_touch(TbBetfullrecord, self.crt_user)
         },{
             'name':'related_user',
             'label':'关联用户',
             'editor':'com-tab-table',
             'pre_set':'rt={accountid:scope.par_row.accountid}',
             'table_ctx':RelatedUserTab().get_head_context(),
            'visible':has_permit(self.crt_user, 'member.relevent_user')
         },{
             'name':'agprofitloss',
             'label':'AG投注',
             'editor':'com-tab-table',
             'pre_set':'rt={accountid:scope.par_row.accountid}',
             'table_ctx':AgprofitLosTab().get_head_context(),
             'visible':getattr(settings,'OPEN_SECRET',False) and can_touch(TbAgprofitloss, self.crt_user)
         }
    ]
    dc = {
        'account_tabs':evalue_container(ls)
    }
    dc.update(MatchesStatisticsPage.get_tabs(self.crt_user))
    dc.update(WithdrawPage.get_tabs())
    return dc


class AccountPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '会员管理'

    def get_context(self):
        ctx = super().get_context()
        #ctx['tabs'] = account_tab(self)
        named_ctx =  account_tab(self)
        ctx['named_ctx'] = named_ctx
        
        return ctx

    class tableCls(ModelTable):
        model = TbAccount
        exclude=['password']
        #include = ['accountid', 'account', 'nickname', 'viplv', 'status', 'amount', 'bonusrate', 'agentamount',
                   #'isenablewithdraw', 'sumrechargecount', 'sumwithdrawcount', 'rechargeamount', 'withdrawamount',
                   #'createtime', 'source','accounttype','weight','groupid']
        fields_sort = ['accountid', 'account', 'nickname', 'createtime','weight','ticketdelay','groupid', 'bonusrate', 'viplv','source', 'status',
                       'isenablewithdraw', 'amount', 'agentamount','betfullrecord',
                       'sumrechargecount', 'sumwithdrawcount', 'rechargeamount', 'withdrawamount','accounttype','anomalyticketnum','csuserid','memo']

        class filters(RowFilter):
            names=['accounttype','groupid','csuserid__name']
            icontains=['csuserid__name']
            range_fields = ['createtime']
            
            def getExtraHead(self):
                return [
                    {'name':"csuserid__name",'placeholder':'所属客服',}
                ]
            
            def clean_search_args(self, search_args):
                cs_user_name = search_args.pop('csuserid__name',None)
                out = super().clean_search_args(search_args)
                if cs_user_name:
                    ls=[x.pk for x in User.objects.filter(Q(first_name__icontains=cs_user_name) | Q(username__icontains=cs_user_name))]
                    out['csuserid__in'] = ls
                return out
            
        def inn_filter(self, query):
            """
            """
            #withdraw_query = TbWithdraw.objects.filter(accountid=OuterRef('pk')).values('accountid')
            #withdraw_query=withdraw_query.annotate(amount_sum=Sum('amount')).values('amount_sum')
            #query= query.annotate(
                #bbb=Count('tbrecharge__confirmamount'),
                #rechargeamount=Sum(Case(When(tbrecharge__status=2, then=F('tbrecharge__confirmamount') ),output_field=DecimalField(decimal_places=2, max_digits=8),  default=0)))
            #query=query.annotate(
                #withdrawamount= Subquery(
                    #withdraw_query
                                         #)
                       #)
                ##withdrawamount=Sum(Case(When(tbwithdraw__status=2, then=F('tbwithdraw__amount')), default=0)))
            #return query
            return query.extra(select={'betfullrecord':'SELECT SUM(TB_Betfullrecord.consumeamount) FROM TB_Betfullrecord WHERE TB_Betfullrecord.ConsumeStatus=1 AND TB_Betfullrecord.AccountID=TB_Account.AccountID',
                                       'rechargeamount':'SELECT SUM(TB_Recharge.ConfirmAmount) FROM TB_Recharge WHERE TB_Recharge.status=2 AND TB_Recharge.AccountID=TB_Account.AccountID',
                                       'withdrawamount':'SELECT SUM(TB_Withdraw.Amount) FROM TB_Withdraw WHERE TB_Withdraw.Status=2 AND TB_Withdraw.AccountID =TB_Account.AccountID'})
        #.annotate(rechargeamount_count=Count('tbrecharge__rechargeid',distinct=True),
                                  #withdrawamount_count=Count('tbwithdraw__withdrawid',distinct=True))\
                   #.annotate( rechargeamount_total= Sum(Case(When(tbrecharge__status=2, then=F('tbrecharge__confirmamount')), default=0)),
                              #withdrawamount_total=Sum(Case(When(tbwithdraw__status=2, then=F('tbwithdraw__amount')), default=0)) )\
                   #.annotate( rechargeamount= Case(When(withdrawamount_count=0,then= F('rechargeamount_total') ),output_field=DecimalField(decimal_places=2, max_digits=8) ,default =  F('rechargeamount_total') / F('withdrawamount_count') ),
                              #withdrawamount= Case(When(rechargeamount_count=0,then= F('withdrawamount_total') ),output_field=DecimalField(decimal_places=2, max_digits=8) ,default= F('withdrawamount_total')/ F('rechargeamount_count') ) 
                              #)
        
                   #.annotate(betfullrecord=Sum('tbbetfullrecord__consumeamount'))
        
                #rechargeamount=Sum(Case(When(tbrecharge__status=2, then=F('tbrecharge__confirmamount')), default=0))) \
                #.annotate(withdrawamount=Sum(Case(When(tbwithdraw__status=2, then=F('tbwithdraw__amount')), default=0)))

        def dict_row(self, inst):
            tmp = list(inst.account)
            tmp[0:-4] = '*' * (len(tmp) - 4)
            out_str = ''.join(tmp)
            
            return {
                'amount': str(inst.amount),
                'account': out_str,
                'group_color':inst.groupid.extension,
                'rechargeamount': round( inst.rechargeamount or 0 ,2),
                'withdrawamount': round( inst.withdrawamount or 0,2),
                'betfullrecord':round( inst.betfullrecord or 0,2) # round( sum( [x.consumeamount for x in  inst.tbbetfullrecord_set.all()] ),2),
            }
        
        def get_rows(self):
            rows = super().get_rows()
            csuserlist = [dc.get('csuserid') for dc in rows if dc.get('csuserid') !=None]
            usermap ={}
            for user in User.objects.filter(pk__in=csuserlist):
                usermap[user.pk] = str(user)
            for row in rows:
                row['_csuserid_label'] = usermap.get(row.get('csuserid'),row.get('csuserid'))
            return rows
        
        def get_head_context(self):
            named_ctx = get_request_cache()['named_ctx']
            named_ctx.update({
                'account.memo.form':MemoForm().get_head_context()
            })
            return super().get_head_context()
        
        def dict_head(self, head):
            dc = {
                'accountid': 80,
                'account': 100,
                'nickname': 100,
                'viplv': 80,
                'amount': 100,
                'rechargeamount': 100,
                'withdrawamount': 100,
                'agentamount': 100,
                'status': 60,
                'createtime': 150,
                'anomalyticketnum':120,
                'csuserid':140,
                'groupid':120,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-switch-to-tab'
                head['ctx_name'] = 'account_tabs'
                head['tab_name'] = 'dashborad'
            if head['name'] == 'status':
                head['editor'] = 'com-table-bool-shower'
            if head['name'] in ['agentamount', 'amount']:
                head['editor'] = 'com-table-digit-shower'
                head['digit'] = 2
            if head['name'] in ['bonusrate']:
                head['editor'] = 'com-table-digit-shower'
                head['digit'] = 3
            if head['name'] =='csuserid':
                head['editor'] = 'com-table-label-shower'
            if head['name'] == 'groupid':
                head['inn_editor'] = head['editor']
                head['editor'] = 'com-table-rich-span'
                head['style'] = 'if(scope.vc.light_level(scope.row.group_color) > 192){var mycolor="black"}else{var mycolor="white"};rt={background:scope.row.group_color,color:mycolor}'
            return head

        #def statistics(self, query):
            #dc = query.aggregate(total_amount=Sum('amount'), total_agentamount=Sum('agentamount'))
            #mapper = {
                #'amount': 'total_amount',
                #'agentamount': 'total_agentamount'
            #}
            #for k in dc:
                #dc[k] = str(round(dc.get(k) or 0, 2))
            #footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            #self.footer = footer
            #self.footer = ['合计'] + self.footer
            #return query.order_by('-pk')

        #def get_context(self):
            #ctx = ModelTable.get_context(self)
            #ctx['footer'] = self.footer
            #return ctx

        def getExtraHead(self):
            return [{'name': 'rechargeamount', 'label': '充值金额'}, 
                    {'name': 'withdrawamount', 'label': '提现金额'},
                    {'name': 'betfullrecord', 'label': '提现限额'}]

        class search(SelectSearch):
            names = ['nickname',]
            exact_names = ['accountid']

            def get_option(self, name):
                if name == 'accountid':
                    return {'value': name,
                            'label': '账户ID', }
                elif name == 'nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }
                

            #def clean_search(self):
                #if self.qf in ['accountid']:
                    #if not re.search('^\d*$', self.q):
                        #return None
                    #else:
                        #return self.q
                #else:
                    #return super().clean_search()

        class sort(RowSort):
            names = ['nickname', 'account', 'amount','ticketdelay', 'bonusrate', 'agentamount', 'createtime', 'sumrechargecount',
                     'rechargeamount', 'withdrawamount','anomalyticketnum']

        def get_operation(self):
            betfullmodify = ModifyBetFullRecord(crt_user=self.crt_user)
            changeable_fields = self.permit.changeable_fields()
            return [
                #'fun': 'selected_set_and_save', 
                {
                 'editor': 'com-op-btn', 
                 'action':'var ctx=named_ctx["account.memo.form"];ctx.title="解冻账号";ctx.row=scope.ps.selected[0];ctx.row.status=1;cfg.pop_vue_com("com-form-one",ctx).then(row=>{ex.vueAssign(ctx.row,row)})',
                 'label': '解冻', 
                 #'field': 'status',
                 #'value': 1,
                 #'confirm_msg': '确认解冻？',
                 'visible': 'status' in changeable_fields, },
                { 'editor': 'com-op-btn',
                  'label': '冻结', 
                  #'field': 'status', 'value': 0, 'confirm_msg': '确认冻结？', 
                'action':'var ctx=named_ctx["account.memo.form"];ctx.title="冻结账号";ctx.row=scope.ps.selected[0];ctx.row.status=0;cfg.pop_vue_com("com-form-one",ctx).then(row=>{ex.vueAssign(ctx.row,row)})',
                 'visible': 'status' in changeable_fields},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '重置登录密码', 'field': 'password',
                 'value': 1, 'row_match': 'one_row', 'confirm_msg': '确认重置登录密码？',
                 'visible': 'password' in changeable_fields},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '重置资金密码', 'field': 'fundspassword',
                 'value': 1, 'row_match': 'one_row', 'confirm_msg': '确认重置资金密码？',
                 'visible': 'fundspassword' in changeable_fields},
                # selected_pop_set_and_save
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '调账',
                 'after_error':'scope.fs.showErrors(scope.errors)',
                 'fields_ctx': AccoutModifyAmount().get_head_context(), 
                 'visible': 'amount' in changeable_fields},
                
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '调整限额',
                 'after_error':'scope.fs.showErrors(scope.errors)',
                 'fields_ctx': betfullmodify.get_head_context(), 'visible': 'amount' in changeable_fields},
                
                { 'editor': 'com-op-btn', 'label': '允许提现',
                  #'field': 'isenablewithdraw','value': 1, 'confirm_msg': '确认允许这些用户提现？', 
                'action':'var ctx=named_ctx["account.memo.form"];ctx.title="允许提现";ctx.row=scope.ps.selected[0];ctx.row.isenablewithdraw=1;cfg.pop_vue_com("com-form-one",ctx).then(row=>{ex.vueAssign(ctx.row,row)})',
                 'visible': 'isenablewithdraw' in changeable_fields},
                { 'editor': 'com-op-btn', 'label': '禁止提现', 
                  #'field': 'isenablewithdraw','value': 0, 
                  'confirm_msg': '确认禁止这些用户提现？', 
                  'row_match':'one_row',
                'action':'var ctx=named_ctx["account.memo.form"];ctx.title="禁止提现";ctx.row=scope.ps.selected[0];ctx.row.isenablewithdraw=0;cfg.pop_vue_com("com-form-one",ctx).then(row=>{ex.vueAssign(ctx.row,row)})',
                 'visible': 'isenablewithdraw' in changeable_fields},
                {'editor':'com-op-btn','label':'选择客服','visible': 'csuserid' in changeable_fields,
                 'table_ctx':UserPicker().get_head_context(),
                 'action':''' cfg.pop_vue_com("com-table-panel",scope.head.table_ctx).
                 then((row)=>{
                 ex.each(scope.ps.selected,account=>{
                     account.csuserid = row.pk
                     account._csuserid_label = row.first_name+'('+ row.username +')'
                     account.meta_change_fields='csuserid'
                 })
                 cfg.show_load()

                 scope.ps.save_rows(scope.ps.selected,option).then((resp)=>{
                     scope.ps.update_rows(resp)
                     cfg.hide_load()
                     cfg.toast("操作完成")
                     scope.ps.selected = []
                 })  
                 })'''}
            ]
          #var option={
                     #after_save:"scope.ps.update_rows(resp);"
                 #}
        
               #ex.director_call('d.save_rows',{rows:scope.ps.selected}).then(resp=>{
                 #if(scope.ps.check_outdate(resp) ){
                     #scope.ps.update_rows(resp)
                     #cfg.hide_load()
                     #cfg.toast("操作完成")
                     #scope.ps.selected = []
                 #}


class MemoForm(Fields):
    def get_heads(self):
        return [
            {'name':'new_memo','label':'备注','editor':'com-field-linetext','required':True,'fv_rule':'length(5~)'}
        ]
    
    #def clean(self):
        #try:
            #self.instance = TbAccount.objects.get(pk = self.kw.get('pk'))
        #except TbAccount.DoesNotExist:
            #raise UserWarning('账号不存在')
    
    #def get_row(self):
        #return {
            #'memo':self.instance.memo
        #}
    
    #def save_form(self):
        #if self.instance.memo:
            #self.instance.memo += ';'+self.kw.get('memo')
        #else:
            #self.instance.memo = self.kw.get('memo')
        #self.instance.save()
 

class AccoutBaseinfo(ModelFields):
    #'agentamount', 
    field_sort = ['account', 'nickname', 'amount', 'status', 'agent', 'verify', 'viplv', 'bonusrate',
                  'isenablewithdraw','accounttype', 'groupid','weight','ticketdelay','risklevel','cashchannel','createtime','anomalyticketnum','powertype']
    readonly = ['createtime', 'account', 'nickname', 'amount', 'agentamount']
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw):
        if kw.get('accountid'):
            pk = kw.get('accountid')
        super().__init__(dc, pk, crt_user, nolimit, *args, **kw)
        self.orgin_risklevel= self.instance.risklevel

    def dict_head(self, head):
        if head['name'] == 'bonusrate':
            head['step'] = 0.001
        if head['name']=='weight':
            head['fv_rule']='range(0.001~500);'+ head.get('fv_rule','')
        if head['name']=='risklevel':
            head['editor']='com-field-select'
            inst = TbSetting.objects.get(settingname='RiskControlLevel')
            head['options']=[{'value':x['Level'],'label':x['Memo']} for x in json.loads(inst.settingvalue)]
        if head['name']=='cashchannel':
            head['editor']='com-field-select'
            inst = TbSetting.objects.get(settingname='CashChannel')
            head['options']=[{'value':x['Channel'],'label':x['Memo']} for x in json.loads(inst.settingvalue)]  
        if head['name'] == 'anomalyticketnum':
            head['fv_rule']='integer(+0);range(0~10)'
        return head

    def dict_row(self, inst):
        tmp = list(inst.account)
        tmp[0:-4] = '*' * (len(tmp) - 4)
        out_str = ''.join(tmp)
        return {
            'account': out_str,
        }

    def clean_save(self):
        if self.kw.get('password') == 1:
            text_pswd, self.instance.password = gen_pwsd()
            send_message_password(self.instance.phone, text_pswd)
            return {'memo': '重置密码', }
        elif self.kw.get('fundspassword') == 1:
            text_pswd, self.instance.fundspassword = gen_money_pswd()
            send_message_fundspassword(self.instance.phone, text_pswd)
            return {'memo': '重置资金密码', }
        if 'risklevel' in self.changed_data:
            # 用户风险控制。
            risklevel = self.cleaned_data.get('risklevel')
            if risklevel > self.orgin_risklevel:
                # 升
                self.instance.isriskleveldown = 0
                TbRisklevellog.objects.create(upordown=1,createuser=self.crt_user.username,accountid=self.instance.accountid,oldrisklevel=self.orgin_risklevel,newrisklevel=risklevel,)
            else:
                # 降
                self.instance.isriskleveldown = 1
                TbRisklevellog.objects.create(upordown=2,createuser=self.crt_user.username,accountid=self.instance.accountid,oldrisklevel=self.orgin_risklevel,newrisklevel=risklevel,)
        if 'status' in self.changed_data:
            dc = {'AccountID':self.instance.accountid}
            msg = json.dumps(dc)
            notifyAccountFrozen(msg)
        if self.kw.get('new_memo'):
            if self.instance.memo:
                self.instance.memo += ';'+self.kw.get('new_memo')
            else:
                self.instance.memo = self.kw.get('new_memo')

    class Meta:
        model = TbAccount
        exclude = ['actimestamp', 'agent', 'phone', 'gender', 'points', 'codeid', 'parentid',
                   'sumrechargecount', 'password']


class AccoutModifyAmount(ModelFields):
    field_sort = ['accountid', 'nickname', 'amount', 'add_amount','moenycategory',] #'fundtype']
    readonly = ['accountid', 'nickname','amount']
    
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.before_amount = self.instance.amount

    class Meta:
        model = TbAccount
        fields = ['amount', 'nickname', 'accountid', 'amount', 'agentamount']
    
    def dict_head(self, head):
        if head['name'] =='amount':
            head['readonly']=True
        return head
    
    def getExtraHeads(self):
        desp_options = [{'value':x.pk,'label':x.categoryname} for x in  TbMoneyCategories.objects.all()]
        return [
            {'name': 'add_amount', 'label': '调整金额', 'editor': 'number', 'required': True,'fv_rule': 'range(-50000~50000)', },
            {'name':'moenycategory','label':'类型','editor':'com-field-select','required':True,'options':desp_options},
            #{'name':'fundtype','label':'定向体育','editor':"com-field-bool",'help_text':'勾选后只能用于体育类型消费'},
        ]

    def extra_valid(self):
        dc = {}
        if self.cleaned_data.get('amount') + Decimal( self.kw.get('add_amount',0) )< 0:
            dc['add_amount'] = '叠加值使得余额小于0'
        return dc

    def clean_save(self):
        if 'add_amount' in self.kw:
            add_amount = Decimal(self.kw.get('add_amount', 0))
            self.changed_amount = add_amount
            moenycategory_pk = self.kw.get('moenycategory')
            moenycategory_inst = TbMoneyCategories.objects.get(categoryid =moenycategory_pk)
            cashflow, moenycategory =moenycategory_inst.cashflow,moenycategory_pk
            #before_amount = self.instance.amount
            self.instance.amount = self.before_amount + add_amount
            TbBalancelog.objects.create(account=self.instance.account, beforeamount=self.before_amount,
                                        amount=abs( self.changed_amount), afteramount=self.instance.amount, creater='Backend',
                                        memo='调账', accountid=self.instance, categoryid_id=moenycategory,
                                        cashflow=cashflow)
            if add_amount > 0:
                TbBetfullrecord.objects.create(accountid_id=self.kw.get('accountid') ,amount = add_amount,
                                               consumeamount = add_amount,
                                               #fundtype = 1 if self.kw.get('fundtype')  else 0,
                                               consumestatus=1,rftype=3,rfid=0,content='后台管理员调账')
            return {'memo': '调账', 'ex_before': {'amount': self.before_amount},
                    'ex_after': {'amount': self.instance.amount, }}


class ModifyBetFullRecord(ModelFields):
    field_sort = ['accountid', 'nickname', 'betfullrecord', 'add_amount']
    readonly = ['accountid', 'nickname',]
    
    class Meta:
        model = TbAccount
        fields = ['nickname', 'accountid']
    
    def clean_dict(self, dc):
        return dc
        #if dc.get('add_amount'):
            #self.add_amount = Decimal(dc.get('add_amount', 0))
            #dc.pop('betfullrecord',None)
           
            #self.changed_amount = add_amount
            #dc['amount'] = Decimal(dc['amount']) + add_amount
        #return dc    
    
    def dict_row(self, inst):
        return {
            'betfullrecord':round( sum( [x.consumeamount for x in  inst.tbbetfullrecord_set.all()] ),2),
        }
    
    def getExtraHeads(self):
        return [
            {'name': 'betfullrecord', 'label': '当前限额', 'editor': 'number', 'readonly':True },
            {'name': 'add_amount', 'label': '调整金额', 'editor': 'number', 'required': True,'fv_rule': 'range(-50000~50000)', }
        ]    
    
    def clean(self):
        super().clean()
        add_amount = self.kw.get('add_amount')
        if not add_amount :
            self._errors['add_amount']= '调整值不能为0或者空'
        else:
            self. betfullrecord_list = TbBetfullrecord.objects.filter(accountid_id=self.kw.get('accountid'),consumestatus=1).order_by('tid')
            total =sum([x.consumeamount for x in  self. betfullrecord_list ] )
            if Decimal( add_amount ) + total < 0 :
                self._errors['add_amount']= '不能使限额小于0'
    
    def clean_save(self):
        if 'add_amount' in self.kw:
            add_amount = Decimal( self.kw.get('add_amount') )
            if add_amount < 0:
                for item in self.betfullrecord_list:
                    if item.consumeamount + add_amount <=0:
                        
                        item.content = item.content or '' + ';调整数-%s'%  item.consumeamount 
                        item.consumeamount = 0
                        item.consumestatus = 2
                        
                        item.save()
                        add_amount += item.consumeamount
                    else:
                        item.content =  item.content or '' + ';调整数%s'%  add_amount 
                        item.consumeamount += add_amount
                        item.save()
                        break
            else:
                TbBetfullrecord.objects.create(accountid_id=self.kw.get('accountid') ,amount = add_amount,consumeamount = add_amount,consumestatus=1,rftype=3,rfid=0,content='后台管理员限额调整')
                
            after_amount = Decimal(self.kw.get('betfullrecord')) + add_amount
            return {'memo': '提现限额调整', 'ex_before': {'betfullrecord': self.kw.get('betfullrecord')},
                    'ex_after': {'betfullrecord': str(after_amount) , }}

class AccountTabBase(ModelTable):
    def __init__(self, *args, **kws):
        ModelTable.__init__(self, *args, **kws)
        accountid = self.kw.get('accountid')
        self.accountid = accountid

    def inn_filter(self, query):
        return query.filter(accountid=self.accountid)


class WithAccoutInnFilter(ModelTable):
    def inn_filter(self, query):
        query = super().inn_filter(query)
        if self.kw.get('accountid'):
            return query.filter(accountid=self.kw.get('accountid'))
        else:
            return query


class AccountBalanceTable(WithAccoutInnFilter, BalancelogPage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return BalancelogPage.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []


class UserBankCard(WithAccoutInnFilter, BankCard.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return BankCard.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []


class UserRecharge(WithAccoutInnFilter, RechargePage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return RechargePage.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []


class UserWithdraw(WithAccoutInnFilter, WithdrawPage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return WithdrawPage.tableCls.get_edit_director_name()
    

    class search(RowSearch):
        names = []


class AccountTicketTable(WithAccoutInnFilter, TicketMasterPage.tableCls):

    @classmethod
    def get_edit_director_name(cls):
        return TicketMasterPage.tableCls.get_edit_director_name()

    #def dict_head(self, head):
        #head = super().dict_head(head)

        #if head['name'] == 'ticketid':
            #head['editor'] = ''
        #return head
    
    class search(SelectSearch):
            #names = ['accountid__nickname']
            exact_names = ['orderid', 'tbticketstake__matchid']

            def get_option(self, name):

                if name == 'orderid':
                    return {'value': name,
                            'label': '订单编号', }
                #elif name == 'accountid__nickname':
                    #return {
                        #'value': name,
                        #'label': '昵称',
                    #}
                elif name == 'tbticketstake__matchid':
                    return {
                        'value': name,
                        'label': '比赛ID',
                    }

            def clean_search(self):
                if self.qf in ['ticketid', 'tbticketstake__matchid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()


class AccountLoginTable(WithAccoutInnFilter, LoginLogPage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return LoginLogPage.tableCls.get_edit_director_name()

    class search(RowSearch):
        names = []

@director_element('account.userlogtab')
class UserlogTab(UserlogPage.tableCls):
    def inn_filter(self, query):
        return query.filter(account_id = self.kw.get('accountid'))
    

class UserStatisticsTab(UserStatisticsPage.tableCls):
    class search(RowSearch):
        names = []
        
    class filters(RowFilter):
        range_fields = ['date']

        def getExtraHead(self):
            return [
                {'name':'date','editor':'com-filter-datetime-range','label':'时间'}
            ]


class MatchesStatisticsTab(MatchesStatisticsPage.tableCls):
    class search(RowSearch):
        names = []


class BetFullRecordTab(WithAccoutInnFilter):
    model = TbBetfullrecord
    exclude = []
    fields_sort=['consumeamount','amount','rftype','consumestatus','content','createtime',]
    
    class filters(RowFilter):
        range_fields=['createtime']
    
    def dict_head(self, head):
        width_dc = {
            'createtime':150,
            'content':200,
        }
        if width_dc.get(head['name']):
            head['width'] = width_dc.get(head['name'])
        return head

class SingleUserStatistic(PlainTable):
    
    def getRowFilters(self):
        return [
            {'name':'StartTime','label':'开始时间','editor':'com-filter-datetime'},
            {'name':'EndTime','label':'结束时间','editor':'com-filter-datetime'},
        ]
    
    def get_heads(self):
        return []
    
    @classmethod
    def clean_search_args(cls, search_args):
        ago_30= timezone.now()-timezone.timedelta(days=30)
        search_args['StartTime'] = search_args.get('StartTime',ago_30.strftime('%Y-%m-%d 00:00:00'))
        search_args['EndTime'] = search_args.get('EndTime',timezone.now().strftime('%Y-%m-%d 23:59:59'))
        
        start =  timezone.datetime.strptime(search_args['StartTime'],'%Y-%m-%d %H:%M:%S')
        end = timezone.datetime.strptime(search_args['EndTime'],'%Y-%m-%d %H:%M:%S')
        if end < start:
            raise UserWarning('结束时间必须大于开始时间')
        if (end -start ).days > 31:
            raise UserWarning('最多只能查询31天的数据')
        
        return search_args
    
    def get_head_context(self):
        ctx = super().get_head_context()
        ctx.update({
            'option':{
                'chart_data_sporttype_group':[],
                'chart_data_market_data':[],
                'chart_data_league_group':[],
                'chart_data_ticket_amount':[],
                'chart_data_void_rate':[],
            },

            'after_get_rows':'''scope.ps.option.chart_data_sporttype_group = scope.resp.sporttype_group;
            scope.ps.option.chart_data_market_data = scope.resp.chart_data_market_data;
            scope.ps.option.chart_data_league_group = scope.resp.chart_data_league_group;
            scope.ps.option.chart_data_ticket_amount = scope.resp.chart_data_ticket_amount;
            scope.ps.option.chart_data_void_rate = scope.resp.chart_data_void_rate;
             '''
        })
        return ctx
    
    def get_data_context(self):
        ctx = super().get_data_context()
        ctx.update({
            'sporttype_group':self.sporttype_group,
            'chart_data_market_data':self.chart_data_market_data,
            'chart_data_league_group':self.chart_data_league_group,
            'chart_data_ticket_amount':self.chart_data_ticket_amount,
            'chart_data_void_rate':self.chart_data_void_rate,
        })
        return ctx
    
    def get_rows(self):
        sql_args ={
            'AccountID':self.kw.get('accountid'),
            'StartTime':self.search_args.get('StartTime'),
            'EndTime':self.search_args.get('EndTime'),
        }
        sql = r"exec dbo.SP_UserStatisticsTrend %(AccountID)s,'%(StartTime)s','%(EndTime)s'" \
                  % sql_args
        with connections['Sports'].cursor() as cursor:
            cursor.execute(sql)
            set0 = cursor.fetchall()
            #self.total = set0[0][0]
            footer = {}
            for col_data, col in zip(set0[0], cursor.description):
                head_name = col[0]
                if head_name.startswith('Sum'):
                    head_name = head_name[3:]
                footer[head_name] = col_data
            footer.update({
                '_label':'合计'
            })
            self.footer =  footer 
            
            cursor.nextset()
            rows =[]
            for row in cursor:
                row_dc = {}
                for index, head in enumerate(cursor.description):
                    row_dc[head[0]] = row[index]
                rows.append(row_dc)
                
            cursor.nextset()
            self.sporttype_group =[]
            for row in cursor:
                row_dc = {}
                for index, head in enumerate(cursor.description):
                    row_dc[head[0]] = row[index]
                self.sporttype_group.append(row_dc)
                
            cursor.nextset()
            self.chart_data_market_data = []
            count = 0
            other_dc={}
            for row in cursor:
                count += 1
                if count > 14:
                    for index, head in enumerate(cursor.description):
                        if head[0]=='MarketNameZH':
                            other_dc['MarketNameZH'] ='其他'
                        else:
                            other_dc[head[0]] = other_dc.get(head[0],0) + row[index]
                else:
                    row_dc = {}
                    for index, head in enumerate(cursor.description):
                        row_dc[head[0]] = row[index]
                    self.chart_data_market_data.append(row_dc)
                    
            if other_dc:
                self.chart_data_market_data.append(other_dc)
            
            # 处理联赛组
            cursor.nextset()
            count = 0
            other_dc={}
            self.chart_data_league_group =[]
            for row in cursor:
                count += 1
                if count >14:
                    for index, head in enumerate(cursor.description):
                        if head[0]=='GroupName':
                            other_dc['GroupName'] ='其他'
                        else:
                            other_dc[head[0]] = other_dc.get(head[0],0) + row[index]    
                else:
                    row_dc = {}
                    for index, head in enumerate(cursor.description):
                        row_dc[head[0]] = row[index]
                    self.chart_data_league_group.append(row_dc)
            if other_dc:
                self.chart_data_league_group.append(other_dc)
                
            cursor.nextset()
            self.chart_data_ticket_amount=[]
            for row in cursor:
                row_dc = {}
                for index, head in enumerate(cursor.description):
                    row_dc[head[0]] = row[index]
                self.chart_data_ticket_amount.append(row_dc)
                
            cursor.nextset()
            self.chart_data_void_rate=[]
            for row in cursor:
                row_dc = {}
                for index, head in enumerate(cursor.description):
                    row_dc[head[0]] = row[index]
                self.chart_data_void_rate.append(row_dc)
        return rows
            
class RelatedUserTab(ReleventUserPage.tableCls):
    def get_rows(self):
        self.search_args['accountid'] = self.kw.get('accountid')
        rows = self.get_data_from_db()
        return rows
    def getRowFilters(self):
        return [
            {'name':'StartTime','label':'开始时间','editor':'com-filter-datetime','width':'200px'},
            {'name':'EndTime','label':'结束时间','editor':'com-filter-datetime'},
        ]

class AgprofitLosTab(AgprofitlossPage.tableCls):
    
    def inn_filter(self, query):
        return query.filter(account_id=self.kw.get('accountid'))
    
    class search(RowSearch):
        pass

director.update({
    'account': AccountPage.tableCls,
    'account.edit': AccoutBaseinfo,
    'account.base.edit': AccoutBaseinfo,
    'account.amount.edit': AccoutModifyAmount,
    'account.betfullmodify':ModifyBetFullRecord,
    
    'account.bankcard': UserBankCard,
    'account.bankcard.edit': BankCardForm,
    'account.UserRecharge': UserRecharge,
    'account.UserWithdraw': UserWithdraw,
    'account.log': AccountLoginTable,
    'account.ticketmaster': AccountTicketTable,
    'account.balancelog': AccountBalanceTable,
    'account.statistc': UserStatisticsTab,
    'account.matches_statistics': MatchesStatisticsTab,
    'account.betfullrecordtab':BetFullRecordTab,
    
    'account.memo.form':MemoForm,
    'account.single_user_statistic':SingleUserStatistic,
    'account.related_user':RelatedUserTab,
    'account.agprofitloss':AgprofitLosTab,
})

# permits = [('TbAccount', model_full_permit(TbAccount), model_to_name(TbAccount), 'model'),
# ('TbLoginlog', model_full_permit(TbLoginlog), model_to_name(TbLoginlog), 'model'),
# ('TbBalancelog', model_full_permit(TbBalancelog), model_to_name(TbBalancelog), 'model'),
# ('TbAccount.all', 'TbAccount;TbLoginlog;TbBalancelog;TbTicketmaster', '', 'set'),
# ]

# add_permits(permits)

page_dc.update({
    'account': AccountPage
})


def gen_pwsd():
    while True:
        pswd = get_str(length=6)
        # 不能全是字母，或者全是数字
        if not (re.search('^\d+$', pswd) or re.search('^\[a-zA-Z]+$', pswd)):
            break
    text_pswd = pswd
    m1 = hashlib.md5()
    m1.update(pswd.encode("utf-8"))
    pswd = m1.hexdigest()
    salt = ':69257765ACB34A08A6D0D978E9CF39ED'
    pswd_str = pswd + salt
    m2 = hashlib.md5()
    m2.update(pswd_str.encode("utf-8"))  # 参数必须是byte类型，否则报Unicode-objects must be encoded before
    pswd_db_str = m2.hexdigest().upper()
    return text_pswd, pswd_db_str

def gen_money_pswd(): 
    pswd = get_random_number(6)
    text_pswd = pswd
    m1 = hashlib.md5()
    m1.update(pswd.encode("utf-8"))
    pswd = m1.hexdigest()
    salt = ':69257765ACB34A08A6D0D978E9CF39ED'
    pswd_str = pswd + salt
    m2 = hashlib.md5()
    m2.update(pswd_str.encode("utf-8"))  # 参数必须是byte类型，否则报Unicode-objects must be encoded before
    pswd_db_str = m2.hexdigest().upper()
    return text_pswd, pswd_db_str

class Digit3(DecimalProc):
    digit=3

field_map.update({
    model_to_name(TbAccount)+'.weight':Digit3
})