# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable, TablePage, page_dc, RowSort, RowFilter, RowSearch
from ..models import TbMatches
from django.db.models.aggregates import Count, Sum
from django.db.models import F
from helpers.director.base_data import director


class MatchesSummaryPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '赛事投注状况'

    class tableCls(ModelTable):
        model = TbMatches
        exclude = []
        fields_sort = ['tournamentzh', 'matchid', 'matchdate', 'matchscore', 'team_zh', 'statuscode', 'nums_stake',
                       'nums_account', 'sum_betamount', 'sum_betoutcome', 'sum_grossprofit', 'sum_bonus', 'sum_profit']

        def permited_fields(self):
            names = ModelTable.permited_fields(self)
            names.extend(
                ['nums_stake', 'nums_account', 'sum_betamount', 'sum_betoutcome', 'sum_grossprofit', 'sum_bonus',
                 'sum_profit'])
            return names

        def getExtraHead(self):
            ls = [
                {'name': 'team_zh', 'label': _('Team Zh')},
                {'name': 'nums_stake', 'label': _('Ticket Count')},
                {'name': 'nums_account', 'label': _('Num Account')},
                {'name': 'sum_betamount', 'label': '投注金额'},
                {'name': 'sum_betoutcome', 'label': '派彩金额'},
                {'name': 'sum_grossprofit', 'label': '毛利'},
                {'name': 'sum_bonus', 'label': '返水'},
                {'name': 'sum_profit', 'label': '亏盈'},
            ]
            return ls

        def statistics(self, query):
            # query = ModelTable.get_query(self)
            dc = query.aggregate(total_stake=Sum('nums_stake'), total_account=Sum('nums_account'),
                                 total_betamount=Sum('sum_betamount'), total_betoutcome=Sum('sum_betoutcome'),
                                 total_grossprofit=Sum('sum_grossprofit'), total_bonus=Sum('sum_bonus'),
                                 total_profit=Sum('sum_profit'))
            mapper = {
                'nums_stake': 'total_stake',
                'nums_account': 'total_account',
                'sum_betamount': 'total_betamount',
                'sum_betoutcome': 'total_betoutcome',
                'sum_grossprofit': 'total_grossprofit',
                'sum_bonus': 'total_bonus',
                'sum_profit': 'total_profit'
            }
            for k in dc:
                dc[k] = str(dc[k])
            footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            self.footer = footer
            self.footer = [_('Total')] + self.footer
            return query

        def dict_head(self, head):
            dc = {
                'tournamentzh': 160,
                'matchid': 80,
                'matchdate': 120,
                'matchscore': 60,
                'team_zh': 160,
                'statuscode': 60,
                'nums_stake': 120,
                'matchdate': 150,
                'statuscode': 80,
                'nums_account': 120,
                'sum_betamount': 120,
                'sum_betoutcome': 120,
                'sum_grossprofit': 120,
                'sum_bonus': 120,
                'sum_profit': 120,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def get_context(self):
            # footer = ['']
            # footer.extend(self.statistics)
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            return ctx

        def inn_filter(self, query):  # __accountid_id
            return query.annotate(nums_stake=Count('tbticketstake')) \
                .annotate(nums_account=Count('tbticketstake__ticket_master__accountid', distinct=True)) \
                .annotate(sum_betamount=Sum('tbticketstake__ticket_master__betamount')) \
                .annotate(sum_betoutcome=Sum('tbticketstake__ticket_master__betoutcome')) \
                .annotate(sum_grossprofit=F('sum_betoutcome') - F('sum_betamount')) \
                .annotate(sum_bonus=Sum('tbticketstake__ticket_master__bonus')) \
                .annotate(sum_profit=F('sum_grossprofit') + F('sum_bonus'))

        def dict_row(self, inst):
            team_zh = ''
            if inst.team1zh and inst.team2zh:
                team_zh = '%s VS %s' % (inst.team1zh, inst.team2zh)
            return {
                'team_zh': team_zh,
                'nums_stake': inst.nums_stake,
                'nums_account': inst.nums_account,
                'sum_betamount': str(inst.sum_betamount) if inst.sum_betamount else '',
                'sum_betoutcome': str(inst.sum_betoutcome) if inst.sum_betoutcome else '',
                'sum_grossprofit': str(inst.sum_grossprofit) if inst.sum_grossprofit else '',
                'sum_bonus': str(inst.sum_bonus) if inst.sum_bonus else '',
                'sum_profit': str(inst.sum_profit) if inst.sum_profit else '',
                # 'team':inst.team1zh +' vs '+ inst.team2zh
            }

        class sort(RowSort):
            names = ['nums_stake', 'nums_account', 'sum_betamount', 'sum_betoutcome', 'sum_grossprofit', 'sum_bonus','sum_profit',]

        class search(RowSearch):
            names = ['matchid']

        class filters(RowFilter):
            names = ['statuscode']
            range_fields = ['matchdate']


director.update({
    'match.viewbymatch': MatchesSummaryPage.tableCls
})

page_dc.update({
    'maindb.MatchesSummary': MatchesSummaryPage
})
