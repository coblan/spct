# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc,RowSort
from ..models import TbMatches,TbTickets,TbTicketstake
from django.db.models.aggregates import Count
from helpers.director.base_data import director

class TicketSingleByMatchPage(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self):
        return '赛事投注状况'
    
    class tableCls(ModelTable):
        model = TbMatches
        exclude=[]
        fields_sort=['tournamentzh','tournamentid','matchdate','matchscore','teams']
        def permited_fields(self):
            names = ModelTable.permited_fields(self)
            names.extend(['nums_stake','nums_account'])
            return names
        
        def get_heads(self):
            heads = ModelTable.get_heads(self)
            heads.extend([
                {'name':'nums_stake','label':_('Ticket Count')},
                {'name':'nums_account','label':_('Num Account')},
                {'name':'teams','label':'队伍'}
            ])
            return heads
        
        def inn_filter(self, query):
            return query.annotate(nums_stake = Count('tbticketstake'))\
                   .annotate(nums_account = Count('tbticketstake__ticketid__accountid'))
        
        def dict_row(self, inst):
            return {
                'nums_stake':inst.nums_stake,
                'nums_account':inst.nums_account,
                'team':inst.team1zh +' vs '+ inst.team2zh
            }
        
        class sort(RowSort):
            names=['nums_stake','nums_account']

director.update({
    'match.viewbymatch':TicketSingleByMatchPage.tableCls
})

page_dc.update({
    'maindb.TicketSingleByMatch':TicketSingleByMatchPage
})