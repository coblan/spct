# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import gettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter, director, SelectSearch, model_to_name
from ..models import TbTicketmaster, TbTicketstake, TbTicketparlay, TbMatches, TbMatchesBasketball
from django.db.models import Q, Sum, F, Case, When, FloatField
import re
from django.db import connections
from helpers.director.middleware.request_cache import get_request_cache
from .. import status_code

class TicketMasterPage(TablePage):
    template = 'jb_admin/table.html'  # 'maindb/table_ajax_tab.html'

    def get_label(self):
        return _('Tb Trans')  # '注单列表'
    
    @staticmethod
    def get_tabs(): 
        catch = get_request_cache()
        crt_user =  catch.get('request').user
        ls = [
            {'name': 'ticketstake',
             'label': '子注单',
             'com': 'com-tab-table',
             'par_field': 'ticketid',
             'table_ctx': TicketstakeTable(crt_user=crt_user).get_head_context()
             },
            {'name': 'ticketparlay',
             'label': '串关规则',
             'com': 'com-tab-table',
             'par_field': 'ticketid',
             'table_ctx': TicketparlayTable(crt_user=crt_user).get_head_context()
             }
        ]
        return {
             'ticketmaster': ls
        }
    
    @classmethod
    def get_named_ctx(cls): 
        catch = get_request_cache()
        crt_user =  catch.get('request').user
        
        dc = cls.get_tabs()
        dc.update({
            'match_form_ctx': {
                'fields_ctx' : MatchForm(crt_user=crt_user).get_head_context(), 
                'after_save' : {
                    'fun': 'do_nothing'
                    # 'fun':'update_or_insert'
                }, 
                'get_row': {
                    "fun": 'get_with_relat_field',
                    'director_name': 'games.ticketstake.matchform',
                    'relat_field': 'matchid',
                }
                },
            'basketball_match_form_ctx': {
                'fields_ctx' : BasketballMatchForm(crt_user=crt_user).get_head_context(), 
                'after_save' : {
                    'fun': 'do_nothing'
                }, 
                'get_row': {
                    "fun": 'get_with_relat_field',
                    'director_name': 'games.ticketstake.basketball_matchform',
                    'relat_field': 'matchid',
                }
                },
        })
        return dc

    def get_context(self):
        ctx = TablePage.get_context(self)
        ctx['named_ctx'] = self.get_named_ctx()
        return ctx
        

    class tableCls(ModelTable):
        model = TbTicketmaster
        exclude = ['accountid']
        fields_sort = ['ticketid', 'orderid', 'accountid__nickname', 'parlayrule', 'status',
                       'winbet', 'stakeamount', 'betamount', 'betoutcome', 'turnover', 'bonuspa', 'bonus', 'profit',
                       'createtime', 'settletime', 'memo','voidreason']
        
        @classmethod
        def clean_search_args(cls, search_args):
            if not search_args.get('_has_default'):
                search_args['accountid__accounttype'] = search_args.get('accountid__accounttype',0)
            return search_args
        
        def dict_head(self, head):
            if head['name'] in ['createtime', 'settletime']:
                head['width'] = 140
            elif head['name'] in ['status', 'orderid', 'accountid__nickname', 'betamount', 'betoutcome', 'turnover',
                                  'bonus',
                                  'profit']:
                head['width'] = 120
            else:
                head['width'] = 80
            if head['name'] == 'ticketid':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'ticketstake'
                head['ctx_name'] = 'ticketmaster'
                #head['named_tabs'] = 'ticketmaster'

            return head

        def getExtraHead(self):
            return [{'name': 'profit', 'label': '亏盈'}, 
                    {'name': 'accountid__nickname','label': '昵称',}]

        def dict_row(self, inst):
            dc = {
                'accountid__nickname': inst.accountid__nickname,
            }
            # if inst.status == 2:
            #     dc.update( {'profit': round(inst.betoutcome - inst.betamount + inst.bonus, 2)} )
            if not inst.profit or inst.status != 2:
                dc['profit'] = '0.00'
            else:
                dc['profit'] = inst.profit

            if not inst.betoutcome:
                dc['betoutcome'] = '0.00'
            if not inst.turnover:
                dc['turnover'] = '0.00'
            if not inst.bonus:
                dc['bonus'] = '0.00'

            if inst.status != 2:
                dc['winbet'] = None
            return dc

        def inn_filter(self, query):
            return query.order_by('-createtime').annotate(profit=F('betoutcome') - F('betamount') + F('bonus')) \
                .annotate(accountid__nickname=F('accountid__nickname'))

        def statistics(self, query):
            dc = query.aggregate(total_betamount=Sum('betamount'), total_betoutcome=Sum('betoutcome'),
                                 total_turnover=Sum('turnover'), total_bonus=Sum('bonus'),
                                 total_profit=Sum(
                                     Case(When(status=2, then=F('betoutcome') - F('betamount') + F('bonus')),
                                          default=0)))

            mapper = {
                'total_betamount': 'betamount' ,
                'total_betoutcome': 'betoutcome' ,
                'total_turnover': 'turnover',
                'total_bonus': 'bonus',
                'total_profit':'profit'
            }
            for k in dc:
                dc[k] = str(round(dc.get(k, 0) or 0, 2))
            normed_dc = {mapper.get(k): v for (k, v) in dc.items()}
            #footer = [dc.get(mapper.get(name), '') for name in self.fields_sort]
            self.footer = self.footer_by_dict(normed_dc)
            self.footer = ['合计'] + self.footer
            return query

        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['footer'] = self.footer
            return ctx

        def get_operation(self):
            return [
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '作废',
                 'pre_set': 'rt={status:-1,memo:""}',
                 #'field': 'status', 'value': 30,
                 'row_match': 'many_row', 
                 'match_express':'rt= ex.isin( scope.row.status,[0,1])',
                 #'match_field': 'status', 'match_values': [0,1], 
                'match_msg': '只能选择【确认中】或【未结算】的订单',
                 'confirm_msg': '确认作废这些注单吗?', 'fields_ctx': {
                    'heads': [{'name': 'memo', 'label': '备注', 'editor': 'blocktext', }],
                    'ops': [{'fun': 'save', 'label': '确定', 'editor': 'com-op-btn', }],
                }, 'visible': 'status' in self.permit.changeable_fields(),},
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]

        class search(SelectSearch):
            names = ['accountid__nickname']
            exact_names = ['orderid', 'tbticketstake__mainmatchid']

            def get_option(self, name):

                if name == 'orderid':
                    return {'value': name,
                            'label': '订单编号', }
                elif name == 'accountid__nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }
                elif name == 'tbticketstake__mainmatchid':
                    return {
                        'value': name,
                        'label': 'matchid',
                    }

            def clean_search(self):
                if self.qf in ['ticketid', 'tbticketstake__mainmatchid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()

        class filters(RowFilter):
            range_fields = ['createtime', 'settletime']
            names = ['status', 'winbet','accountid__accounttype']
            
            def getExtraHead(self):
                return [
                    {'name':'accountid__accounttype','label':'账号类型','editor':'com-filter-select','options':[{'value':value,'label':label} for value,label in status_code.ACCOUNT_TYPE]}
                ]
            def clean_query(self, query): 
                search_args = self.kw.get('search_args')
                if search_args.get('winbet', None) != None :
                    query= query.filter(status = 2)
                if search_args.get('accountid__accounttype',None) !=None:
                    query= query.filter(accountid__accounttype=search_args.get('accountid__accounttype'))
                return query

        class sort(RowSort):
            names = ['stakeamount', 'betamount', 'createtime', 'betoutcome', 'turnover', 'bonuspa', 'bonus', 'profit',
                     'settletime']


class TicketMasterForm(ModelFields):
    class Meta:
        model = TbTicketmaster
        fields = ['status', 'memo']

    def save_form(self):
        if 'status' in self.changed_data and self.cleaned_data['status'] == -1:
            sql = 'exec [dbo].[SP_CancelTicket] %(ticketid)s,-1' % {'ticketid': self.instance.ticketid}
            cursor = connections['Sports'].cursor()
            cursor.execute(sql)
            cursor.commit()
            self.instance.memo = self.kw.get('memo')
            self.instance.save()
            self.save_log({'model': model_to_name(TbTicketmaster), 'memo': '取消订单', 'pk': self.instance.pk,})
        else:
            super().save_form()


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
    fields_sort = ['tournament', 'matchid', 'matchname', 'whole_score','oddskind','oddsid','oddsid__outcomedesc','specialbetname', 'odds', 'confirmodds', 'realodds', 
                   'status', 'createtime', 'updatetime']

    def getExtraHead(self):
        return [
            #{'name': 'matchid', 'label': 'matchid', },
            {'name': 'matchname', 'label': '比赛', 'width': 200, },
            {'name': 'tournament', 'label': '联赛', 'width': 120, },
            {'name':'whole_score','label':'当时比分','width':100},
            {'name': 'oddsid__outcomedesc', 'label': '盘口类型', 'width': 90, },
        ]

    def dict_row(self, inst):
        match = inst.match  # TbMatches.objects.get(matchid =  inst.matchid)
        if inst.sportid == 0:
            matchid_form = 'match_form_ctx'
        elif inst.sportid == 1:
            matchid_form = 'basketball_match_form_ctx'
        else:
            raise UserWarning('子注单%s无法匹配比赛' % inst.tid)
        return {
            'whole_score':'%s:%s'%(inst.homescore,inst.awayscore),
            '_matchid_form': matchid_form,
            'matchid': match.matchid,
            'tournament': match.tournamentzh,
            'oddsid__outcomedesc':inst.oddsid.outcomedesc,
            'matchname': '{team1zh} VS {team2zh}'.format(team1zh=match.team1zh, team2zh=match.team2zh)
        }

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

        #if head['name'] == 'match':
            #head['label'] = '比赛'
        if head['name'] == 'matchid':
            head['editor'] = 'com-table-pop-fields-from-row'
            head['ctx_field'] = '_matchid_form'
            #head['fields_ctx'] = MatchForm(crt_user=self.crt_user).get_head_context()
            #head['after_save'] = {
                #'fun': 'do_nothing'
                ## 'fun':'update_or_insert'
            #}
            ## head['fields_heads']= MatchForm(crt_user=self.crt_user).get_heads()
            ## head['model_name']=model_to_name(TbMatches)
            #head['get_row'] = {
                #"fun": 'get_with_relat_field',
                #'director_name': 'games.ticketstake.matchform',
                #'relat_field': 'matchid',
            #}
            ## head['ops']=[] #MatchForm(crt_user=self.crt_user).get_operations()
        return head


class TicketparlayTable(ModelTable):
    model = TbTicketparlay
    exclude = ['tid']

    def dict_head(self, head):
        if head['name'] == 'createtime':
            head['width'] = 150
        else:
            head['width'] = 80

        return head

    def inn_filter(self, query):
        ticketid = self.kw.get('ticketid')
        # master = TbTicketmaster.objects.get(ticketid = ticketid)
        return query.filter(
            ticket_master_id=ticketid)  # .select_related('parlay1tid__match', 'parlay2tid__match', 'parlay3tid__match', 'parlay4tid__match', 'parlay5tid__match',  'parlay6tid__match')

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
    field_sort = ['matchdate', 'team1zh', 'team2zh', 'period1score','matchscore', 'winner', 'statuscode', 'roundinfo'
                                                                                           'livebet', 'generatedat',
                  'tournamentzh']
    readonly = field_sort
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        if kw.get('matchid'):
            instance = TbMatches.objects.get(matchid = kw.get('matchid'))
            super().__init__(dc, pk, crt_user, nolimit, instance = instance,**kw)
        else:
            super().__init__(dc, pk, crt_user, nolimit, *args, **kw)

    class Meta:
        model = TbMatches
        exclude = []

    def get_operations(self):
        return []
    
    def dict_head(self, head): 
        if head['name'] == 'winner':
            head['editor'] = 'linetext'
        return head

    def dict_row(self, inst):
        
        if inst.winner == 1:
            winner = inst.team1zh
        elif inst.winner == 2:
            winner = inst.team2zh
        else:
            winner = '---'
        return {
            'winner': winner
        }


class BasketballMatchForm(MatchForm):
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        if kw.get('matchid'):
            instance = TbMatchesBasketball.objects.get(matchid = kw.get('matchid'))
            super(MatchForm, self).__init__(dc, pk, crt_user, nolimit, instance = instance,**kw)
        else:
            super(MatchForm, self).__init__(dc, pk, crt_user, nolimit, *args, **kw)    
            
    class Meta:
        model = TbMatchesBasketball
        exclude = [] 

director.update({
    'games.ticketmaster': TicketMasterPage.tableCls,
    'games.ticketmaster.edit': TicketMasterForm,

    'games.TicketstakeTable': TicketstakeTable,
    'games.TicketparlayTable': TicketparlayTable,

    'games.ticketstake.matchform': MatchForm,
     'games.ticketstake.basketball_matchform': BasketballMatchForm,

})

page_dc.update({
    'tickets': TicketMasterPage,
})
