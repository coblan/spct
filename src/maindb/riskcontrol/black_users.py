# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable, TablePage, page_dc, ModelFields, RowSearch, director
from ..models import Blackiprangelist, \
    Whiteiplist, Whiteuserlist, TbAccount


class BlackIPRangeListPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '登录IP黑名单'

    class tableCls(ModelTable):
        model = Blackiprangelist
        exclude = []
        hide_fields = ['startipnum', 'endipnum']
        pop_edit_field = 'blackiprangelistid'

        def dict_head(self, head):
            dc = {
                'startip': 120,
                'endip': 120
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def get_operation(self):
            create = super().get_operation()[0]
            return [create,
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '启用',
                        'field': 'iswork',
                        'value': True,
                        'row_match': 'many_row',
                        'confirm_msg': '确认启用该IP黑名单范围吗?', 
                        'visible': 'iswork' in self.permit.changeable_fields(),
                    },
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '禁用',
                        'field': 'iswork',
                        'value': False,
                        'row_match': 'many_row',
                        'confirm_msg': '确认禁用该IP黑名单范围吗?', 
                        'visible': 'iswork' in self.permit.changeable_fields(),
                    }
                    ]


class BlackIPRangeForm(ModelFields):
    hide_fields = ['startipnum', 'endipnum']

    class Meta:
        model = Blackiprangelist
        exclude = []

    def dict_head(self, head):
        if head['name'] in ['startip', 'endip']:
            head['fv_rule'] = 'ip'
        if head['name'] in ['startipnum', 'endipnum']:
            head['readonly'] = True
        return head

    def clean_dict(self, dc):
        super().clean_dict(dc)
        if dc.get('startip'):
            dc['startipnum'] = ip2num(dc.get('startip'))
        else:
            dc['startipnum'] = 0

        if dc.get('endip'):
            dc['endipnum'] = ip2num(dc.get('endip'))
        else:
            dc['endipnum'] = 0
        return dc


class WhiteIpListPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return 'IP白名单'

    class tableCls(ModelTable):
        model = Whiteiplist
        pop_edit_field = 'whiteiplistid'

        def dict_head(self, head):
            dc = {
                'whiteiplistid': 120,
                'ip': 120,
                'remark': 150,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def get_operation(self):
            create = super().get_operation()[0]
            return [create,
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '启用',
                        'field': 'iswork',
                        'value': True,
                        'row_match': 'many_row',
                        'confirm_msg': '确认启用该IP白名单吗?', 
                        'visible': 'iswork' in self.permit.changeable_fields(),
                    },
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '禁用',
                        'field': 'iswork',
                        'value': False,
                        'row_match': 'many_row',
                        'confirm_msg': '确认禁用该IP白名单吗?', 
                        'visible': 'iswork' in self.permit.changeable_fields(),
                    }
                    ]


class WhiteIPForm(ModelFields):
    class Meta:
        model = Whiteiplist
        exclude = []

    def dict_head(self, head):
        if head['name'] == 'ip':
            head['fv_rule'] = 'ip'
        return head


class WhiteUserListPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '用户白名单'

    class tableCls(ModelTable):
        model = Whiteuserlist
        exclude = ['addtime']
        pop_edit_field = 'whiteuserlistid'

        def dict_head(self, head):
            if head['name'] in ('account', 'memo'):
                head['width'] = 150
            return head

        def get_operation(self):
            opes = super().get_operation()
            ls = []
            if opes:
                ls.append(opes[0])
            ls.extend( [
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '启用',
                        'field': 'iswork',
                        'value': True,
                        'row_match': 'many_row',
                        'confirm_msg': '确认启用该用户白名单吗?', 
                        'visible': 'iswork' in self.permit.changeable_fields(),
                    },
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '禁用',
                        'field': 'iswork',
                        'value': False,
                        'row_match': 'many_row',
                        'confirm_msg': '确认禁用该用户白名单吗?', 
                         'visible': 'iswork' in self.permit.changeable_fields(),
                    }
                    ])
            return ls


class WhiteUserForm(ModelFields):
    class Meta:
        model = Whiteuserlist
        exclude = ['addtime']

    def dict_head(self, head):
        if head['name'] == 'account':
            table_obj = AccountSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
        return head


class AccountSelect(ModelTable):
    selectable = False
    model = TbAccount
    include = ['accountid', 'nickname', ]
    
    def inn_filter(self, query):
        if self.crt_user.merchant:
            query = query.filter(merchant = self.crt_user.merchant)
        return query
    
    def dict_head(self, head):
        dc = {
            'accountid': 100,
            'nickname': 150,
        }
        if dc.get(head['name']):
            head['width'] = dc.get(head['name'])

        if head['name'] == 'accountid':
            head['editor'] = 'com-table-foreign-click-select'
        return head

    def dict_row(self, inst):
        return {
            'account': inst.accountid,
        }

    class search(RowSearch):
        names = ['accountid', 'nickname']


def ip2num(ip):
    arr = ip.split('.')
    num = 256 * 256 * 256 * int(arr[0]) + 256 * 256 * int(arr[1]) + 256 * int(arr[2]) + int(arr[3])
    return num


director.update({
    # 'risk.TbBlackuserlistPage': BlackUserListPage.tableCls,
    # 'risk.TbBlackuserlistPage.edit': BlackUserForm,
    # 'risk.TbBlackuserlistLogPage': BlackUserListLogPage.tableCls,

    'risk.WhiteIpListPage': WhiteIpListPage.tableCls,
    'risk.WhiteIpListPage.edit': WhiteIPForm,

    'risk.WhiteuserlistPage': WhiteUserListPage.tableCls,
    'risk.WhiteuserlistPage.edit': WhiteUserForm,
    'risk.AccountSelect': AccountSelect,

    'risk.BlankipRangeListPage': BlackIPRangeListPage.tableCls,
    'risk.BlankipRangeListPage.edit': BlackIPRangeForm
})

page_dc.update({
    # 'black_users': BlackUserListPage,
    # 'maindb.TbBlackuserlistLog': BlackUserListLogPage,
    'blackip_range': BlackIPRangeListPage,
    'white_ips': WhiteIpListPage,
    'white_users': WhiteUserListPage,
})
