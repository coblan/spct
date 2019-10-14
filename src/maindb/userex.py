from helpers.director.shortcut import TablePage,ModelFields,ModelTable,page_dc,director
from .models import TbUserex
from django.contrib.auth.models import User

class UserExPage(TablePage):
    def get_label(self):
        return '账号扩展信息'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbUserex
        exclude =['usedpassword']
        pop_edit_fields=['userid']

        def dict_head(self, head):
            if head['name']=='userid':
                head['inn_editor'] = 'com-table-label-shower'
            return head
        
        def dict_row(self, inst):
            user = User.objects.get(pk = inst.userid)
            return {
                '_userid_label':str(user)
            }

class UserExForm(ModelFields):
    class Meta:
        model = TbUserex
        exclude =['usedpassword']
    
    def dict_head(self, head):
        if head['name'] == 'userid':
            head['editor'] ='com-field-single-select2'
            head['options'] = [{'value':x.pk,'label':str(x)} for x in User.objects.all()]
        return head
    
    def dict_row(self, inst):
        dc ={}
        if inst.userid:
            user = User.objects.get(pk = inst.userid)
            dc.update( {
                '_userid_label':str(user)
            } )
        return  dc

director.update({
    'userex':UserExPage.tableCls,
    'userex.edit':UserExForm,
})

page_dc.update({
    'userex':UserExPage
})