from helpers.case.jb_admin.admin_user import UserPage,UserFields
from helpers.director.shortcut import page_dc,director,has_permit,RowFilter
from .models import UserProfile
from maindb.models import TbMerchants
from django.contrib.auth.models import User,Group

class MerchantInstancCheck(object):
    def clean(self):
        if self.crt_user.merchant:
            if hasattr(self.instance,'merchant'):
                if self.instance.merchant != self.crt_user.merchant:
                    raise UserWarning('没有权限修改该数据') 
            elif self.kw.get('merchant'):
                if self.kw.get('merchant') != self.crt_user.merchant.id:
                    raise UserWarning('没有权限修改该数据') 
        return super().clean()

def get_user_merchantid(user,default=None):
    if has_permit(user,'-i_am_merchant'):
        return user.userprofile.merchantid
    else:
        return default

def get_user_merchant(user,default=None):
    if has_permit(user,'-i_am_merchant'):
        return  TbMerchants.objects.get(id= user.userprofile.merchantid  )
    else:
        return default

class Jb_with_merchant_User(UserPage):
    class tableCls(UserPage.tableCls):
        fields_sort = ['username','first_name','groups','is_superuser','is_staff','is_active','merchantid','last_login']
        
        def inn_filter(self, query):
            self.merchant_map = {x.pk:str(x) for x in TbMerchants.objects.all() }
            query = super().inn_filter(query)
            if self.crt_user.merchant:
                query = query.filter(userprofile__merchantid = self.crt_user.merchant.id)
            query = query.filter(userprofile__merchantid__isnull=False)
            return query.select_related('userprofile')
        
        def dict_row(self, inst):
            return {
                'merchantid': inst.userprofile.merchantid if getattr(inst,'userprofile',None) else '',
                '_merchantid_label':self.merchant_map[ inst.userprofile.merchantid ]
            }
         
        def get_heads(self):
            heads = super().get_heads()
            if self.crt_user.merchant:
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
                {'name':'merchantid','label':'商户','editor':'com-table-label-shower'},
            ])
            return heads
        
        def get_operation(self):
            ops = super().get_operation()
            out = []
            for op in ops:
                if op.get('name') =='delete_selected':
                    pass
                else:
                    out.append(op)
            return out
        
        class filters(RowFilter):
            names=['first_name','groups__name','is_superuser','is_staff','is_active','userprofile__merchantid']
            icontains=['first_name','groups__name']
            
            def getExtraHead(self):
                return [
                    {'name':"userprofile__merchantid",'label':'商户','editor':'com-filter-select','options':[
                        {'value':x.pk,'label':str(x)} for x in TbMerchants.objects.all()
                        ],'visible':not self.crt_user.merchant},
                    {'name':'groups__name','label':'权限分组','show':'!scope.ps.search_args.groups_id'}
                ]
            
            

class WithMerchantUserForm(UserFields):
    overlap_fields=['merchantid']
    class Meta:
        model=User
        fields=['username','first_name','is_active','is_staff','groups', 'date_joined']
        
    def getExtraHeads(self):
        extra_ls = super().getExtraHeads()
        if not getattr(self.crt_user,'userprofile',None):
            extra_ls.extend([
                {'name':'merchantid','label':'商户号','required':True,'editor':'com-field-select','options':[
                    {'value':x.pk,'label':str(x)} for x in TbMerchants.objects.all()
                    ]}
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
        if head['name'] =='groups':
            head['options']=[
                {'value':x.pk,'label':str(x)} for x in Group.objects.filter(name__startswith='商户-')
            ]
        
        return head
    
    def clean_dict(self, dc):
        dc = super().clean_dict(dc)
        if self.crt_user.merchant and not dc.get('pk') and dc.get('username'):
            merchant = TbMerchants.objects.get(id=self.crt_user.userprofile.merchantid)
            dc['username'] = merchant.merchantname + '_' + dc.get('username')
        return dc
    
    def after_save(self):
        merchantid = self.kw.get('merchantid')
        if self.crt_user.merchant:
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
                merchant = TbMerchants.objects.get(pk=self.instance.userprofile.merchantid )
                dc.update({
                    'merchantid': self.instance.userprofile.merchantid,
                    '_merchantid_label':str(merchant)
                })
        return dc

director.update({
    'with_merchant_user':Jb_with_merchant_User.tableCls,
    'with_merchant_user.edit':WithMerchantUserForm
})

page_dc.update({
    'with_merchant_user':Jb_with_merchant_User
})