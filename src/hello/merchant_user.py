from helpers.case.jb_admin.admin_user import UserPage,UserFields
from helpers.director.shortcut import page_dc,director
from .models import UserProfile
from maindb.models import TbMerchants

class Jb_with_merchant_User(UserPage):
    class tableCls(UserPage.tableCls):
        fields_sort = ['id','username','first_name','groups','is_superuser','is_staff','is_active','merchantid','last_login']
        def inn_filter(self, query):
            query = super().inn_filter(query)
            return query.select_related('userprofile')
        
        def dict_row(self, inst):
            return {
                'merchantid': inst.userprofile.merchantid if getattr(inst,'userprofile',None) else ''
            }
        
        def getExtraHead(self):
            heads = super().getExtraHead()
            heads.extend([
                {'name':'merchantid','label':'商户号'},
            ])
            return heads

class WithMerchantUserForm(UserFields):
    overlap_fields=['merchantid']
    def getExtraHeads(self):
        extra_ls = super().getExtraHeads()
        if not getattr(self.crt_user,'userprofile',None):
            extra_ls.extend([
                {'name':'merchantid','label':'商户号','editor':'com-field-linetext'}
            ])
        return extra_ls
    
    def dict_head(self, head):

        if head['name'] =='username':
            if getattr(self.crt_user,'userprofile',None):
                merchant = TbMerchants.objects.get(id=self.crt_user.userprofile.merchantid)
                head['prefix'] = merchant.merchantname + '_'
                head['class']='merchant-username'
                head['css']='.merchant-username input{width:19rem !important;}'
            #head['on_mounted'] = '''if(! scope.vc.row.pk){ Vue.set( scope.vc.head,'prefix','bba')  } '''
            head['readonly']='Boolean( scope.row.pk )'
        return head
    
    def after_save(self):
        if self.kw.get('merchantid'):
            count = UserProfile.objects.filter(user = self.instance).update(merchantid= self.kw.get('merchantid'))
            if not count:
                UserProfile.objects.create(user = self.instance,merchantid = self.kw.get('merchantid'))
    
    def dict_row(self, inst):
        dc = super().dict_row(inst) 
        dc.update({
            'merchantid':self.kw.get('merchantid','') 
        })
        return dc

director.update({
    'with_merchant_user':Jb_with_merchant_User.tableCls,
    'with_merchant_user.edit':WithMerchantUserForm
})

page_dc.update({
    'with_merchant_user':Jb_with_merchant_User
})