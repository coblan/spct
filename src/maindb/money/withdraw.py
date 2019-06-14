# encoding:utf-8
import re
from django.db import transaction
from django.utils.timezone import datetime
from django.db.models import Sum
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter, ModelFields,director_view
from helpers.director.table.row_search import SelectSearch
from helpers.director.table.table import RowSort
from ..models import TbWithdraw, TbBalancelog, TbMessageUnsend,TbTicketmaster
from maindb.rabbitmq_instance import notifyWithdraw
from maindb.matches.ticket_master import TicketMasterPage

class WithdrawPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '提现管理'

    class tableCls(ModelTable):
        model = TbWithdraw
        exclude = []
        fields_sort = ['accountid', 'orderid', 'amount', 'status', 'createtime', 'confirmtime',
                       'amounttype', 'apollocode', 'apollomsg', 'memo']

        def dict_head(self, head):
            dc = {
                'accountid': 120,
                'createtime': 150,
                'confirmtime': 150,
                'apollomsg': 200,
                'memo': 120,
                'apollocode': 150
            }
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-switch-to-tab'
                head['inn_editor'] = 'com-table-label-shower'
                head['tab_name'] = 'baseinfo'
                head['ctx_name'] = 'account_tabs'
                
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def statistics(self, query):
            dc = query.aggregate(total_amount=Sum('amount'))
            mapper = {
                'amount': 'total_amount'
            }
            for k in dc:
                dc[k] = str(round(dc.get(k) or 0, 2))
            footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            self.footer = footer
            self.footer = ['合计'] + self.footer
            return query

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            
            # 交叉引用问题
            from maindb.member.account import account_tab
            ctx['named_ctx'] = account_tab(self)
            ctx['named_ctx'].update({
                'withdraw_tab':[
                     {'name': 'ticketmaster',
                      'label': '注单列表',
                      'com': 'com-tab-table',
                      'pre_set': '{accountid:scope.par_row.accountid}',
                      'table_ctx': TicketmasterTab(crt_user=self.crt_user).get_head_context(),
                      'visible': True,
                      },
                ]
            })
            return ctx

        def get_operation(self):
            return [
                {
                    'fun': 'selected_set_and_save',
                    'action':'''(function(){
                    if( !scope.ps.check_selected(scope.head) ){return};
                    ex.director_call("has_audit_ticketmaster",{accountid:scope.ps.selected[0].accountid})
                    .then((res)=>{
                        if(!res){
                            scope.self.$emit('operation',scope.self.head.name || scope.self.head.fun)
                        }else{
                            cfg.confirm("该用户有未处理的异常注单").then(()=>{
                                scope.ps.switch_to_tab({ctx_name:"withdraw_tab",tab_name:"ticketmaster",par_row:scope.ps.selected[0]})
                            })
                           
                        }
                    })
                    })()''',
                    'editor': 'com-op-btn',
                    'label': '审核异常单/重发',
                    'field': 'status',
                    'value': 1,
                    'row_match': 'one_row_match',
                    'match_field': 'status',
                    'match_values': [3,4],
                    'match_msg': '只能选择状态为异常/失败的订单！',
                    'fields_ctx': WithDrawForm(crt_user=self.crt_user).get_head_context(),
                    'visible': 'status' in self.permit.changeable_fields(), },
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '确认成功',
                    'field': 'status',
                    'value': 2,
                    'row_match': 'one_row_match',
                    'match_field': 'status',
                    'match_values': [1],
                    'match_msg': '只能选择状态为处理中的订单！',
                    'confirm_msg': '确认修改订单状态为成功吗？',
                    'fields_ctx': WithDrawForm(crt_user=self.crt_user).get_head_context(),
                    'visible': 'status' in self.permit.changeable_fields(), },
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '退款',
                    'field': 'status',
                    'value': 5,
                    'row_match': 'one_row_match',
                    'match_field': 'status',
                    'match_values': [1, 3, 4],
                    'confirm_msg': '确认退款到用户余额吗？',
                    'visible': 'status' in self.permit.changeable_fields(),
                    'match_msg': '只能选择状态为处理中，失败或异常的订单',
                    'fields_ctx': WithDrawForm(crt_user=self.crt_user).get_head_context()},
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o'}
            ]

        def inn_filter(self, query):
            return query.order_by('-createtime')

        class sort(RowSort):
            names = ['amount', 'createtime', 'confirmtime']

        class search(SelectSearch):
            names = ['accountid__nickname']
            exact_names = ['orderid']

            def get_option(self, name):
                if name == 'orderid':
                    return {'value': name,
                            'label': '订单编号', }
                elif name == 'accountid__nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }

            #def clean_search(self):
                #if self.qf == 'orderid':
                    ##if re.search('^\d*$', self.q):
                    #return self.q
                #if self.qf =='accountid__nickname':
                    #return self.qf
                #else:
                    #return super().clean_search()

        class filters(RowFilter):
            range_fields = ['createtime', 'confirmtime']
            names = ['status', 'amounttype']


