import datetime

from django.db.models import Sum

from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, get_request_cache, RowFilter
from helpers.director.table.row_search import SelectSearch
from helpers.director.table.table import RowSort
from ..models import TbAgentcommission
import requests
import urllib
from django.conf import settings
import json
import logging

req_log = logging.getLogger('general_log')

class AgentCommission(TablePage):
    template = 'jb_admin/table_new.html'

    def get_label(self):
        return '代理佣金'

    class tableCls(ModelTable):
        model = TbAgentcommission
        exclude = ['agent', 'description', 'creater', 'updater', 'updatetime']
        sort = ['accountid', 'amount']
        fields_sort = ['commid', 'accountid', 'amount', 'status', 'daus', 'betamount', 'bonusamount', 'expendamount',
                       'rechargeamount', 'withdrawalamount', 'lostamount', 'balancelostamount',
                       'percentage', 'settleyear', 'settlemonth', 'settledate', 'createtime', 'applytime']

        def dict_head(self, head):
            dc = {
                'commid': 80,
                'accountid': 120,
                'amount': 100,
                'daus': 100,
                'lostamount': 120,
                'betamount': 120,
                'bonusamount': 120,
                'expendamount': 120,
                'rechargeamount': 120,
                'withdrawalamount': 120,
                'balancelostamount': 120,
                'settledate': 100,
                'createtime': 140,
                'applytime': 140
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def statistics(self, query):
            dc = query.aggregate(total_amount=Sum('amount'), total_daus=Sum('daus'), total_lostamount=Sum('lostamount'),
                                 total_balancelostamount=Sum('balancelostamount'), total_betamount=Sum('betamount'),
                                 total_bonusamount=Sum('bonusamount'), total_expendamount=Sum('expendamount'),
                                 total_rechargeamount=Sum('rechargeamount'),
                                 total_withdrawalamount=Sum('withdrawalamount')
                                 )
            mapper = {
                'amount': 'total_amount',
                'daus': 'total_daus',
                'lostamount': 'total_lostamount',
                'balancelostamount': 'total_balancelostamount',
                'betamount': 'total_betamount',
                'bonusamount': 'total_bonusamount',
                'expendamount': 'total_expendamount',
                'rechargeamount': 'total_rechargeamount',
                'withdrawalamount': 'total_withdrawalamount'
            }
            for k in dc:
                dc[k] = str(round(dc[k], 2)) if dc[k] else ''
            footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            self.footer = footer
            self.footer = ['合计'] + self.footer
            return query

        class sort(RowSort):
            names = ['accountid', 'amount', 'daus', 'lostamount', 'balancelostamount', 'betamount', 'bonusamount',
                     'expendamount', 'rechargeamount', 'withdrawalamount']

        class search(SelectSearch):
            names = ['accountid__nickname']

            def get_option(self, name):
                if name == 'accountid__nickname':
                    return {'value': 'accountid__nickname', 'label': '用户昵称', }
                else:
                    return super().get_option(name)

        class filters(RowFilter):
            names = ['status','settleyear','settlemonth']

        def get_operation(self):
            return [
                #{'fun': 'director_call',
                 #'director_name': 'agent_commission.audit',
                 #'editor': 'com-op-btn',
                 #'label': '审核通过',
                 #'row_match': 'many_row_match',
                 #'match_msg': '只能选择待审核的数据！',
                 #'match_field': 'status',
                 #'match_values': [0],
                 #'confirm_msg': '确认审核通过？', 
                 #'visible': self.permit.can_edit(),
                 #},
                #{
                    #'fun': 'director_call',
                    #'editor': 'com-op-btn',
                    #'label': '一键审核',
                    #'director_name': 'agent_commission.onekey_all',
                    #'after_call': 'get_data',
                    #'confirm_msg': '确认审核通过所有订单？',
                    #'visible': self.permit.can_edit(),
                #}
            ]
        
        @staticmethod
        def onekey_audit_all(**kws): 
            url = urllib.parse.urljoin(settings.AGENT_SERVICE, '/comm/audit')
            cache = get_request_cache()
            request = cache['request']
            user = request.user
            data = json.dumps({'CommIDs': [],'OperatorName': user.username, 'AuditAll': True,})
            rt = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
            req_log.info(json.dumps({'url': url, 'data': data,'return': rt.text,}))
            dc = json.loads(rt.text)
            if not dc.get('success'):
                raise UserWarning(dc.get('error_description'))      
            return {'status': 'success',}
           

        @staticmethod
        def audit(rows):
            """
            {data:[{Key:'Success','Value':[]},{Key:'Fail',Value:[]}],
            error_description:'xxx',
            success:true
            }
            
            """
            url = urllib.parse.urljoin(settings.AGENT_SERVICE, '/comm/audit')
            comids = [row['commid'] for row in rows]
            cache = get_request_cache()
            request = cache['request']
            user = request.user
            data = json.dumps({'CommIDs': comids, 'OperatorName': user.username, })
            rt = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
            req_log.info(json.dumps({'url': url, 'data': data,'return': rt.text,}))
            
            dc = json.loads(rt.text)
            if dc.get('success'):
                rt_data = dc.get('data')
                success_rows = []
                fail_rows = []
                for item in rt_data:
                    if item['Key'] == 'Success':
                        success_rows = item['Value']
                    elif item['Key'] == 'Fail':
                        fail_rows = item['Value']

                rt_dc = {
                    'rows': [{'pk': row['pk'], 'status': 1, 'applytime': datetime.datetime.now()} for row in rows if
                             row['commid'] in success_rows]}
                if fail_rows:
                    rt_dc['msg'] = '这些 %s 行数据,操作不成功' % fail_rows
                return rt_dc
            else:
                raise UserWarning(dc.get('error_description'))


director.update({
    'agent_commission': AgentCommission.tableCls,
    'agent_commission.audit': AgentCommission.tableCls.audit, 
    'agent_commission.onekey_all': AgentCommission.tableCls.onekey_audit_all,
})

page_dc.update({
    'agent_commission': AgentCommission,
})
