# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import gettext as _
from helpers.director.shortcut import TablePage, ModelTable, model_dc, page_dc, ModelFields, FieldsPage, \
    TabPage, RowSearch, RowSort, RowFilter, model_to_name, director
from ..models import TbTicketmaster, TbTicketstake, TbTicketparlay, TbMatches
from ..status_code import *
from django.db.models import Q, fields, Sum
import re


class TicketMasterPage(TablePage):
    template = 'jb_admin/table.html'  # 'maindb/table_ajax_tab.html'

    def get_label(self):
        return _('Tb Trans')  # '注单列表'

    def get_context(self):
        ctx = TablePage.get_context(self)
        ls = [
            {'name': 'ticketstake',
             'label': '子注单',
             'com': 'com_tab_table',

             'get_data': {
                 'fun': 'get_rows',
                 'kws': {
                     'director_name': TicketstakeTable.get_director_name(),  # model_to_name(TbTicketstake),
                     'relat_field': 'ticketid',
                 }

             },
             'table_ctx': TicketstakeTable(crt_user=self.crt_user).get_head_context()
             },
            # 'model':model_to_name(TbTicketstake),
            # 'relat_field':'ticketid',
            # 'kw': TicketstakeTable(crt_user=self.crt_user).get_head_context()},
            {'name': 'ticketparlay',
             'label': '串关规则',
             'com': 'com_tab_table',
             'get_data': {
                 'fun': 'get_rows',
                 'kws': {
                     'director_name': TicketparlayTable.get_director_name(),  # model_to_name(TbTicketparlay),
                     'relat_field': 'ticketid',
                 }

             },
             'table_ctx': TicketparlayTable(crt_user=self.crt_user).get_head_context()
             }

            # 'model':model_to_name(TbTicketparlay),
            # 'relat_field':'ticketid',
            # 'kw':TicketparlayTable(crt_user=self.crt_user).get_head_context()},
        ]
        ctx['tabs'] = ls
        return ctx

    class tableCls(ModelTable):
        model = TbTicketmaster
        exclude = []
        fields_sort = ['ticketid', 'account', 'stakeamount', 'betamount', 'parlayrule', 'status',
                       'winbet', 'createtime', 'betoutcome', 'turnover', 'bonuspa', 'bonus',
                       'settletime']

        def dict_head(self, head):
            if head['name'] in ['account', 'createtime', 'settletime']:
                head['width'] = 150
            elif head['name'] in ['betamount', 'betoutcome', 'turnover', 'bonus']:
                head['width'] = 100
            else:
                head['width'] = 80

            if head['name'] == 'ticketid':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'ticketstake'

            return head

        def statistics(self, query):
            dc = query.aggregate(total_betamount=Sum('betamount'), total_betoutcome=Sum('betoutcome'),
                                 total_turnover=Sum('turnover'), total_bonus=Sum('bonus'))
            mapper = {
                'betamount': 'total_betamount',
                'betoutcome': 'total_betoutcome',
                'turnover': 'total_turnover',
                'bonus': 'total_bonus'
            }
            for k in dc:
                dc[k] = str(round(dc[k], 2))
            footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            self.footer = footer
            self.footer = ['合计'] + self.footer
            return query

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            return ctx

        # def dict_row(self, inst):
        # account_type = dict(ACCOUNT_TYPE)
        # return {
        # 'amount':unicode(inst.amount),
        # 'accounttype': account_type.get(inst.accounttype)
        # }
        class search(RowSearch):
            names = ['ticketid', 'account']

            def get_context(self):
                ls = []
                for name in self.valid_name:
                    ls.append(_(self.model._meta.get_field(name).verbose_name))
                dc = {
                    'search_tip': ','.join(ls) + ',matchid' + '(精确值)',
                    'editor': 'com-search-filter',
                    'name': '_q'
                }
                return dc

            def get_query(self, query):
                if self.q:
                    exp = Q(account=self.q)
                    if re.search('^\d+$', self.q):
                        exp = exp | Q(ticketid=self.q) | Q(tbticketstake__match_id=self.q)
                    # return query.filter(Q(ticketid__icontains = self.q) | Q(account__icontains = self.q) | \
                    # Q(tbticketstake__match_id = self.q)).distinct()
                    return query.filter(exp).distinct()

                else:
                    return query

        class filters(RowFilter):
            range_fields = ['createtime']
            names = ['status', 'winbet']
            # range_fields=[{'name':'createtime','type':'date'},
            # {'name':'settletime','type':'date'}]

        class sort(RowSort):
            names = ['stakeamount', 'betamount', 'createtime', 'betoutcome', 'turnover', 'bonuspa', 'bonus',
                     'settletime']


class TicketTabBase(ModelTable):
    def __init__(self, *args, **kws):
        ModelTable.__init__(self, *args, **kws)
        self.ticketid = self.kw.get('ticketid')

    def inn_filter(self, query):
        if self.ticketid:
            return query.filter(ticket_master_id=self.ticketid)
        else:
            return query


