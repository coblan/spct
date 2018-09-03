from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, ModelFields, get_request_cache
from ..models import TbAgentcommission
import requests
import urllib
from django.conf import settings

class AgentCommission(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '代理佣金'
    
    class tableCls(ModelTable):
        model = TbAgentcommission
        exclude = []
    
        def get_operation(self): 
            return [
                 {'fun': 'director_rows', 
                  'director_name': 'agent_commission.audit', 
                  'editor': 'com-op-btn', 
                  'label': '审核通过', 
                  'after_save': 'update_or_insert_rows',
                  'row_match': 'many_row_match',
                  'match_field': 'status',
                  'match_values': [0],
                  'confirm_msg': '确认通过审核？'},
            ]
        
        @staticmethod
        def audit(rows): 
            url = urllib.parse.urljoin( settings.AGENT_SERVICE, '/comm/audit')
            comids = [row['commid'] for row in rows]
            cache = get_request_cache()
            request = cache['request']
            user = request.user
            rt = requests.post(url, data= {'CommIDs': comids, 'OperatorName': user.username,})
            print(rt.text)
        
        

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