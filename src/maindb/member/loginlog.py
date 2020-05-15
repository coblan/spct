# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, \
    RowSearch, RowFilter, director,SelectSearch,has_permit

from ..models import TbLoginlog
import re
from django.db.models import Q
from hello.merchant_user import get_user_merchantid

class LoginLogPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return _('Tb Login Log')

    class tableCls(ModelTable):
        model = TbLoginlog
        exclude = []
        fields_sort = ['merchant','accountid_id', 'accountid__nickname', 'devicecode', 'deviceip', 'area', 'appversion',
                       'devicename',
                       'deviceversion',
                       'logintype', 'createtime']

        def dict_head(self, head):
            dc = {
                'accountid_id': 120,
                'devicecode': 120,
                'deviceip': 120,
                'appversion': 100,
                'devicename': 120,
                'deviceversion': 120,
                'area': 200,
                'createtime': 150,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def getExtraHead(self):
            return [
                {'name': 'accountid__nickname', 'label': '用户昵称'},
                {'name': 'accountid_id', 'label': '用户ID'}
            ]

        def get_operation(self):
            return [
                    {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
                ]
        
        def inn_filter(self, query):
            if self.is_export_excel:
                query =  query.using('Sports_nolock')
            if has_permit(self.crt_user,'-i_am_merchant'):
                query = query.filter(merchant_id = get_user_merchantid(self.crt_user) )
            return query
            #return query.values(*self.fields_sort).order_by('-createtime')
            
        class search(SelectSearch):
            names = ['accountid__nickname','area','devicecode','deviceip']
            exact_names = ['accountid']

            def get_option(self, name):
                if name == 'accountid':
                    return {'value': name,
                            'label': '用户ID', }
                elif name == 'accountid__nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }
                elif name == 'area':
                    return {
                        'value': name,
                        'label': '地区',
                    }
                elif name =='devicecode':
                    return {
                        'value':name,
                        'label':'设备码'
                    }
                elif name =='deviceip':
                    return {
                        'value':name,
                        'label':'设备ip'
                    }
                

            def clean_search(self):
                if self.qf in ['accountid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()

        class filters(RowFilter):
            range_fields = ['createtime']
            
            @property
            def names(self):
                if has_permit(self.crt_user, '-i_am_merchant'):
                    return  []
                else:
                    return ['merchant']


director.update({
    'account.loginpage': LoginLogPage.tableCls,
})

page_dc.update({
    'loginlog': LoginLogPage
})
