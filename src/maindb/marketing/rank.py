from helpers.director.shortcut import TablePage, ModelTable, ModelFields, page_dc, director, field_map, RowFilter, RowSearch
from ..models import TbUserConst, TbUserRank, TbParlayrules, TbUserConst
from django.core.exceptions import ValidationError

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
        
        class filters(RowFilter):
            names = ['type', 'enabled', 'parlayid', 'period']
        
        class search(RowSearch):
            names = ['userid__nickname']
            
            def get_context(self):
                """
                """
                dc = {
                    'search_tip':'用户昵称',
                    'editor':'com-search-filter',
                    'name':'_q'
                }
                return dc            
        
        #def dict_head(self, head):
            #if head['name'] == 'parlayid':
                #head['editor'] = 'com-table-mapper'
                #head['options'] = [{'value':x.parlayid, 'label':str(x)} for x in TbParlayrules.objects.all()]
            #return head        

class RankForm(ModelFields):
    class Meta:
        model = TbUserRank
        exclude = []
    
    def dict_head(self, head):
        if head['name'] not in ['value', 'enabled']:
            head['readonly'] = 'rt= scope.row.pk||scope.row.pk==0'
        
        if head['name'] == 'period':
            head['editor'] = 'com-field-select'
            head['placeholder'] = '请选择周期'
        if head['name'] == 'type':
            head['editor'] = 'com-field-select'
            head['placeholder'] = '请选择榜单'
            
        if head['name'] == 'userid':
            head['style'] = 'width:20em;'
            head['placeholder'] = '选择用户'
            head['editor'] = 'com-field-single-select2'  #  'com-field-single-chosen'# 
            head['options'] = [{'value':x.id, 'label':str(x)} for x in TbUserConst.objects.all()]
        if head['name'] == 'parlayid':
            head['placeholder'] = '请选择串关类型'
            head['fv_rule'] = 'required'
            head['show'] = 'rt=scope.row.type==2'
            head['editor'] = 'com-field-select'
            #head['options'] = [{'value':x.parlayid, 'label':str(x)} for x in TbParlayrules.objects.all()]
        #if head['name'] == 'value':
            #head['fv_express']:'rt='
            #head['fv_map'] = {
                #1: 'xxx',
                #2: 'bbb',
            #}
        
        return head
    
    def clean_dict(self, dc):
        dc = super().clean_dict(dc)
        if not dc.get('parlayid', None) or dc.get('type') != 2:  # 不是大奖榜，就置为 11  
            dc['parlayid'] = 11
        #dc['parlayid'] =  or 0
        return dc
    
    def clean_value(self):
        if self.kw.get('type') == 3:  #  胜率榜
            value = self.kw.get('value')
            if not 0 <= value <= 100:
                raise ValidationError('请填写0到100')
        return self.kw.get('value')
        
        
    
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
    