# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import gettext as _
from helpers.director.shortcut import TablePage, ModelTable, page_dc, ModelFields, \
    RowSearch, RowSort, RowFilter, director, SelectSearch, model_to_name,director_view,has_permit
from ..models import TbTicketmaster, TbTicketstake, TbTicketparlay, TbMatch,TbMessageUnsend
from django.db.models import Q, Sum, F, Case, When, FloatField,Count
import re
from django.db import connections
from helpers.director.middleware.request_cache import get_request_cache
from .. import status_code
from .matches import get_match_tab
from helpers.func.collection.container import evalue_container
from django.utils import timezone
from helpers.director.model_func.dictfy import sim_dict
from helpers.func.collection.mylist import split_list
from hello.merchant_user import get_user_merchantid,MerchantInstancCheck
from helpers.director.access.permit import can_write
from django.db.models import Prefetch
import logging

operation_log =logging.getLogger('operation_log')

class TicketstakeTable(ModelTable):
    """ 子注单 """
    model = TbTicketstake
    exclude = ['marketid']
    fields_sort = ['tournament', 'matchid', 'matchname','oddskind','marketname','specialbetname','outcomename','score', 'odds', 'confirmodds', 'realodds', 
                   'status', 'createtime', 'updatetime','ticketbetstopdiff','oddsource','dangeroustid']

    
    def inn_filter(self, query):
        ticketid = self.kw.get('ticketid')
        query = query.using('Sports_nolock').extra(select={
            'tournament':'select TB_Tournament.tournamentnamezh'},
                            tables=['TB_Tournament','TB_Match'],
                            where=['TB_Tournament.tournamentid=TB_Match.tournamentid and TB_Match.sportid=TB_Tournament.sportid',
                                   'TB_Match.matchid=TB_TicketStake.matchid']
                            )
        if ticketid:
            return query.filter(ticket_master_id = ticketid)
        else:
            return query

    def getExtraHead(self):
        return [
            {'name': 'matchname', 'label': '比赛', 'width': 200,'editor':'com-table-rich-span','cell_class':'scope.row.ticketstake_match_source != 1?"jjyy":""','css':'.jjyy{color:black;background-color:#F7DF9C}' },
            {'name': 'tournament', 'label': '联赛', 'width': 160, },
        ]

    def dict_row(self, inst):

        return {
            '_matchid_form': 'match_form_ctx',#  matchid_form,
            'matchid': inst.matchid.matchid,
            'tournament': inst.tournament,
            'matchname': '{team1zh} VS {team2zh}'.format(team1zh=inst.matchid.team1zh, team2zh=inst.matchid.team2zh),
            'ticketbetstopdiff':inst.ticketbetstopdiff/1000 if inst.ticketbetstopdiff else '',
            'ticket_master':inst.ticket_master_id,
            'match_source':inst.matchid.source
        }

    def dict_head(self, head):
        dc = {
            'tid': 80,
            'match': 250,
            'marketname':160,
            'specialbetvalue': 80,
            'odds': 80,
            'confirmodds': 80,
            'realodds': 80,
            'confirmoddsid_ori': 80,
            'status': 80,
            'updatetime': 150,
            'createtime': 150,
            'ticketbetstopdiff':150,
        }
        if dc.get(head['name']):
            head['width'] = dc.get(head['name'])

        #if head['name'] == 'match':
            #head['label'] = '比赛'
        if head['name'] == 'matchid':
            head['editor'] = 'com-table-switch-to-tab'
            head['tab_name']='match_base_info'
            head['ctx_name']='match_tabs'
            #head['editor'] = 'com-table-pop-fields-from-row'
            #head['ctx_field'] = '_matchid_form'
        return head