class TicketstakeTable(TicketTabBase):
    """ 子注单 """
    model = TbTicketstake
    exclude = []
    fields_sort = ['tournament', 'matchid', 'match', 'specialbetvalue', 'odds', 'confirmodds', 'realodds',
                   'status', 'createtime', 'updatetime']

    def getExtraHead(self):
        return [
            {'name': 'matchid', 'label': 'matchid', },
            {'name': 'tournament', 'label': 'tournament', 'width': 120, }
        ]

    def dict_row(self, inst):
        match = inst.match  # TbMatches.objects.get(matchid =  inst.matchid)
        return {
            'matchid': match.matchid,
            'tournament': match.tournamentzh,
            'match': '{team1zh} VS {team2zh}'.format(team1zh=match.team1zh, team2zh=match.team2zh)
        }
        # return {
        # 'matchid':{'label':'{tournamentzh} {team1zh}VS{team2zh}'.format(tournamentzh=match.tournamentzh,
        # team1zh=match.team1zh,
        # team2zh=match.team2zh),
        # 'pk':match.pk

        # }
        # }

    def dict_head(self, head):
        dc = {
            'tid': 80,
            'match': 250,
            'specialbetvalue': 80,
            'odds': 80,
            'confirmodds': 80,
            'realodds': 80,
            'confirmoddsid_ori': 80,
            'status': 80,
            'updatetime': 150,
            'createtime': 150
        }
        if dc.get(head['name']):
            head['width'] = dc.get(head['name'])

        if head['name'] == 'match':
            head['label'] = '比赛'
        if head['name'] == 'matchid':
            head['editor'] = 'com-table-pop-fields'
            head['fields_ctx'] = MatchForm(crt_user=self.crt_user).get_head_context()
            head['after_save'] = {
                'fun': 'do_nothing'
                # 'fun':'update_or_insert'
            }
            # head['fields_heads']= MatchForm(crt_user=self.crt_user).get_heads()
            # head['model_name']=model_to_name(TbMatches)
            head['get_row'] = {
                "fun": 'get_with_relat_field',
                'director_name': 'games.ticketstake.matchform',
                'relat_field': 'matchid',
            }
            # head['ops']=[] #MatchForm(crt_user=self.crt_user).get_operations()
        return head


class TicketparlayTable(TicketTabBase):
    model = TbTicketparlay
    exclude = ['tid', 'ticketid']

    def dict_head(self, head):
        if head['name'] == 'createtime':
            head['width'] = 150
        else:
            head['width'] = 80

        return head

    def inn_filter(self, query):
        return query.filter(
            ticket_master_id=self.ticketid)  # .select_related('parlay1tid__match', 'parlay2tid__match', 'parlay3tid__match', 'parlay4tid__match', 'parlay5tid__match',  'parlay6tid__match')

    def dict_row(self, inst):
        dc = {}
        for i in range(1, 7):
            field_name = 'parlay%stid' % i
            if getattr(inst, field_name + '_id', 0) != 0:
                parlay = getattr(inst, field_name)
                dc[field_name] = '{team1zh}VS{team2zh}'.format(team1zh=parlay.match.team1zh,
                                                               team2zh=parlay.match.team2zh)
            else:
                dc[field_name] = ''
        return dc
        # return {
        # 'parlay1tid': '{team1zh}VS{team2zh}'.format(team1zh=inst.parlay1tid.match.team1zh, team2zh=inst.parlay1tid.match.team2zh) ,
        # 'parlay2tid': '{team1zh}VS{team2zh}'.format(team1zh=inst.parlay2tid.match.team1zh, team2zh=inst.parlay2tid.match.team2zh) ,
        # 'parlay3tid': '{team1zh}VS{team2zh}'.format(team1zh=inst.parlay3tid.match.team1zh, team2zh=inst.parlay3tid.match.team2zh) ,
        # 'parlay4tid': '{team1zh}VS{team2zh}'.format(team1zh=inst.parlay1tid.match.team1zh, team2zh=inst.parlay1tid.match.team2zh) ,
        # 'parlay1tid': '{team1zh}VS{team2zh}'.format(team1zh=inst.parlay1tid.match.team1zh, team2zh=inst.parlay1tid.match.team2zh) ,
        # 'parlay1tid': '{team1zh}VS{team2zh}'.format(team1zh=inst.parlay1tid.match.team1zh, team2zh=inst.parlay1tid.match.team2zh) ,
        # 'parlay1tid': '{team1zh}VS{team2zh}'.format(team1zh=inst.parlay1tid.match.team1zh, team2zh=inst.parlay1tid.match.team2zh) ,
        # }


class MatchForm(ModelFields):
    field_sort = ['matchdate', 'team1zh', 'team2zh', 'matchscore', 'winner', 'statuscode', 'roundinfo'
                                                                                           'livebet', 'generatedat',
                  'tournamentzh']
    readonly = field_sort

    class Meta:
        model = TbMatches
        exclude = []

    def get_operations(self):
        return []

    def dict_row(self, inst):
        winner = inst.winner
        if inst.winner == 1:
            winner = inst.team1zh
        elif inst.winner == 2:
            winner = inst.team2zh
        return {
            'winner': winner
        }


# model_dc[TbTicketstake] = {'table':TicketstakeTable}
# model_dc[TbTicketparlay] = {'table':TicketparlayTable}
# model_dc[TbMatches] = {'fields':MatchForm}
director.update({
    'games.ticketmaster': TicketMasterPage.tableCls,
    'games.TicketstakeTable': TicketstakeTable,
    'games.TicketparlayTable': TicketparlayTable,

    'games.ticketstake.matchform': MatchForm,

})

page_dc.update({
    'maindb.ticketmaster': TicketMasterPage,
})