class WithDrawForm(ModelFields):
    hide_fields = ['status', 'orderid', 'account', 'confirmtime', 'memo', ]

    class Meta:
        model = TbWithdraw
        fields = ['orderid', 'account', 'memo', 'status', 'confirmtime']

    def getExtraHeads(self):
        return [{'name': 'fakememo', 'editor': 'blocktext', 'required': True, 'label': '备注'}]

    def dict_head(self, head):
        if head['name'] == 'memo':
            head['editor'] = 'blocktext'
            head['required'] = True
        else:
            head['readonly'] = True
        return head

    def after_save(self):
        if 'status' in self.changed_data and self.instance.status == 1:  # 审核异常单
            notifyWithdraw(self.instance.accountid_id, self.instance.orderid)
    
    def clean_save(self):
        # super().save_form()
        if 'status' in self.changed_data and self.instance.status == 1:  # 审核异常单
            self.instance.memo = (self.instance.memo or '') + '\r\n' + self.kw.get('fakememo')
            self.instance.confirmtime = datetime.now()
            self.instance.save()
            ex_log = {'memo': self.kw.get('fakememo'), }
            # self.instance.save()
        elif 'status' in self.changed_data and self.instance.status == 2:  # 确认到账
            self.instance.memo += '\r\n' + self.kw.get('fakememo')
            self.instance.confirmtime = datetime.now()
            with transaction.atomic():
                self.instance.save()
                TbMessageUnsend.objects.create(
                    body='提现订单【{0}】,成功提现{1}元'.format(self.instance.orderid, self.instance.amount), type=3,
                    sender='system',
                    createtime=datetime.now(),
                    accountid=self.instance.accountid_id)
            ex_log = {'content': '提现订单【{0}】,成功提现{1}元'.format(self.instance.orderid, self.instance.amount),
                      'memo': self.kw.get('fakememo')}
        elif 'status' in self.changed_data and self.instance.status == 5:  # 退款
            self.instance.memo += '\r\n' + self.kw.get('fakememo')
            self.instance.confirmtime = datetime.now()
            # self.instance.save()
            category = 35
            if self.instance.amounttype == 1:
                beforamount = self.instance.accountid.amount
                self.instance.accountid.amount += self.instance.amount
                afteramount = self.instance.accountid.amount #+ self.instance.amount
            elif self.instance.amounttype == 2:
                beforamount = self.instance.accountid.agentamount
                self.instance.accountid.agentamount += self.instance.amount
                afteramount = self.instance.accountid.agentamount #+ self.instance.amount
                category = 36
            with transaction.atomic():
                self.instance.accountid.save()
                TbBalancelog.objects.create(account=self.instance.accountid.nickname, beforeamount=beforamount,
                                            amount=self.instance.amount, afteramount=afteramount, creater='system',
                                            memo='提现退款', accountid=self.instance.accountid, categoryid_id=category,
                                            cashflow=1)
                TbMessageUnsend.objects.create(body='提现订单【{0}】处理失败'.format(self.instance.orderid), type=3,
                                               sender='system',
                                               createtime=datetime.now(),
                                               accountid=self.instance.accountid_id)
            ex_log = {
                'content': '提现订单【{0}】处理失败'.format(self.instance.orderid),
                'memo': '提现退款'}
        return ex_log

@director_view("has_audit_ticketmaster")
def has_audit_ticketmaster(accountid):
    audit_count = TbTicketmaster.objects.filter(accountid_id = accountid).exclude(audit = 0).count()
    if audit_count >0:
        return True
    else:
        return False

@director_view('tab.ticketmaster')
class TicketmasterTab(TicketMasterPage.tableCls):
    @classmethod
    def get_edit_director_name(cls):
        return TicketMasterPage.tableCls.get_edit_director_name()
    
    @classmethod
    def clean_search_args(cls, search_args):
        search_args = TicketMasterPage.tableCls.clean_search_args(search_args)
        search_args['_need_audit']='1'
        return search_args
    
    def inn_filter(self, query):
        query = super().inn_filter(query)
        if self.kw.get('accountid'):
            return query.filter(accountid=self.kw.get('accountid'))
        else:
            return query

director.update({
    'Withdraw': WithdrawPage.tableCls,
    'Withdraw.edit': WithDrawForm,
})

page_dc.update({
    'withdraw': WithdrawPage,
})
