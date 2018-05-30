# encoding:utf-8

from helpers.director.shortcut import TablePage, ModelTable, page_dc, director
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from ..models import TbMatches
from django.db.models.aggregates import Count,Sum
from django.db.models import Q, F, Case, When, Sum, DecimalField

class OddsPage(object):
    template = 'maindb/tabs.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    
    def __init__(self, request): 
        self.request = request
        self.crt_user = request.user
    
    def get_label(self): 
        return 'odds'
    
    def get_context(self):
        #ctx = TablePage.get_context(self)
        ctx = {
            'crt_tab': 'balance_log',
            'extra_js': self.extra_js,
        }
  
        base_table = OddsTable(crt_user= self.crt_user)
        ls = [
            {'name':'balance_log',
             'label':'Balance Log',
             'com':'com_odds_editor',
             'director_name': base_table.get_director_name(),
             #'rows': base_table.get_rows(),
             'get_data':{
                 'fun': 'do_not',
                 #'fun':'get_rows',
                 #'kws':{
                    #'director_name':AccountBalanceTable.get_director_name() ,# model_to_name(TbBalancelog),
                    #'relat_field':'accountid',
                 #}
                 
             },
             'table_ctx':base_table.get_context()  #AccountBalanceTable(crt_user=self.crt_user).get_head_context(), 
           },  
            {'name':'ss',
             'label':'ss Log',
             'com':'com_odds_editor',
             'get_data':{
                 'fun': 'do_not',
                 #'fun':'get_rows',
                 #'kws':{
                    #'director_name':AccountBalanceTable.get_director_name() ,# model_to_name(TbBalancelog),
                    #'relat_field':'accountid',
                 #}
                 
             },
             'table_ctx':{}  #AccountBalanceTable(crt_user=self.crt_user).get_head_context(), 
           },              
        ]
        ctx['tabs']=  ls 
        return ctx


class OddsTable(ModelTable):
    model = TbMatches
    exclude = []
    fields_sort = ['matchdate', 'event', 'turnover']
    
    def getExtraHead(self): 
        return [{'name': 'event','label': 'Event', 'editor': 'com-table-html-shower',}, 
                {'name': 'turnover','label': 'Turnover','editor': 'com-odds-turnover',}]
    
    def statistics(self, query): 
        """
        --查询流水
select 
	MatchID,
	sum(case oddsid when 151001 then Amount else 0 end) as FavTurnover,
	sum(case oddsid when 151003 then Amount else 0 end) as UnderTurnover
 from dbo.TB_MatchesTurnover with(nolock)
where matchid in( 13497287,14473288)
group by MatchID


--查询盘口
select MatchID,SpecialBetValue,
	sum(case oddsid when 151001 then odds else 0 end) as FavOdds,
	sum(case oddsid when 151003 then odds else 0 end) as UnderOdds
  from dbo.tb_odds with(nolock) 
where matchid in( 13497287,14473288)
and status =1 and oddsid in(151001,151003)
group by MatchID,SpecialBetValue
order by matchid

        """
        #ss = query.annotate(FavTurnover = Sum('tbmatchesturnover__amount', filter = Q(tbmatchesturnover__oddsid = 151001) ), 
                            #UnderTurnover = Sum( 'tbmatchesturnover__amount', filter = Q(tbmatchesturnover__oddsid = 151003) ))
        ss = query.annotate(FavTurnover = Sum(Case(When(tbmatchesturnover__oddsid = 151001 , then= F('tbmatchesturnover__amount')), default=0, output_field=DecimalField()) ), 
                            UnderTurnover = Sum( Case(When(tbmatchesturnover__oddsid = 151003 , then= F('tbmatchesturnover__amount')), default=0, output_field=DecimalField() ) ) ) 
        
        return ss
    
    def dict_row(self, inst): 
        return {
            'event': '%s<br>%s' % (inst.team1zh, inst.team2zh),
            'FavTurnover': str(inst.FavTurnover),
            'UnderTurnover': str(inst.UnderTurnover),
        }


director.update({
     'maindb.TbOdds': OddsTable,
})

page_dc.update({
    'maindb.TbOdds': OddsPage,
})