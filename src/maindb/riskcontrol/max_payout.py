from django.db.models import Q

from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowSearch, ModelFields, RowFilter, \
    field_map, \
    model_to_name
from helpers.director.table.row_search import SelectSearch
from ..models import TbMaxpayout, TbMatches, TbOddstypegroup, TbMaxpayouttype, TbTournament
from ..riskcontrol.blanklist import AccountSelect
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc
from django import forms


class MaxPayoutPage(TablePage):
    template = 'jb_admin/table.html'
    extra_js = ['/static/js/maindb.pack.js?t=%s' % js_stamp_dc.get('maindb_pack_js', '')]

    def get_label(self):
        return '最大赔付'

    class tableCls(ModelTable):
        model = TbMaxpayout
        exclude = ['updatetime']
        pop_edit_field = 'tid'

        def __init__(self, *args, **kw):
            super().__init__(*args, **kw)
            self.oddstype_options = [{'value': x.oddstypegroup, 'label': x.oddstypenamezh, } for x in
                                     TbOddstypegroup.objects.filter(enabled=1)]
            self.user_options = [
                {'value': 1, 'label': '等级一', },
                {'value': 2, 'label': '等级二', },
                {'value': 3, 'label': '等级三', },
                {'value': 4, 'label': '等级四', },
                {'value': 5, 'label': '等级五', },
            ]

        def get_operation(self):
            create = super().get_operation()[0]
            return [create,
                    {
                        'fun': 'selected_set_and_save',
                        'editor': 'com-op-btn',
                        'label': '作废',
                        'field': 'status',
                        'value': False,
                        'row_match': 'one_row',
                        'confirm_msg': '确认作废该限制类型吗?'
                    }
                    ]

        def dict_head(self, head):
            dc = {
                'limittype': 200,
                'tournamentid': 150,
                'matchid': 150,
                'accountid': 120,
                'oddstypegroup': 120,
                'maxpayout': 120,
                'description': 150,
                'createtime': 140
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])

            if head['name'] == 'relationno':
                head['editor'] = 'com-table-label-shower'
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-label-shower'

            return head

        class search(SelectSearch):
            names = ['tournament', 'team1zh', 'bettype', 'nickname']

            # exact_names = ['matchid']

            def get_option(self, name):
                if name == 'tournament':
                    return {'value': 'tournament', 'label': '联赛', }
                elif name == 'team1zh':
                    return {'value': 'team1zh', 'label': '比赛', }
                elif name == 'bettype':
                    return {'value': 'bettype', 'label': '玩法', }
                elif name == 'nickname':
                    return {'value': 'nickname', 'label': '昵称', }
                else:
                    return super().get_option(name)

            def get_express(self, q_str):
                if self.qf == 'tournament':
                    return Q(tournamentid__tournamentname__icontains=q_str)
                elif self.qf == 'team1zh':
                    return Q(matchid__team1zh__icontains=q_str) | Q(matchid__team2zh__icontains=q_str)
                elif self.qf == 'bettype':
                    return Q(oddstypegroup__oddstypenamezh__icontains=q_str)
                elif self.qf == 'nickname':
                    return Q(accountid__nickname__icontains=q_str)
                else:
                    return super().get_express(q_str)

        class filters(RowFilter):
            names = ['status', 'viplv']


