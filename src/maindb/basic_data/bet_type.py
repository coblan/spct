from helpers.director.shortcut import TablePage, ModelTable, ModelFields, page_dc, director
from ..models import TbOddstypegroup
from ..rabbitmq_instance import updateSpread
import json
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from urllib.parse import urljoin
from django.conf import settings
import requests

class BetTypePage(TablePage):
    template = 'jb_admin/table.html'
    extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]

    def get_label(self):
        return '玩法设置'

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            'extra_table_logic': 'oddstypegroup_logic',
        })
        return ctx

    class tableCls(ModelTable):
        model = TbOddstypegroup
        exclude = []
        fields_sort = ['bettype', 'oddstypenamezh', 'periodtype', 'spread', 'enabled']
        pop_edit_field = 'oddstypenamezh'

        # def inn_filter(self, query):
        # return query.filter(enabled = 1)

        def get_operation(self):
            return [
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '启用',
                    'field': 'enabled',
                    'value': 1,
                    'row_match': 'many_row',
                    # 'match_field': 'enabled', 'match_values': [0], 'match_msg': '只能选择禁用的玩法！',
                    'confirm_msg': '确认启用该玩法吗?'
                },
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '禁用',
                    'field': 'enabled',
                    'value': 0,
                    'row_match': 'many_row',
                    'confirm_msg': '确认禁用该玩法吗?'
                }
            ]

        def dict_head(self, head):
            dc = {
                'oddstypenamezh': 200,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            elif head['name'] == 'enabled':
                head['editor'] = 'com-table-bool-shower'
            return head


class BetTypeForm(ModelFields):
    class Meta:
        model = TbOddstypegroup
        exclude = []

    readonly = ['bettype', 'oddstypenamezh', 'periodtype']
    field_sort = ['bettype', 'oddstypenamezh', 'periodtype', 'spread']

    def dict_head(self, head):
        if head['name'] == 'spread':
            head['fv_rule'] = 'range(0~1);two_valid_digit'
            head['step'] = 0.01
        return head

    def save_form(self):
        rt = super().save_form()

        ls = [
            {'betType': self.instance.bettype,
             'periodType': self.instance.periodtype,
             'spread': float(self.instance.spread)
             }
        ]
        url = urljoin(settings.SPREAD_SERVICE, 'spread/set')
        rq_rt = requests.post(url, json = ls)
        self.save_log({'model': 'TbOddstypegroup', 'service_return': rq_rt.text,})
        #updateSpread(json.dumps(ls))

        return rt


director.update({
    'maindb.TbOddstypeGroupPage': BetTypePage.tableCls,
    'maindb.TbOddstypeGroupPage.edit': BetTypeForm,
})

page_dc.update({
    'bet_type': BetTypePage,
})
