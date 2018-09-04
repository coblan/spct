from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, ModelFields, get_request_cache, RowFilter
from ..models import TbAgentcommission
import requests
import urllib
from django.conf import settings
import json

class AgentCommission(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '代理佣金'
    
    class tableCls(ModelTable):
        model = TbAgentcommission
        exclude = []
        
        class filters(RowFilter):
            names = ['status']
        
        def get_operation(self): 
            return [
                 {'fun': 'director_rows', 
                  'director_name': 'agent_commission.audit', 
                  'editor': 'com-op-btn', 
                  'label': '审核通过', 
                  'after_call': 'update_or_insert_rows',
                  'row_match': 'many_row_match',
                  'match_msg': '请全部选择未审核的数据行！',
                  'match_field': 'status',
                  'match_values': [0],
                  'confirm_msg': '确认通过审核？'},
            ]
        
        @staticmethod
        def audit(rows): 
            """
            {data:[{Key:'Success','Value':[]},{Key:'Fail',Value:[]}],
            error_description:'xxx',
            success:true
            }
            
            """
            url = urllib.parse.urljoin( settings.AGENT_SERVICE, '/comm/audit')
            comids = [row['commid'] for row in rows]
            cache = get_request_cache()
            request = cache['request']
            user = request.user
            data = json.dumps({'CommIDs': comids, 'OperatorName': user.username,})
            rt = requests.post(url, data= data, headers = {'Content-Type': 'application/json'})
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
                
                rt_dc = {'rows': [{'pk':row['pk'], 'status': 1,} for row in rows if row['commid'] in success_rows]}
                if fail_rows:
                    rt_dc['msg'] = '这些 %s 行数据,操作不成功' % fail_rows
                return rt_dc
            else:
                raise UserWarning(dc.get('error_description')) 
        
        

#class AgentCommissionForm(ModelFields):
    #class Meta:
        #model = TbAgentcommission
        #exclude = []
    
    #def save_form(self):
        #if 'status'in self.changed_data and self.cleaned_data['status'] == 1:
            #req
        #print('hell')
        

director.update({
    'agent_commission': AgentCommission.tableCls,
    'agent_commission.audit': AgentCommission.tableCls.audit,
    #'agent_commission.edit': AgentCommissionForm,
})

page_dc.update({
    'agent_commission': AgentCommission,
})