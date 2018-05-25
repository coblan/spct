# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from helpers.director.shortcut import ModelTable,TablePage,page_dc,RowSort,RowFilter
from ..models import TbMatches,TbTickets,TbTicketstake
from django.db.models.aggregates import Count,Sum
from django.db.models import F
from helpers.director.base_data import director

class TicketSingleByMatchPage(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self):
        return '赛事投注状况'
    
    class tableCls(ModelTable):
        model = TbMatches
        exclude=[]
        fields_sort=['tournamentzh','matchid','matchdate','matchscore','team_zh','statuscode','nums_stake',
                     'nums_account','sum_betamount','sum_betoutcome','sum_profit']
        def permited_fields(self):
            names = ModelTable.permited_fields(self)
            names.extend(['nums_stake','nums_account','sum_betamount','sum_betoutcome','sum_profit'])
            return names
        
        def getExtraHead(self):
            ls = [
                {'name':'team_zh','label':_('Team Zh')},
                {'name':'nums_stake','label':_('Ticket Count')},
                {'name':'nums_account','label':_('Num Account')},
                {'name':'sum_betamount','label':_('Total bet amount')},
                {'name':'sum_betoutcome','label':_('Total Bet Outcome')},
                {'name':'sum_profit','label':_('Total Profit')},
            ]
            return ls
  
        def statistics(self,query):
            #query = ModelTable.get_query(self)
            dc = query.aggregate(total_stake=Sum('nums_stake'),total_account=Sum('nums_account'),
                                 total_betamount=Sum('sum_betamount'),total_betoutcome=Sum('sum_betoutcome'),
                                 total_profit=Sum('sum_profit'))
            mapper = {
                'nums_stake':'total_stake',
                'nums_account':'total_account',
                'sum_betamount':'total_betamount',
                'sum_betoutcome':'total_betoutcome',
                'sum_profit':'total_profit',
            }
            out_dc={}
            for k in dc:
                dc[k] = str(dc[k])
            footer = [dc.get( mapper.get( name) ,'') for name in self.fields_sort]
            self.footer = footer
            return query
        
        def dict_head(self, head):
            dc={
                'tournamentzh':160,
                'matchid':80,
                'matchdate':120,
                'matchscore':60,
                'team_zh':160,
                'statuscode':60,
                'nums_stake':120,
                
                'nums_account':120,
                'sum_betamount':120,
                'sum_betoutcome':120,
                'sum_profit':120,

                
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])     
            return head
        
        def get_context(self):
            #footer = ['']
            #footer.extend(self.statistics)
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            return ctx
        
        def inn_filter(self, query):
            return query.annotate(nums_stake = Count('tbticketstake'))\
                   .annotate(nums_account = Count('tbticketstake__ticket_master__accountid'))\
                   .annotate(sum_betamount = Sum('tbticketstake__ticket_master__betamount'))\
                   .annotate(sum_betoutcome = Sum('tbticketstake__ticket_master__betoutcome'))\
                   .annotate( sum_profit=F('sum_betamount') - F('sum_betoutcome'))                
        
        
        def dict_row(self, inst):
            team_zh=''
            if inst.team1zh and inst.team2zh:
                team_zh = '%s VS %s'%(inst.team1zh,inst.team2zh)
            return {
                'team_zh':team_zh,
                'nums_stake':inst.nums_stake,
                'nums_account':inst.nums_account,
                'sum_betamount':str( inst.sum_betamount ) if inst.sum_betamount else '',
                'sum_betoutcome':str( inst.sum_betoutcome ) if inst.sum_betoutcome else '',
                'sum_profit':str( inst.sum_profit ) if inst.sum_profit else ''
                #'team':inst.team1zh +' vs '+ inst.team2zh
            }
        
        class sort(RowSort):
            names=['nums_stake','nums_account','sum_betamount','sum_betoutcome','sum_profit']
        
        class filters(RowFilter):
            names=['tournamentzh','statuscode']
            range_fields=['matchdate']

director.update({
    'match.viewbymatch':TicketSingleByMatchPage.tableCls
})

page_dc.update({
    'maindb.TicketSingleByMatch':TicketSingleByMatchPage
})