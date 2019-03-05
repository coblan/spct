from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,ModelFields
from ..models import TbLimitusergroup

class LimitUserGroupPage(TablePage):
    def get_label(self):
        return '用户限额分组'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbLimitusergroup
        exclude=['extension','betbase']
        pop_edit_field='groupid'
        
        def dict_head(self, head):
            width_dc={
                'singleweight':120,
                'betmatch':120,
                'groupname':150,
                'description':150,
            }
            if width_dc.get(head['name']):
                head['width']=width_dc.get(head['name'])
            return head
        
        def get_operation(self):
            return []
    
class LimitUserForm(ModelFields):
    readonly=['groupid']
    class Meta:
        model = TbLimitusergroup
        exclude = ['extension','betbase']
    
    def dict_head(self, head):
        if head['name']=='singleweight':
            head['fv_rule']='range(0.001~5)'
        if head['name']=='betmatch':
            head['fv_rule']='range(1~1000)'
        return head

director.update({
    'limitusergroup':LimitUserGroupPage.tableCls,
    'limitusergroup.edit':LimitUserForm
})

page_dc.update({
    'limitusergroup':LimitUserGroupPage
})