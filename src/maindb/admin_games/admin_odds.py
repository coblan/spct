# encoding:utf-8

from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, PageNum, RowSearch, RowFilter
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from ..models import TbMatches, TbOdds
from django.db.models.aggregates import Count,Sum
from django.db.models import Q, F, Case, When, Sum, DecimalField, Max
from django.db.models.expressions import Subquery, OuterRef
from django.db import connections
import math
import re

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
            'crt_tab': 'typegroup_4',
            'extra_js': self.extra_js,
        }

        base_table = OddsTypeGroup4Table(crt_user= self.crt_user)
        typegroup_2 =  OddsTypeGroup2Table(crt_user= self.crt_user)
        ls = [
            {'name':'typegroup_4',
             'label':'全场让分',
             'com':'com_odds_editor',
             'director_name': base_table.get_director_name(),
             'first_page': True,
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
            {'name':'typegroup_2',
             'label':'全场大小',
             'com':'com_odds_editor',
             'director_name': typegroup_2.get_director_name(),
             'get_data':{
                 'fun': 'do_not',
                 #'fun':'get_rows',
                 #'kws':{
                 #'director_name':AccountBalanceTable.get_director_name() ,# model_to_name(TbBalancelog),
                 #'relat_field':'accountid',
                    #}

                    },
             'table_ctx':typegroup_2.get_context()  #AccountBalanceTable(crt_user=self.crt_user).get_head_context(), 
             },              
        ]
        ctx['tabs']=  ls 
        return ctx


class CusPagenator(PageNum):
    def get_query(self,query):
        count = query.count()
        totalpage = int( math.ceil( float( count )/self.perPage) )
        self.totalpage = max(totalpage,1)

        self.query = query  
        crt_page=min(self.totalpage,abs(int( self.pageNumber)))
        start = (crt_page -1)*self.perPage
        end = min(crt_page*self.perPage,count)
        return query[start:end]

        #self.pagenator = Paginator(query,self.perPage)
        #self.pageNumber = min(self.pagenator.num_pages,abs(int( self.pageNumber)))
        #return  self.pagenator.page(self.pageNumber)
    def get_context(self): 

        return {
            'crt_page':self.pageNumber,
            'total':self.count,
            'perpage':self.perPage
            }

#"""
#['亚洲让分 4', '大小 -', '']
#"""      

class OddsTypeGroup4Table(ModelTable):
    model = TbMatches
    exclude = []
    fields_sort = ['matchid', 'matchdate', 'event', 'turnover', 'balance', 'favorite', 'betradar','sw', 'SpecialBetValue', 'FavOdds', 'UnderOdds', 
                   'plus', 'MaxPayout','status_odds', 'special_turnover']
    pagenator = CusPagenator
    
    class search(RowSearch):
        names = ['matchid'] 
        
        def get_where_str(self): 
            if not self.q:
                return ''
            
            ls = []
            for name in self.valid_name:
                ls.append('%s like %s' % (name, self.q))
                            
            return 'AND ' + ' AND '.join(ls) 
    
    class filters(RowFilter):
        range_fields = ['matchdate']
        
        def get_where_str(self): 
            if not self.filter_args:
                return ''
            ls = []
            for k, v in self.filter_args.items():
                mt = re.search('(\w+)__gte', k)
                if mt:
                    ls.append("%s>='%s'"% (mt.group(1), v) )
                    continue
                
                mt = re.search('(\w+)__lte', k)
                if mt:
                    ls.append("%s<='%s'" % (mt.group(1), v))
                    continue
                ls.append('%s EQ %s' % (k, v))
                    
            return 'AND ' + ' AND '.join(ls) 
    
    def getExtraHead(self): 
        return [{'name': 'event','label': 'Event', 'editor': 'com-table-html-shower',}, 
                {'name': 'turnover','label': 'Turnover','editor': 'com-odds-turnover','width': 120,}, 
                 {'name': 'SpecialBetValue','label': 'Line','editor': 'com-odds-multi-line',},
                 
                {'name': 'balance','label': 'Balance','editor': 'com-odds-balance'}, 
                {'name': 'favorite','label': 'Favorite','editor': 'com-odds-favorite'}, 
                
                {'name': 'betradar','label': 'Betradar','editor': 'com-table-bool-editor','width': 76,},
                
                {'name': 'sw','label': 'SW','editor': 'com-odds-switch-checkbox','width': 45,},
                {'name': 'SpecialBetValue','label': 'Line','editor': 'com-odds-multi-line',},
                 
                {'name': 'FavOdds','label': 'Fav.','editor': 'com-odds-multi-line-edit',}, 
               {'name': 'UnderOdds','label': 'Under.','editor': 'com-odds-multi-line-edit',}, 
                {'name': 'MaxPayout','label': 'MaxPayout','editor': 'com-odds-multi-line','width': 90,}, 
                
               {'name': 'plus','label': '+/-','editor': 'com-odds-plus','width': 100,},
               {'name': 'status_odds','label': 'Status','editor': 'com-odds-status',},
            {'name': 'special_turnover','label': 'Liability','editor': 'com-odds-special-turnover',},
               ]
    def dict_head(self, head): 
        if head['name'] == 'matchdate':
            head['editor'] = 'com-table-html-shower'
            head['width'] = 100
        return head
    

    def get_query(self): 
        sql = """
--查询比赛信息
declare @OddsTypeGroup int
declare @PageIndex int
declare @PageSize int
set @PageIndex='%(pageindex)s'
set @PageSize = '%(pagesize)s'
set @OddsTypeGroup='4'
declare @tb_matches table(
	MatchID bigint
)

select count(1) as TotalCount from dbo.TB_Matches with(nolock)
where 1=1 %(where_filter)s
"""
        pageindex = self.pagenum.pageNumber
        pagesize = self.pagenum.perPage
        
        search_str = self.row_search.get_where_str()
        filter_str = self.row_filter.get_where_str()
        
        
        ls = [x for x in [search_str, filter_str] if x]
        
        if ls:
            where_filter = 'AND'.join(ls)
        else:
            where_filter = ''
        #where_filter = 'and matchid in(14574778,14520592,14561132)'
        
        sql = sql % dict(pageindex = pageindex, pagesize = pagesize, where_filter = where_filter)

        cursor = connections['MainDB'].cursor()
        cursor.execute(sql)
        ls = []
        cout_query =  cursor.fetchall()
        dc = {
            'count': cout_query[0][0],
        }
        cursor.nextset()
        cursor.nextset()
        dc['matchs'] = list(cursor)
        cursor.nextset()
        dc['turnover'] = list(cursor)
        cursor.nextset()
        dc['odds'] = list(cursor)

        self.pagenum.count = dc['count']
        return dc

    def get_rows(self): 
        dc = self.get_query()
        matchs = dc.get('matchs')
        match_dc_list = []
        for match in matchs:
            match_dc = {
                'TournamentID': match[2],
                'TournamentZH': match[3],
                'matchid': match[4],
                'matchdate': match[6],
                'Team1ZH': match[7],
                'Team2ZH': match[9],
            }
            
            matchdate =  str( match_dc['matchdate'] )
            if matchdate:
                matchdate = matchdate[:10] + '<br>' + matchdate[11:16]
            match_dc['matchdate'] = matchdate
        
            match_dc['event'] = '%(Team1ZH)s<br>%(Team2ZH)s' % match_dc
            matchid = match_dc['matchid']
            turnover_tmp= [{'OddsID': x[2], 'Turnover': x[3]} for x in dc['turnover'] if x[0] == matchid]
            match_dc['FavTurnover'] = 0
            match_dc['UnderTurnover'] = 0
            
            for turnover in turnover_tmp:
                if turnover['OddsID'] == 151001:
                    match_dc['FavTurnover'] = turnover['Turnover']
                elif turnover['OddsID'] == 151003:
                    match_dc['UnderTurnover'] = turnover['Turnover']
            
            match_dc['odds'] = []
            match_dc['betradar'] = 1
            
            odds_tmp = [{'OddsID': x[1],'SpecialBetValue': x[2], 'Odds': x[3], 'MaxPayout': x[5],  'Turnover': x[6],'LineStatus': x[7],} for x in dc.get('odds') if x[0] == matchid]
            tmp_dc = {}
            for odd in odds_tmp:
                spv =  odd['SpecialBetValue'] 
                if spv not in tmp_dc:
                    tmp_dc[spv] = {'SpecialBetValue': spv,}
                    match_dc['odds'].append(tmp_dc[spv])
                odd_dc =  tmp_dc[spv]
                odd_dc['MaxPayout'] = odd['MaxPayout']
                odd_dc['LineStatus'] = odd['LineStatus']
                if odd['OddsID'] == 151001:
                    odd_dc['FavOdds'] = odd['Odds']
                    odd_dc['FavTurnover'] = odd['Turnover']
                    
                elif odd['OddsID'] == 151003:
                    odd_dc['UnderOdds'] = odd['Odds']
                    odd_dc['UnderTurnover'] = odd['Turnover']


            match_dc_list.append(match_dc)
        #print(match_dc_list)
        return match_dc_list
        #print(cursor)
        #return query

    #def statistics(self, query): 
        #"""
        #--查询流水
#select 
        #MatchID,
        #sum(case oddsid when 151001 then Amount else 0 end) as FavTurnover,
        #sum(case oddsid when 151003 then Amount else 0 end) as UnderTurnover
    #from dbo.TB_MatchesTurnover with(nolock)
#where matchid in( 13497287,14473288)
#group by MatchID


#--查询盘口
#select MatchID,SpecialBetValue,
        #sum(case oddsid when 151001 then odds else 0 end) as FavOdds,
        #sum(case oddsid when 151003 then odds else 0 end) as UnderOdds
    #from dbo.tb_odds with(nolock) 
#where matchid in( 13497287,14473288)
#and status =1 and oddsid in(151001,151003)
#group by MatchID,SpecialBetValue
#order by matchid

        #"""
        ##ss = query.annotate(FavTurnover = Sum('tbmatchesturnover__amount', filter = Q(tbmatchesturnover__oddsid = 151001) ), 
                            ##UnderTurnover = Sum( 'tbmatchesturnover__amount', filter = Q(tbmatchesturnover__oddsid = 151003) ))
        #ss = query.filter(tbodds__status = 1, tbodds__oddstype_id__in = [151001, 151003]).values('matchdate', 'team1zh', 'team2zh','matchid')\
            #.annotate(FavTurnover = Sum(Case(When(tbmatchesturnover__oddsid = 151001 , then= F('tbmatchesturnover__amount')), default=0, output_field=DecimalField()) ), 
                    #UnderTurnover = Sum( Case(When(tbmatchesturnover__oddsid = 151003 , then= F('tbmatchesturnover__amount')), default=0, output_field=DecimalField() ) ) ) \
            #.order_by('matchid')
            ##.annotate(FavOdds = Sum(Case(When(tbodds__oddstype_id = 151001, then= F('tbodds__odds')), default = 0, output_field = DecimalField())), 
                        ##UnderOdds = Sum(Case(When(tbodds__oddstype_id = 151003, then = F('tbodds__odds')), default = 0, output_field = DecimalField())))\


        #return ss

    def dict_row(self, inst): 
        return {
            'event': '%s<br>%s' % (inst.team1zh, inst.team2zh),
            #'FavTurnover': str(inst.FavTurnover),
            #'UnderTurnover': str(inst.UnderTurnover),
            #'FavOdds': str(inst.FavOdds),
            #'UnderOdds': str(inst.UnderOdds),
        }
    #def get_rows(self): 
        #rows = super().get_rows()
        #newodds1 = TbOdds.objects.filter(status = 1, oddstype_id = 151001,specialbetvalue = OuterRef('tbodds__specialbetvalue'), match = OuterRef('matchid')).order_by('-tid')
        #newodds3 = TbOdds.objects.filter(status = 1, oddstype_id = 151003,specialbetvalue = OuterRef('tbodds__specialbetvalue'), match = OuterRef('matchid')).order_by('-tid')

        #matchids = [row['matchid'] for row in rows]
        #query = TbMatches.objects.filter(matchid__in = matchids, tbodds__oddstype_id__in = [151001, 151003]).values('matchid', 'tbodds__specialbetvalue')\
            #.annotate(FavOdds = Subquery(newodds1.values('odds')[:1]), 
                    #UnderOdds = Subquery(newodds3.values('odds')[:1])).order_by('matchid').distinct()

        ##query = TbMatches.objects.filter(matchid__in = matchids).annotate(FavOdds = Sum(Case(When(Q(tbodds__oddstype_id = 151001) | Q( tbodds__tid = Max()), then= F('tbodds__odds')), default = 0, output_field = DecimalField())), 
                                                                            ##UnderTurnover = Sum(Case(When(tbodds__oddstype_id = 151001, then= F('tbodds__odds')), default = 0, output_field = DecimalField()))        
        #print(query)

class  OddsTypeGroup2Table(OddsTypeGroup4Table):
    pass

director.update({
    'maindb.OddsTypeGroup4Table': OddsTypeGroup4Table,
    'maindb.typegroup_2': OddsTypeGroup2Table,
})

page_dc.update({
    'maindb.TbOdds': OddsPage,
})