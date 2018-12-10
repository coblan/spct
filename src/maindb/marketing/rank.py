from helpers.director.shortcut import TablePage, ModelTable, ModelFields, page_dc, director, field_map
from ..models import TbUserConst, TbUserRank, TbParlayrules

class RankUserPage(TablePage):
    def get_label(self):
        return '虚拟用户信息'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        pop_edit_field = 'id'
        model = TbUserConst
        exclude = []
        

class RankUserForm(ModelFields):
    class Meta:
        model = TbUserConst
        exclude = []

class RankPage(TablePage):
    def get_label(self):
        return '虚拟排行榜'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    class tableCls(ModelTable):
        pop_edit_field = 'id'
        model = TbUserRank
        exclude = []
        
        def dict_head(self, head):
            if head['name'] == 'parlayid':
                head['editor'] = 'com-table-mapper'
                head['options'] = [{'value':x.parlayid, 'label':str(x)} for x in TbParlayrules.objects.all()]
            return head        

class RankForm(ModelFields):
    class Meta:
        model = TbUserRank
        exclude = []
    
    def dict_head(self, head):
        if head['name'] not in ['value', 'enabled']:
            head['readonly'] = 'rt= scope.row.pk||scope.row.pk==0'
            
        if head['name'] == 'parlayid':
            head['show'] = 'rt=scope.row.type==2'
            head['editor'] = 'sim_select'
            head['options'] = [{'value':x.parlayid, 'label':str(x)} for x in TbParlayrules.objects.all()]
        
        return head
    
    def clean_dict(self, dc):
        dc = super().clean_dict(dc)
        if not dc.get('parlayid', None):
            dc['parlayid'] = 0
        #dc['parlayid'] =  or 0
        return dc
    
    
    
    def clean(self):
        if not self.instance.pk:
            userid = self.kw.get('userid')
            type = self.kw.get('type')
            parlayid = self.kw.get('parlayid')
            period = self.kw.get('period')
            if TbUserRank.objects.filter(userid = userid, type = type, parlayid = parlayid, period = period, ).exists():
                raise UserWarning('用户，榜单，串关类型，周期 相同的记录已经存在')
            
        
        


director.update({
    'rankuser': RankUserPage.tableCls,
    'rankuser.edit': RankUserForm,
    'rank': RankPage.tableCls,
    'rank.edit': RankForm,
})

page_dc.update({
    'rankuser': RankUserPage,
    'rank': RankPage,
})
    