class TicketstakeEmbedTable(TicketstakeTable):
    fields_sort = ['ticketstake_'+x for x in TicketstakeTable.fields_sort]
    
    def inn_filter(self, query):
        query = query.extra(select={
            'tournament':'select TB_Tournament.tournamentnamezh'},
                            tables=['TB_Tournament','TB_Match'],
                            where=['TB_Tournament.tournamentid=TB_Match.tournamentid and TB_Match.sportid=TB_Tournament.sportid',
                                   'TB_Match.matchid=TB_TicketStake.matchid']
                            )
        master_id_list = self.kw.get('master_id_list')
        return query.filter(ticket_master_id__in = master_id_list).select_related('matchid')
    
    def dict_head(self, head):
        head = super().dict_head(head)
        
        if head['name'] == 'matchid':
            head['editor'] = 'com-table-click'
            head['action']='scope.head["par_row"]={matchid:scope.row.ticketstake_matchid,sportid:scope.row.ticketstake_sportid};scope.ps.switch_to_tab(scope.head)'
            head['tab_name']='match_base_info'
            head['ctx_name']='match_tabs'
        
        head.update({
            'name':'ticketstake_'+head['name'],
            'row_editor':head['editor']
          })
               
        head.update({
            'sublevel':True,
            'editor':'com-field-multi-row',
            'rows_field':'ticketstake',
            'show_tooltip':False,
        })
        return head
    
    def get_rows(self):
        rows = super().get_rows()
        out_rows=[]
        for row in rows:
            dc ={}
            for k,v in row.items():
                if not k.startswith('_') and k not in ['pk']:
                    dc['ticketstake_'+k] = v
                elif k.startswith('_') and k.endswith('_label'):
                    dc['_ticketstake_'+k[1:]] =v
                else:
                    dc[k] = v

            out_rows.append(dc)
        return out_rows


