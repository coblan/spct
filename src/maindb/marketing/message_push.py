from helpers.director.shortcut import ModelTable,TablePage,director,page_dc,ModelFields
from maindb.models import TbMessage
from django.utils.html import strip_tags

class MessagePage(TablePage):
    def get_label(self):
        return '消息推送'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbMessage
        exclude =[]
    
class MessageForm(ModelFields):
    
    hide_fields=['sender','abstract']
    
    class Meta:
        model = TbMessage
        exclude =[]
    
    def clean_save(self):
        self.instance.sender = self.crt_user.username
        self.instance.abstract = strip_tags( self.instance.content)[:50]
    
 
director.update({
    'message':MessagePage.tableCls,
    'message.edit':MessageForm,
})
    
page_dc.update({
    'message':MessagePage
})