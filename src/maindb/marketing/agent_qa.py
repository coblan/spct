from helpers.director.shortcut import page_dc, director
from .notice import NoticePage, NoticeForm
from ..models import TbAgentqa

class AgentQAPage(NoticePage):
    def get_label(self): 
        return '代理QA'
    
    def get_tabs(self): 
        notice_form = AgentQAForm(crt_user=self.crt_user)
        ls = [
            {'name': 'notice_form',
             'label': '基本信息',
             'com': 'com-tab-fields',
             'get_data': {
                 'fun': 'table_row',
                 # 'kws':{
                 # 'director_name':help_form.get_director_name(),
                 # 'relat_field':'pk',
                 # }
             },
             'after_save': {
                 'fun': 'update_or_insert'
             },
             'heads': notice_form.get_heads(),
             'ops': notice_form.get_operations()
             },
        ]
        return {
            'notice_tabs':ls
        }         
    
    class tableCls(NoticePage.tableCls):
        model = TbAgentqa
        exclude = ['id']

class AgentQAForm(NoticeForm):
    class Meta:
        model = TbAgentqa
        exclude = []
    hide_fields = ['createuser']
    

director.update({
    'agent_qa': AgentQAPage.tableCls,
    'agent_qa.edit': AgentQAForm,
})
page_dc.update({
    'agent_qa': AgentQAPage,
})