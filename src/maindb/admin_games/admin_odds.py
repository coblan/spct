# encoding:utf-8

from helpers.director.shortcut import TablePage, ModelTable, page_dc
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from ..models import TbMatches

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
  
        ls = [
            {'name':'balance_log',
             'label':'Balance Log',
             'com':'com_odds_editor',
             'row': [],
             'get_data':{
                 'fun': 'do_not',
                 #'fun':'get_rows',
                 #'kws':{
                    #'director_name':AccountBalanceTable.get_director_name() ,# model_to_name(TbBalancelog),
                    #'relat_field':'accountid',
                 #}
                 
             },
             'table_ctx':OddsTable(crt_user= self.crt_user).get_head_context()  #AccountBalanceTable(crt_user=self.crt_user).get_head_context(), 
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
    



page_dc.update({
    'maindb.TbOdds': OddsPage,
})