class TicketMasterPage(TablePage):
    template = 'jb_admin/table.html'  # 'maindb/table_ajax_tab.html'

    def get_label(self):
        return _('Tb Trans')  # '注单列表'
    
    @staticmethod
    def get_tabs(): 
        from ..member.account import account_tab
        named_ctx = get_request_cache()['named_ctx']
        crt_user =  get_request_cache().get('request').user
        if 'ticketmaster' in named_ctx:
            return {}
        named_ctx['ticketmaster'] = []
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
        named_ctx['ticketmaster'] = ls
        
        if 'match_tabs' not in named_ctx:
            named_ctx['match_tabs'] = evalue_container( get_match_tab(crt_user) )
        account_tab()
        #if 'account_tabs' not in named_ctx:
            #named_ctx['account_tabs'] = account_tab()
        return {}
    
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
            #'basketball_match_form_ctx': {
                #'fields_ctx' : BasketballMatchForm(crt_user=crt_user).get_head_context(), 
                #'after_save' : {
                    #'fun': 'do_nothing'
                #}, 
                #'get_row': {
                    #"fun": 'get_with_relat_field',
                    #'director_name': 'games.ticketstake.basketball_matchform',
                    #'relat_field': 'matchid',
                #}
                #},
        })
        return dc

    def get_context(self):
        ctx = TablePage.get_context(self)
        ctx['named_ctx'] = self.get_named_ctx()
        return ctx
        

    class tableCls(ModelTable):
        model = TbTicketmaster
        exclude = ['accountid']
        fields_sort = ['merchant','sp_status','ticketid','createtime', 'accountid__nickname', 'ticketstake',] +TicketstakeEmbedTable.fields_sort + \
        ['orderid','audit',  'status','winbet','parlayrule', 'stakeamount', 'betamount', 'betoutcome', 'profit',
         'turnover', 'bonuspa', 'bonus', 'settletime', 'memo','voidreason','terminal','updatetime','betactionelapsed']
        
        @classmethod
        def clean_search_args(cls, search_args):
            if search_args.get('_first_access',1):
                search_args['accountid__accounttype'] = search_args.get('accountid__accounttype',0)
                search_args['_first_access'] = 0 
                now = timezone.now()
                start = ( now-timezone.timedelta(days=1) ) .strftime('%Y-%m-%d 00:00:00')
                search_args['_start_createtime'] = start
                search_args['status'] =[0,1,2,11]
            return search_args
        
        def dict_head(self, head):
            if head['name'] in ['createtime', 'settletime']:
                head['width'] = 140
            elif head['name'] in ['status', 'orderid', 'accountid__nickname', 'betamount', 'betoutcome', 'turnover',
                                  'bonus',
                                  'profit']:
                head['width'] = 120

            #if head['name'] == 'ticketid':
                #head['editor'] = 'com-table-switch-to-tab'
                #head['tab_name'] = 'ticketstake'
                #head['ctx_name'] = 'ticketmaster'
            if head['name']=='accountid__nickname':
                head['editor'] ='com-table-switch-to-tab'
                head['ctx_name']='account_tabs'
                head['tab_name'] ='dashborad'
                #head['']
            if head['name'] =='betamount':
                head['inn_editor'] = head['editor']
                head['editor']='com-table-rich-span'
                head['css']='.danger_bet{color:white;background:#FF4E4C}'
                head['cell_class'] = 'rt= scope.row.betamount>1000?"danger_bet":""'
            
            if head['name'] =='audit':
                head['css']='.audit_danger{color:red}'
                head['inn_editor'] = head['editor']
                head['editor']='com-table-rich-span'
                head['class']='middle-col btn-like-col'
                head['cell_class'] = 'var dc={0:"success",1:"warning",2:"primary"};rt=dc[scope.row.audit]'
                #head['cell_class'] ='scope.row.audit !=0 ? "audit_danger" :""'
               
            return head

        def getExtraHead(self):
            stake_heads = TicketstakeEmbedTable().get_heads()
            return [
                {'name':'sp_status','label':'图标提示','editor':'com-table-icon-cell','width':70,'show_tooltip':False,
                 'icon_express':'''var pig=[];rt=pig;
                 if(scope.row.long_time_no_confirm){pig.push({url:"/static/images/超时.png",label:"长期未确认"})}
                 if(scope.row.audit==1){pig.push({"url":"/static/images/异常.png","label":"异常注单"})} 
               ''' },
                
                {'name': 'profit', 'label': '亏盈'}, 
                {'name': 'accountid__nickname','label': '昵称',},
                {'name':'ticketstake','label':'子注单','children':TicketstakeEmbedTable.fields_sort,
                 'class':'mystake','style':'th.mystake{background-color:#48A66C !important;color:white;text-align:center !important}'},
                    ]+ stake_heads

        def dict_row(self, inst):
            now = timezone.now()
            dc = {
                'accountid__nickname': inst.accountid__nickname,
                'stake_count':inst.stake_count,
                'accountid':inst.accountid_id , # 在 fields 中 exclude 了，但是为了显示 account_tabs，需要par_row 具备accountid 属性，所以这里手动导出
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
            if inst.status ==0 and ( now - inst.createtime ) > timezone.timedelta(minutes=5):
                dc['long_time_no_confirm']=True
            return dc

        def inn_filter(self, query):
            if self.crt_user.merchant:
                query = query.filter(merchant_id = self.crt_user.merchant.id)
                
            return query.using('Sports_nolock').order_by('-createtime').annotate(profit=F('betoutcome') - F('betamount') + F('bonus')) \
                .annotate(accountid__nickname=F('accountid__nickname'),stake_count=Count('tbticketstake'))
        
        def get_rows(self):
            rows = super().get_rows()
            rows_pklist = [x['pk'] for x in rows]
            dc={}
            for row in rows:
                dc[row['pk']]=[]
            for batch_pklist in split_list(rows_pklist, 200):
                for stake in  TicketstakeEmbedTable(master_id_list = batch_pklist,perpage=2000).get_rows():
                    dc[stake.get('ticketstake_ticket_master')].append(stake)
                
            for row in rows:
                row.update({
                    'ticketstake':dc[row['pk'] ]
                    #'matchid':[x['matchid'] for x in dc[row['pk']]],
                    #'matchname':[x['matchname'] for x in dc[row['pk']]],
                    #'marketname':[x['marketname'] for x in dc[row['pk']]]
                })
            
            return rows
         
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
            normed_dc.update({
                '_label':'合计'
            })
            #self.footer = self.footer_by_dict(normed_dc)
            #self.footer = ['合计'] + self.footer
            self.footer = normed_dc
            return query
        
        def get_head_context(self):
            ctx = super().get_head_context()
            heads_names = [head['name'] for head in ctx.get('heads')]
            ctx.update({
                'advise_heads':heads_names,
            })
            return ctx

        def get_operation(self):
            return [
                {'editor':'com-op-btn','label':'设置列','icon': 'fa-gear',
                 'action':'cfg.pop_vue_com("com-panel-table-setting",{table_ps:scope.ps,title:"设置列"})'},
                {'editor':'com-op-table-refresh','label':'自动刷新频率','options':[
                    {'value':10*1000,'label':'10秒'},
                    {'value':30*1000,'label':'30秒'},
                    {'value':1*60*1000,'label':'1分钟'},
                    #{'value':2*60*1000,'label':'2分钟'},
                    #{'value':3*60*1000,'label':'3分钟'},
                ],'action':'rt= scope.ps.search()'},
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 'label': '作废',
                 'pre_set': 'rt={status:-1,voidreason:""}',
                 #'field': 'status', 'value': 30,
                 'row_match': 'many_row', 
                 'match_express':'rt= ex.isin( scope.row.status,[0,1,11])',
                 #'match_field': 'status', 'match_values': [0,1], 
                'match_msg': '只能选择【确认中】,【未结算】,【危险球】的订单',
                 'confirm_msg': '确认作废这些注单吗?', 'fields_ctx': {
                    'heads': [{'name': 'voidreason', 'label': '备注', 'editor': 'blocktext', }],
                    'ops': [{'fun': 'save', 'label': '确定', 'editor': 'com-op-btn', }],
                }, 'visible': 'status' in self.permit.changeable_fields(),},
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', },
                {'editor':'com-op-btn',
                 'label':'审核通过',
                 'row_match':'one_row','match_express':' rt = scope.row.audit == 1', 'match_msg': '只能选择异常注单',
                 'action':'''(function(){
                 if (!scope.ps.check_selected(scope.head)){return};
                 cfg.confirm("确定审核该条注单吗？")
                 .then(res=>{
                    scope.ps.selected.forEach(row=>{row.audit=2});
                    cfg.show_load();
                    return ex.director_call("save_rows",{rows:scope.ps.selected})
                 })
                 .then(res=>{return cfg.showMsg("操作成功!")})
                 .then((res)=>{scope.ps.search()})
                 })()''',
                 'visible': 'audit' in self.permit.changeable_fields()
                 },
                {'fun':'director_call',
                 'director_name':'match.makesure_ticketmaster', 
                 'editor':'com-op-btn','label':'确认注单',
                 'confirm_msg':'确认该注单？',
                 #'icon':'fa-exclamation-triangle',
                 'row_match':'one_row',
                 'match_express':'ex.isin( scope.row.status,[0,11])',
                 'after_save':'scope.ps.search()',
                 'match_msg':"只能选择状态为[确认中,危险球]的注单",
                 'visible':can_write(TbTicketmaster,self.crt_user)},
                 #'action':'ex.director_call("save_rows",scope.ps.selected_rows).then((rows)=>{ex.each(rows,(row)=>{scope.ps.update_or_insert(row)})})'}
            ]
        
        def getExcelRows(self):
            operation_log.info('开始导出注单列表excel')
            query=self.get_query()
            query = query.prefetch_related( 
                Prefetch('tbticketstake_set',queryset=TbTicketstake.objects.using('Sports_nolock').select_related('matchid','marketid').extra(select={
            'tournament':'select TB_Tournament.tournamentnamezh'},
                            tables=['TB_Tournament','TB_Match'],
                            where=['TB_Tournament.tournamentid=TB_Match.tournamentid and TB_Match.sportid=TB_Tournament.sportid',
                                   'TB_Match.matchid=TB_TicketStake.matchid']
                            ) ) 
                ).all()  #'tbticketstake_set',
            query = query[:1000] 
            out=[]
            permit_fields =  self.permited_fields()
            for inst in query:
                cus_dict = self.dict_row( inst)
                dc = sim_dict(inst, include=permit_fields,filt_attr=cus_dict)
                dc.update(cus_dict)
                first = True
                for stake in inst.tbticketstake_set.all():
                    if first:
                        mydc = dict(dc)
                        first =False
                    else:
                        mydc ={}
                    dd = TicketstakeEmbedTable.dict_row(None,stake)
                    stake_dc = sim_dict(stake,filt_attr=dd)
                    stake_norm_dc = {}
                    for k,v in stake_dc.items():
                        if not k.startswith('_') and k not in ['pk']:
                            stake_norm_dc['ticketstake_'+k] = v
                        elif k.startswith('_') and k.endswith('_label'):
                            stake_norm_dc['_ticketstake_'+k[1:]] =v
                        #else:
                            #stake_norm_dc[k] = v

                    mydc.update(stake_norm_dc)
                    out.append(mydc)
            operation_log.info('导出注单列表excel查询完成')
            return out
        
        class search(SelectSearch):
            names = ['accountid__nickname']
            exact_names = ['ticketid','orderid', 'tbticketstake__matchid']

            def get_option(self, name):

                if name == 'orderid':
                    return {'value': name,
                            'label': '订单编号', }
                elif name == 'accountid__nickname':
                    return {
                        'value': name,
                        'label': '昵称',
                    }
                elif name == 'tbticketstake__matchid':
                    return {
                        'value': name,
                        'label': 'matchid',
                    }
                elif name =='ticketid':
                    return {
                        'value':name,
                        'label':'注单ID'
                    }

            def clean_search(self):
                if self.qf in ['ticketid', 'tbticketstake__matchid']:
                    if not re.search('^\d*$', self.q):
                        return None
                    else:
                        return self.q
                else:
                    return super().clean_search()

        class filters(RowFilter):
            range_fields = ['createtime', 'settletime']
            #names = ['status','audit', 'winbet','terminal','accountid__accounttype','merchant']
            
            @property
            def names(self):
                if  self.crt_user.merchant:
                    return ['status','audit', 'winbet','terminal','accountid__accounttype']
                else:
                    return ['merchant','status','audit', 'winbet','terminal','accountid__accounttype',]
            
            def clean_search_args(self, search_args):
                #if search_args.get('createtime__gte'):
                    #start = timezone.datetime.strptime(search_args.get('createtime__gte'),'%Y-%m-%d %H:%M:%S')
                    #if timezone.now() - start > timezone.timedelta(days=2):
                        #raise UserWarning('只能查询两天内的注单信息')
                return search_args
            
            def dict_head(self, head):
                if head['name'] =='status':
                    head['editor'] = 'com-filter-multi-select'
                    head['width']='170px'
                return head
            
            def getExtraHead(self):
                return [
                    {'name':'is_multi_stake','placeholder':'单注/串关','editor':'com-filter-select','options':[
                        {'value':1,'label':'单注'},{'value':2,'label':'串关'}
                    ]},
                    {'name':'accountid__accounttype','placeholder':'账号类型','editor':'com-filter-select',
                     'options':[{'value':value,'label':label} for value,label in status_code.ACCOUNT_TYPE]},
                    #{'name':'meta_need_audit','label':'正常/异常','editor':'com-filter-select',
                     #'options':[{'value':'0','label':'正常注单'},
                                #{'value':'1','label':'异常注单'},
                                #{'value':'2','label':'审核过的'},]},
                ]
            
            #def clean_search_args(self, search_args):
                #if '_need_audit' in search_args:
                    #search_args.pop('_need_audit')
                #return search_args
            
            def clean_query(self, query): 
                search_args = self.kw.get('search_args')
                if search_args.get('winbet', None) != None :
                    query = query.filter(status = 2)
                if search_args.get('accountid__accounttype',None) !=None:
                    query = query.filter(accountid__accounttype=search_args.get('accountid__accounttype'))
                if search_args.get('is_multi_stake') ==1:
                    query = query.filter(stake_count = 1)
                if search_args.get('is_multi_stake') ==2:
                    query = query.filter(stake_count__gte = 2)
                #if search_args.get('meta_need_audit') == '1':
                    ## 不正常的
                    #query= query.filter(audit = 1)
                #elif search_args.get('meta_need_audit') == '0':
                    ## 正常的
                    #query= query.exclude(audit = 1)
                #elif search_args.get('meta_need_audit') == '2':
                    #query= query.filter(audit = 2)
                return query

        class sort(RowSort):
            names = ['stakeamount', 'betamount', 'createtime', 'betoutcome', 'turnover', 'bonuspa', 'bonus', 'profit',
                     'settletime']


