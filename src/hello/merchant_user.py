from helpers.case.jb_admin.admin_user import UserPage,UserFields
from helpers.director.shortcut import page_dc,director,has_permit
from .models import UserProfile
from maindb.models import TbMerchants
from django.contrib.auth.models import User,Group

def get_user_merchantid(user):
    return 1

class Jb_with_merchant_User(UserPage):
    class tableCls(UserPage.tableCls):
        fields_sort = ['username','first_name','groups','is_superuser','is_staff','is_active','merchantid','last_login']
        def inn_filter(self, query):
            query = super().inn_filter(query)
            if has_permit(self.crt_user,'-i_am_merchant'):
                query = query.filter(userprofile__merchantid = get_user_merchantid(self.crt_user))
            return query.select_related('userprofile')
        
        def dict_row(self, inst):
            return {
                'merchantid': inst.userprofile.merchantid if getattr(inst,'userprofile',None) else ''
            }
        
        def get_heads(self):
            heads = super().get_heads()
            if has_permit(self.crt_user,'-i_am_merchant'):
                out_heads = []
                for head in heads:
                    if head['name'] != 'is_superuser':
                        out_heads.append(head)
            else:
                out_heads = heads
            return out_heads
        
        def getExtraHead(self):
            heads = super().getExtraHead()
            heads.extend([
                {'name':'merchantid','label':'商户号'},
            ])
            return heads

class WithMerchantUserForm(UserFields):
    overlap_fields=['merchantid']
    class Meta:
        model=User
        fields=['username','first_name','is_active','is_staff','groups', 'date_joined']
        
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
        if head['name'] =='groups' and has_permit(self.crt_user,'-i_am_merchant'):
            head['options']=[
                {'value':x.pk,'label':str(x)} for x in Group.objects.filter(name__startswith='商户-')
            ]
        
        return head
    
    def clean_dict(self, dc):
        dc = super().clean_dict(dc)
        if has_permit(self.crt_user,'-i_am_merchant') and not dc.get('pk') and dc.get('username'):
            merchant = TbMerchants.objects.get(id=self.crt_user.userprofile.merchantid)
            dc['username'] = merchant.merchantname + '_' + dc.get('username')
        return dc
    
    def after_save(self):
        merchantid = self.kw.get('merchantid')
        if has_permit(self.crt_user,'-i_am_merchant'):
            merchantid = self.crt_user.userprofile.merchantid
        if merchantid:
            count = UserProfile.objects.filter(user = self.instance).update(merchantid= merchantid)
            if not count:
                UserProfile.objects.create(user = self.instance,merchantid = merchantid)
    
    def dict_row(self, inst):
        dc = super().dict_row(inst) 
        if self.instance.pk:
            self.instance.refresh_from_db()
            if hasattr(self.instance,'userprofile'):
                dc.update({
                    'merchantid': self.instance.userprofile.merchantid
                })
        return dc

director.update({
    'with_merchant_user':Jb_with_merchant_User.tableCls,
    'with_merchant_user.edit':WithMerchantUserForm
})

page_dc.update({
    'with_merchant_user':Jb_with_merchant_User
})