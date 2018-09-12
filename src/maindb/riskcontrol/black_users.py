# encoding:utf-8
from __future__ import unicode_literals

from numpy import long

from helpers.director.shortcut import ModelTable, TablePage, page_dc, ModelFields, RowSearch, director
from ..models import Blackiprangelist, \
    Whiteiplist, Whiteuserlist, TbAccount


# class BlackUserListPage(TablePage):
#     template = 'jb_admin/table.html'
#
#     def get_label(self):
#         return _('Main.TbBlackuserlist')
#
#     class tableCls(ModelTable):
#         model = TbBlackuserlist
#         exclude = []
#
#         def dict_head(self, head):
#             dc = {
#                 'blackuserlistid': 120,
#                 'accounttype': 100
#             }
#             if dc.get(head['name']):
#                 head['width'] = dc.get(head['name'])
#             return head
#
#
# class BlackUserForm(ModelFields):
#     class Meta:
#         model = TbBlackuserlist
#         exclude = ['accountid', 'accounttype', 'username', 'accounttpe' ,'addtime']
#
#     def dict_head(self, head):
#         if head['name'] == 'account':
#             table_obj = AccountSelect(crt_user=self.crt_user)
#             head['editor'] = 'com-field-pop-table-select'
#             head['table_ctx'] = table_obj.get_head_context()
#         return head


# class BlackUserListLogPage(TablePage):
#     template = 'jb_admin/table.html'
#
#     def get_label(self):
#         return _('Main.TbBlackuserlistLog')
#
#     class tableCls(ModelTable):
#         model = TbBlackuserlistLog
#         exclude = []
#
#         def dict_head(self, head):
#             dc = {
#                 'blacklogid': 100,
#                 'before_ban_status': 130,
#                 'alter_ban_status': 120,
#                 'modify_user': 120,
#
#             }
#             if dc.get(head['name']):
#                 head['width'] = dc.get(head['name'])
#             return head
#
#         # class BlankiplistPage(TablePage):
#     # template='jb_admin/table.html'
#     # class tableCls(ModelTable):
#     # model=Blackiplist
#     # exclude=[]


class BlackIPRangeListPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return 'IP黑名单(范围)'

    class tableCls(ModelTable):
        model = Blackiprangelist
        exclude = []
        hide_fields = ['startipnum', 'endipnum']
        pop_edit_field = 'blackiprangelistid'

        def dict_head(self, head):
            dc = {
                'startip': 100,
                'endip': 100,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head


class BlackIPRangeForm(ModelFields):
    # hide_fields = ['startipnum', '']
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
    model = TbAccount
    include = ['accountid', 'nickname']

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

    class search(RowSearch):
        names = ['accountid', 'nickname']


def ip2num(ip):
    arr = ip.split('.')
    num = 256 * 256 * 256 * long(arr[0]) + 256 * 256 * long(arr[1]) + 256 * long(arr[2]) + long(arr[3])
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