class TicketMasterForm(MerchantInstancCheck,ModelFields):
    class Meta:
        model = TbTicketmaster
        fields = ['status', 'voidreason','audit']

    def save_form(self):
        if 'status' in self.changed_data and self.cleaned_data['status'] == -1:
            sql = r"exec [dbo].[SP_CancelTicket] %(ticketid)s,%%s" % {
                'ticketid': self.instance.ticketid,
                #'VoidReason':self.kw.get('memo')
            }
            cursor = connections['Sports'].cursor()
            cursor.execute(sql,[self.kw.get('voidreason')])
            cursor.commit()
            #self.instance.memo = self.kw.get('memo')
            #self.instance.save()
            self.save_log({'model': model_to_name(TbTicketmaster), 'voidreason': '取消订单', 'pk': self.instance.pk,})
        else:
            super().save_form()


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
            parlay = getattr(inst, field_name)
            if parlay:
                dc[field_name] = '{team1zh}VS{team2zh}'.format(team1zh=parlay.matchid.team1zh,
                                                               team2zh=parlay.matchid.team2zh)
            else:
                dc[field_name] = ''
        return dc

class MatchForm(ModelFields):
    field_sort = ['matchdate', 'team1zh', 'team2zh', 'period1score','winner', 'statuscode', 'roundinfo'
                    'livebet', 'generatedat','tournamentzh'] #'matchscore', 
    readonly = field_sort
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        if kw.get('matchid'):
            instance = TbMatch.objects.get(matchid = kw.get('matchid'))
            super().__init__(dc, pk, crt_user, nolimit, instance = instance,**kw)
        else:
            super().__init__(dc, pk, crt_user, nolimit, *args, **kw)

    class Meta:
        model = TbMatch
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

