# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, \
    RowSearch, RowFilter, director,SelectSearch,has_permit

from ..models import TbLoginlog
import re
from django.db.models import Q
from hello.merchant_user import get_user_merchantid
from django.utils import timezone

class LoginLogPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return _('Tb Login Log')

    class tableCls(ModelTable):
        model = TbLoginlog
        exclude = []
        fields_sort = ['merchant','account_id', 'account__nickname', 'devicecode', 'deviceip', 'area', 'appversion',
                       'devicename',
                       'deviceversion',
                       'logintype', 'createtime']
        
        @classmethod
        def clean_search_args(cls, search_args):
            if '_seached' not in search_args:
                now = timezone.now()
                search_args['_start_createtime'] = now.strftime('%Y-%m-%d 00:00:00')
                search_args['_end_createtime'] = now.strftime('%Y-%m-%d 23:59:59')
                search_args['_seached'] = 1
            return search_args
        
        def dict_head(self, head):
            dc = {
                'account_id': 120,
                'devicecode': 120,
                'deviceip': 120,
                'appversion': 100,
                'devicename': 120,
                'deviceversion': 120,
                'area': 200,
                'createtime': 150,
                'account__nickname':150,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def getExtraHead(self):
            return [
                {'name': 'account__nickname', 'label': '用户昵称'},
                {'name': 'account_id', 'label': '用户ID'}
            ]

        def get_operation(self):
            return [
                    {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
                ]
        
        def inn_filter(self, query):
            if self.crt_user.merchant:
                query = query.filter(merchant_id = self.crt_user.merchant.id)
            #if self.is_export_excel:
            query =  query.using('Sports_nolock').select_related('account')
            #if self.crt_user.merchant:
                #query = query.filter(merchant_id = self.crt_user.merchant.id )
            return query
            #return query.values(*self.fields_sort).order_by('-createtime')
        
        def dict_row(self, inst):
            return {
                'account_id':inst.account.accountid,
                'account__nickname':inst.account.nickname
            }
        
        class search(SelectSearch):
            names = ['account__nickname','area','devicecode','deviceip']
            exact_names = ['account']

            def get_option(self, name):
                if name == 'account':
                    return {'value': name,
                            'label': '用户ID', }
                elif name == 'account__nickname':
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
                if self.crt_user.merchant:
                    return  []
                else:
                    return ['merchant']


director.update({
    'account.loginpage': LoginLogPage.tableCls,
})

page_dc.update({
    'loginlog': LoginLogPage
})
