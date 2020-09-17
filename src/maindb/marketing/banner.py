# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSort, RowFilter,has_permit
from ..models import TbBanner
from ..status_code import *
from django.contrib.auth.models import User
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from hello.merchant_user import MerchantInstancCheck

class BannerPage(TablePage):
    template = 'jb_admin/table.html'  # 'jb_admin/table_with_height.html'

    class tableCls(ModelTable):
        model = TbBanner
        include = ['merchant','title', 'navigateurl','displaytype','status', 'picturename','pcpicturename', 'order', 'createuser', 'createtime', 'description']
        pop_edit_fields=['title']
        def get_context(self):
            ctx = ModelTable.get_context(self)
            #ctx['extra_table_logic'] = 'banner_logic'
            return ctx

        @classmethod
        def clean_search_args(cls, search_args):
            if not search_args.get('_sort'):
                search_args['_sort'] = '-createtime'
            return search_args
        
        def inn_filter(self, query):
            if self.crt_user.merchant:
                return query.filter(merchant = self.crt_user.merchant )
            else:
                return query
        
        def dict_head(self, head):
            dc = {
                'title': 180,
                'picturename': 160,
                'order': 100,
                'createtime': 160,
                'createuser': 100,
                'description': 250,
                'status': 60
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])

            if head['name'] in ['createuser']:
                head['editor'] = 'com-table-label-shower'

            if head['name'] in ['status']:
                head['editor'] = 'com-table-bool-shower'
                head['options'] = [{'value': x[0], 'label': x[1], } for x in ONLINE_STATUS]  # dict( ONLINE_STATUS )

            #if head['name'] == 'title':
                #head['editor'] ='com-table-click'
                #head['fields_ctx'] = BannerForm().get_head_context()
                #head['action'] = 'cfg.show_load();ex.director_call("banner.table.edit",{pk:scope.row.pk}).then(resp=>{cfg.hide_load();scope.head.fields_ctx.row=resp.row; return cfg.pop_vue_com("com-form-one",scope.head.fields_ctx) }).then(row=>{ex.vueAssign(scope.row,row)}) '
                ##head['editor'] = 'com-table-pop-fields'
                ##head['fields_ctx'] = BannerForm(crt_user=self.crt_user).get_head_context()
                ##head['get_row'] = {
                    ##'fun': 'get_with_relat_field',
                    ##'kws': {
                        ##"director_name": 'banner.table.edit',
                        ##'relat_field': 'pk'
                    ##}
                ##}
                ##head['after_save'] = {
                    ### 'fun':'do_nothing'
                    ##'fun': 'update_or_insert'
                ##}

            return head

        #def dict_row(self, inst):
            #return {
                #'_createuser_label': str(User.objects.get(pk=inst.createuser)) if inst.createuser else "",
            #}

        def get_operation(self):
            ops = [ModelTable.get_operation(self)[0]]
            ops.extend([
                {
                    #'fun': 'selected_set_and_save',
                    #'editor': 'com-op-btn',
                    'editor':'com-btn',
                    'action':'scope.ps.check_selected(scope.head).then(()=>{scope.ps.selected_set_and_save(scope.head)})',
                    'label': '在线',
                    'field': 'status',
                    'value': 1,
                    'row_match': 'many_row',
                    'confirm_msg': '确认修改为在线吗?', 
                    'visible': self.permit.can_edit(),
                },
                {
                    #'fun': 'selected_set_and_save',
                    #'editor': 'com-op-btn',
                    'editor':'com-btn',
                    'action':'scope.ps.check_selected(scope.head).then(()=>{scope.ps.selected_set_and_save(scope.head)})',
                    'label': '离线',
                    'field': 'status',
                    'value': 0,
                    'row_match': 'many_row',
                    'confirm_msg': '确认修改为离线吗?', 
                    'visible': self.permit.can_edit(),
                }
            ])
            return ops

        class filters(RowFilter):
            
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['status']
                else:
                    return ['merchant','status']


        # class search(RowSearch):
        # names=['channel']
        class sort(RowSort):
            names = ['name', 'order', 'createtime']

    def get_label(self):
        return 'Banner管理'


class BannerForm(MerchantInstancCheck,ModelFields):
    readonly = []
    
    @property
    def field_sort(self):
        if self.crt_user.merchant:
            return ['title', 'navigateurl', 'picturename','pcpicturename', 'order', 'description']
        else:
            return ['title', 'navigateurl', 'picturename','pcpicturename', 'order', 'description','merchant']
    #field_sort = ['title', 'navigateurl', 'picturename','pcpicturename', 'order','displaytype', 'description','merchant']

    class Meta:
        model = TbBanner
        exclude = []
        # fields=['title','navigateurl','picturename','order','description']

    def dict_head(self, head):
        if head['name'] in ['picturename','pcpicturename']:
            if self.crt_user.merchant:
                head['up_url'] = '/d/upload?path=public/%s/banner'%self.crt_user.merchant.merchantname
            else:
                head['up_url'] = '/d/upload?path=public/banner'
        if head['name'] == 'createuser':
            head['editor'] = 'com-field-label-shower'
        if head['name'] =='navigateurl':
            head['explain_text'] = '''
<ol>
<li>活动：/sh/activityv2/5.html?_nt=activity&id=5</li>
<li>比赛：sh://www.sh.com/match/detail?_nt=match&id=1000</li>
<li>消息：sh://www.sh.com/message/detail?_nt=message&id=1000</li>
<li>充值：sh://www.sh.com/user/recharge?_nt=recharge</li>
<li>绝对url：Htttps://www.baidu.com</li>
</ol>
sh为商户英文名称
                                   '''
        #if head['name'] == 'displaytype':
            #head['editor'] = 'com-field-radio'
        return head

    def dict_row(self, row):
        return {
            'createtime': row.createtime.strftime('%Y-%m-%d %H:%M:%S') if row.createtime else None,
            '_createuser_label': str(User.objects.get(pk=row.createuser)) if row.createuser else "",
            # 'picturename':'/media/banner/'+row.picturename if row.picturename else ""
        }

    def clean_dict(self, dc):
        if self.crt_user.merchant:
            dc['merchant'] = self.crt_user.merchant.id
        return dc
        
    def save_form(self):
        ModelFields.save_form(self)
        if not self.instance.createuser:
            self.instance.createuser = self.crt_user.pk
            self.instance.save()
        return self.instance


director.update({
    'banner.table': BannerPage.tableCls,
    'banner.table.edit': BannerForm,
})

page_dc.update({
    'banner': BannerPage
})