@director_view('match.makesure_ticketmaster')
def make_sure_ticketmaster(rows,**kws):
    ticket_list = [row.get('pk') for row in rows]
    #s30_ago = timezone.now() - timezone.timedelta(seconds=30)
    #count = TbTicketmaster.objects.filter(pk__in=ticket_list,createtime__lte=s30_ago).update(status=1)
    crt_user = get_request_cache()['request'].user
    if crt_user.merchant:
        query = TbTicketmaster.objects.filter(merchant = crt_user.merchant)
    else:
        query = TbTicketmaster.objects.all()
    now = timezone.now()
    count = query.filter(pk__in=ticket_list).update(status=1,updatetime=now)
    if count==0:
        raise UserWarning('确认不成功，不存在对应的注单')
    master = query.get(pk = rows[0]['pk'])
    TbMessageUnsend.objects.create(body='注单%s投注成功'%master.orderid,type=1,sender='Backend',accountid = master.accountid_id,relationno=master.ticketid)
    stake_count =TbTicketstake.objects.filter(ticket_master_id__in=ticket_list,status =0).update(status =1,confirmodds=F('odds'))
    operation_log.info('确认注单%s'%ticket_list)
    #return {
        #'msg':'确认成功,修改小单%s条'%stake_count
    #}

director.update({
    'games.ticketmaster': TicketMasterPage.tableCls,
    'games.ticketmaster.edit': TicketMasterForm,

    'games.TicketstakeTable': TicketstakeTable,
    'games.TicketparlayTable': TicketparlayTable,

    'games.ticketstake.matchform': MatchForm,
     #'games.ticketstake.basketball_matchform': BasketballMatchForm,
})

page_dc.update({
    'tickets': TicketMasterPage,
})
