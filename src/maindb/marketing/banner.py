# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSort, RowFilter
from ..models import TbBanner
from ..status_code import *
from django.contrib.auth.models import User
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc


class BannerPage(TablePage):
    template = 'jb_admin/table.html'  # 'jb_admin/table_with_height.html'
    extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]

    class tableCls(ModelTable):
        model = TbBanner
        include = ['title', 'status', 'picturename', 'order', 'createuser', 'createtime', 'description']

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['extra_table_logic'] = 'banner_logic'
            return ctx

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
                head['editor'] = 'com-table-mapper'

                head['options'] = [{'value': x[0], 'label': x[1], } for x in ONLINE_STATUS]  # dict( ONLINE_STATUS )

            if head['name'] == 'title':
                head['editor'] = 'com-table-pop-fields'
                head['fields_ctx'] = BannerForm(crt_user=self.crt_user).get_head_context()
                # head['fields_heads']=BannerForm(crt_user=self.crt_user).get_heads()
                head['get_row'] = {
                    # 'fun':'use_table_row'
                    # "fun":'get_table_row'
                    'fun': 'get_with_relat_field',
                    'kws': {
                        "director_name": 'banner.table.edit',
                        'relat_field': 'pk'
                    }
                }
                head['after_save'] = {
                    # 'fun':'do_nothing'
                    'fun': 'update_or_insert'
                }

            return head

        def dict_row(self, inst):
            return {
                '_createuser_label': str(User.objects.get(pk=inst.createuser)) if inst.createuser else "",
            }

        def get_operation(self):
            ops = ModelTable.get_operation(self)
            ops.extend([
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '在线',
                    'field': 'status',
                    'value': 1,
                    'row_match': 'one_row',
                    'confirm_msg': '确认修改为在线吗?'
                },
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '离线',
                    'field': 'status',
                    'value': 0,
                    'row_match': 'one_row',
                    'confirm_msg': '确认修改为离线吗?'
                }
            ])
            return ops

        class filters(RowFilter):
            names = ['status']

        # class search(RowSearch):
        # names=['channel']
        class sort(RowSort):
            names = ['name', 'order', 'createtime']

    def get_label(self):
        return 'Banner管理'


class BannerForm(ModelFields):
    readonly = ['createuser']
    field_sort = ['title', 'navigateurl', 'picturename', 'order', 'description']

    class Meta:
        model = TbBanner
        exclude = []
        # fields=['title','navigateurl','picturename','order','description']

    def dict_head(self, head):
        if head['name'] == 'picturename':
            head['up_url'] = '/d/upload?path=public/banner'
        if head['name'] == 'createuser':
            head['editor'] = 'com-field-label-shower'
        return head

    def dict_row(self, row):
        return {
            'createtime': row.createtime.strftime('%Y-%m-%d %H:%M:%S') if row.createtime else None,
            '_createuser_label': str(User.objects.get(pk=row.createuser)) if row.createuser else "",
            # 'picturename':'/media/banner/'+row.picturename if row.picturename else ""
        }

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