class MaxPayoutForm(ModelFields):
    class Meta:
        model = TbMaxpayout
        exclude = ['createtime', 'updatetime']

    extra_mixins = ['maxpayout_form_logic']

    def __init__(self, *args, **kw):

        # self.oddstype_options = [{'value': x.oddstypegroup, 'label': x.oddstypenamezh,} for x in TbOddstypegroup.objects.filter(enabled = 1)]
        self.user_options = [
            {'value': 1, 'label': '等级一', },
            {'value': 2, 'label': '等级二', },
            {'value': 3, 'label': '等级三', },
            {'value': 4, 'label': '等级四', },
            {'value': 5, 'label': '等级五', },
        ]
        self.var_fields = ['accountid', 'matchid', 'tournamentid', 'oddstypegroup', 'viplv']
        mapper = (
            ('User', 'accountid'),
            ('Match', 'matchid'),
            ('League', 'tournamentid'),
            ('BetType', 'oddstypegroup'),
            ('Vip', 'viplv'),
        )
        keywords = {}
        for x in TbMaxpayouttype.objects.filter(isenable=True):
            bb = x.enum.strip()
            for item in mapper:
                bb = bb.replace(item[0], item[1])
            keywords[x.pk] = bb.split('_')
        self.keywords = keywords
        super().__init__(*args, **kw)

    # def clean_dict(self, dc):
    # dc['matchid'] = dc.get('matchid', 0)
    # dc['tournamentid'] = dc.get('tournamentid', 0)
    # dc['accountid'] = dc.get('accountid', 0)
    # dc['oddstypegroup'] = dc.get('oddstypegroup', 0)
    # dc['viplv'] = dc.get('viplv', 0)
    # dc = super().clean_dict(dc)

    # return dc

    def dict_head(self, head):
        if head['name'] == 'tournamentid':
            table_obj = LeagueSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
            head['options'] = []

        if head['name'] == 'matchid':
            table_obj = MatchSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
            head['options'] = []
        if head['name'] == 'accountid':
            table_obj = AccountSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
            head['options'] = []
        if head['name'] == 'limittype':
            head['var_fields'] = self.var_fields
            head['keywords'] = self.keywords
            # head['order'] = True
            head['placeholder'] = '请选择'
            head['options'] = [{'value': x.pk, 'label': str(x)} for x in
                               TbMaxpayouttype.objects.filter(isenable=True).order_by('level')]
        if head['name'] in( 'oddstypegroup','viplv'):
            head['placeholder'] = '请选择'

        if head['name'] == 'status':
            head['check_label'] = '启用'

        return head

    def dict_row(self, inst):
        # if inst.limittype in [11, 21]:
        # relationno_label = ''
        # elif inst.limittype in [12, 22]:
        # relationno_label = 'ERROR'
        # for i in  self.oddstype_options:
        # if i['value'] == inst.relationno:
        # relationno_label = i['label']
        # break
        # elif inst.limittype in [13 ]:
        # relationno_label = 'ERROR'
        # for i in  self.user_options:
        # if i['value'] == inst.relationno:
        # relationno_label = i['label']
        # break

        return {
            # '_relationno_label': relationno_label,
            # 'relationno': inst.relationno or 1,
            'createtime': inst.createtime.strftime('%Y-%m-%d %H:%M:%S') if inst.createtime else '',
            'updatetime': inst.updatetime.strftime('%Y-%m-%d %H:%M:%S') if inst.updatetime else '',
        }

    def clean_accountid(self):
        data = self.cleaned_data['accountid']
        limittype = self.cleaned_data['limittype']
        if limittype in [21, 22] and not data:
            raise forms.ValidationError('必须填写一个用户')
        return data

    def clean_maxsinglepayout(self):
        data = self.cleaned_data['maxsinglepayout']
        if float(data) <= 0:
            raise forms.ValidationError('必须大于0')
        return data

    def save_form(self):
        keywords = self.keywords.get(self.instance.limittype_id)
        for vf in self.var_fields:
            if vf not in keywords:
                setattr(self.instance, vf, None)
        super().save_form()


class LeagueSelect(ModelTable):
    model = TbTournament
    exclude = ['typegroupswitch', 'categoryid', 'uniquetournamentid', 'createtime']
    fields_sort = ['tournamentid', 'tournamentname', 'issubscribe', 'openlivebet']

    def dict_head(self, head):
        dc = {
            'tournamentid': 120,
            'categoryid': 100,
            'tournamentname': 250,
            'createtime': 120
        }
        if head['name'] in dc:
            head['width'] = dc.get(head['name'])
        if head['name'] == 'tournamentname':
            head['editor'] = 'com-table-foreign-click-select'
        if head['name'] in ('openlivebet'):
            head['editor'] = 'com-table-bool-shower'
        return head

    def getExtraHead(self):
        return [{'name': 'openlivebet', 'label': '开启走地'}]

    def dict_row(self, inst):
        return {
            'openlivebet': not bool(inst.closelivebet)
        }

    class search(RowSearch):
        names = ['tournamentname', 'tournamentid']


class MatchSelect(ModelTable):
    model = TbMatches
    include = ['matchid', 'tournamentzh', 'team1zh', 'team2zh', 'matchdate']

    def dict_head(self, head):
        dc = {
            'matchid': 100,
            'tournamentzh': 150,
            'team1zh': 150,
            'team2zh': 150,
            'matchdate': 150
        }
        if dc.get(head['name']):
            head['width'] = dc.get(head['name'])

        if head['name'] == 'matchid':
            head['editor'] = 'com-table-foreign-click-select'
        return head

    class search(RowSearch):
        names = ['matchid', 'team1zh', 'team2zh']

    class filters(RowFilter):
        range_fields = ['matchdate']


field_map.update({
    model_to_name(TbMaxpayout) + '.status': IntBoolProc,
})

director.update({
    'sports.maxpayout': MaxPayoutPage.tableCls,
    'sports.maxpayout.edit': MaxPayoutForm,
    'sports.matchselect': MatchSelect,
    'sports.leagureselect': LeagueSelect,
})

page_dc.update({
    'maxpayout': MaxPayoutPage,
})
