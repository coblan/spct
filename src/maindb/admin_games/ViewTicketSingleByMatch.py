# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc
from ..models import TbMatches,TbTickets

class TicketSingleByMatchPage(TablePage):
    template = 'maindb/table_plain.html'
    class tableCls(ModelTable):
        model = TbMatches
        exclude=[]
        def get_heads(self):
            heads = ModelTable.get_heads(self)
            heads.extend([
                {'name':'ticket_count','label':_('Ticket Count')}
            ])
            return heads
        
        def dict_row(self, inst):
            ls = list(TbTickets.objects.filter(matchid=inst.tid) )
            return {
                'ticket_count':len(ls)
            }

page_dc.update({
    'maindb.TicketSingleByMatch':TicketSingleByMatchPage
})