from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,RowFilter
from ..models import TbVipbonus,TbProductContactUser,TbMoneyCategories
from django.db.models import Case,When,Value,Subquery,OuterRef

class VipBonusPage(TablePage):
    def get_label(self):
        return 'VIP红利记录'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbVipbonus
        exclude =[]
        
        def getExtraHead(self):
            return [
                {'name':'user_address','label':'收货地址','editor':'com-table-click','action':'cfg.showMsg(scope.row.user_address_detail)'}
            ]
        
        def inn_filter(self, query):
            #subque= TbProductContactUser.objects.filter(accountid = OuterRef('accountid'))
            #return query.annotate(user_address = Subquery(subque.values('userrealname')[:1]))
            return query.using('Sports_nolock').extra(select={'userrealname':'TB_Product_Contact_User.userrealname',
                                       'phone':'TB_Product_Contact_User.phone',
                                       'province':'TB_Product_Contact_User.province',
                                       'city':'TB_Product_Contact_User.city',
                                       'county':'TB_Product_Contact_User.county',
                                       'address':'TB_Product_Contact_User.address'},
                               where=['TB_Product_Contact_User.accountid=TB_VipBonus.accountid'],
                               tables=['TB_Product_Contact_User'])
        
        def dict_row(self, inst):
            dc = {
                'userrealname':inst.userrealname,
                'phone':inst.phone,
                'province':inst.province,
                'city':inst.city,
                'county':inst.county,
                'address':inst.address,
            }
            return {
                'user_address':inst.userrealname if inst.ruleid_id ==17 else '',
                'user_address_detail':'''<table>
                <tr><td style="width:50px;vertical-align:top">地址:</td><td>%(province)s|%(city)s|%(county)s|%(address)s</td></tr>
                <tr><td>姓名:</td><td>%(userrealname)s</td></tr>
                <tr><td>电话:</td><td>%(phone)s</td></tr> 
                </table>''' %dc 
            }
        
        class filters(RowFilter):
            names=['level','status','accountid__nickname']
            icontains=['accountid__nickname']
            range_fields=['createtime','arrivetime','drawtime']
            
            def getExtraHead(self):
                return [
                    {'name':'accountid__nickname','label':'账号昵称','editor':'com-filter-text'}
                ]
            
            #def clean_query(self, query):
                #if self.search_args.get('accountid__name'):
                    #pass
        
        

director.update({
    'vipbonus':VipBonusPage.tableCls
})

page_dc.update({
    'vipbonus':VipBonusPage
})