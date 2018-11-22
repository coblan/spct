from helpers.director.shortcut import page_dc, director, field_map, model_to_name
from .notice import NoticePage, NoticeForm
from ..models import TbAgentqa
from django.contrib.auth.models import User

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

        def get_operation(self):
            return super().get_operation()[:-1]
        
        #def dict_head(self, head): 
            #super().dict_head(head)
            #if head['name'] == 'createuser':
                #head['editor'] = 'com-table-label-shower'
            #return head
            
        #def dict_row(self, inst): 
            #dc = super().dict_row(inst)
            #if inst.createuser:
                #user =  User.objects.get(pk = inst.createuser)
                #user_label = str(user)
            #else:
                #user_label = ''
            #dc.update( {
                #'_createuser_label': user_label,
            #})
            #return dc

class AgentQAForm(NoticeForm):
    class Meta:
        model = TbAgentqa
        exclude = []
    readonly = ['createuser']
    
    def save_form(self): 
        if not self.instance.pk:
            self.instance.createuser = self.crt_user.pk
        return super().save_form()
    
    #def dict_row(self, row): 
        #dc = super().dict_row(row)
        #if self.instance.createuser:
            #user =  User.objects.get(pk = inst.createuser)
            #user_label = str(user)
        #else:
            #user_label = ''
            
        #dc.update({
            #'_createuser_label': user_label,
        #})
        #return dc
    


director.update({
    'agent_qa': AgentQAPage.tableCls,
    'agent_qa.edit': AgentQAForm,
})
page_dc.update({
    'agent_qa': AgentQAPage,
})