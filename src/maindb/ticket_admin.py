# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import gettext as _
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,model_to_name
from .models import TbTicketmaster,TbTicketstake,TbTicketparlay,TbMatches
from .status_code import *


class TicketMasterPage(TablePage):
    template='maindb/table.html' #'maindb/table_ajax_tab.html'
    def get_label(self):
        return  _('Tb Trans') #  '注单列表'

    def get_context(self):
        ctx = TablePage.get_context(self)
        ls = [
            {'name':'ticketstake',
             'label':'子注单',
             'com':'com_ajax_table',
             'model':model_to_name(TbTicketstake),
             'relat_field':'ticketid',
             'kw': TicketstakeTable(crt_user=self.crt_user).get_head_context()},
            {'name':'ticketparlay',
             'label':'串关规则',
             'com':'com_ajax_table',
             'model':model_to_name(TbTicketparlay),
             'relat_field':'ticketid',
             'kw':TicketparlayTable(crt_user=self.crt_user).get_head_context()},                     
        ]
        ctx['tabs']=ls
        return ctx

    class tableCls(ModelTable):
        model = TbTicketmaster
        exclude = []
        fields_sort=['ticketid','account','stakeamount','betamount','parlayrule','status',
                     'winbet','createtime','betoutcome','turnover','bonuspa','bonus',
                     'settletime']
        
        def dict_head(self, head):
            if head['name'] in [ 'createtime','settletime']:
                head['width'] = 150
            else:
                head['width'] =80
                
            if head['name'] == 'account':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name']='ticketstake'  
                
            return head         

        #def dict_row(self, inst):
            #account_type = dict(ACCOUNT_TYPE)
            #return {
                #'amount':unicode(inst.amount),
                #'accounttype': account_type.get(inst.accounttype)
            #}

        class filters(RowFilter):
            range_fields=[{'name':'createtime','type':'date'},
                          {'name':'settletime','type':'date'}]
            

    
class TicketTabBase(ModelTable):
    def __init__(self, *args,**kws):
        ModelTable.__init__(self,*args,**kws)
        self.ticketid = self.kw.get('ticketid')
        
    def inn_filter(self, query):
        if self.ticketid:
            return query.filter(ticketid=self.ticketid) 
        else:
            return query

class TicketstakeTable(TicketTabBase):
    """ 子注单 """
    model = TbTicketstake
    exclude=[]
    fields_sort=['tid','matchid','specialbetvalue','odds','confirmodds','realodds','confirmoddsid_ori',
                 'status','createtime','updatetime']
    def dict_row(self, inst):
        match = TbMatches.objects.get(matchid =  inst.matchid)
        return {
            'matchid':{'label':'{tournamentzh} {team1zh}VS{team2zh}'.format(tournamentzh=match.tournamentzh,
                                                                   team1zh=match.team1zh,
                                                                   team2zh=match.team2zh),
                       'pk':match.pk
                    
                       }
        }
    def dict_head(self, head):
        dc={
            'tid':80,
            'matchid':250,
            'specialbetvalue':80,
            'odds':80,
            'confirmodds':80,
            'realodds':80,
            'confirmoddsid_ori':80,
            'status':80,
            'updatetime':150,
            'createtime':150,
          
        }
        if dc.get(head['name']):
            head['width'] =dc.get(head['name'])        
        
        if head['name']=='matchid':
            head['editor']='com-table-pop-fields'
            head['fields_heads']= MatchForm(crt_user=self.crt_user).get_heads()
            head['model_name']=model_to_name(TbMatches)
            head['ops']=[] #MatchForm(crt_user=self.crt_user).get_operations()
        return head
    
      

class TicketparlayTable(TicketTabBase):
    model=TbTicketparlay
    exclude=['tid','ticketid']
    
    def dict_head(self, head):
        if head['name'] == 'createtime':
            head['width'] = 150
        else:
            head['width'] =80
    
        return head    

    

class MatchForm(ModelFields):
    field_sort=['matchdate','team1zh','team2zh','matchscore','winner','statuscode','roundinfo'
                'livebet','generatedat','tournamentzh']
    readonly= field_sort
    
    class Meta:
        model=TbMatches
        exclude=[]
    def dict_row(self, inst):
        winner = inst.winner
        if inst.winner==1:
            winner = inst.team1zh 
        elif  inst.winner==2:
            winner = inst.team2zh 
        return {
            'winner':winner
        }
    
model_dc[TbTicketstake] = {'table':TicketstakeTable}
model_dc[TbTicketparlay] = {'table':TicketparlayTable}
model_dc[TbMatches] = {'fields':MatchForm}

    
