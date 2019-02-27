from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,RowFilter,RowSearch,RowSort
from ..models import TbAccount
from django.utils import timezone
from django.db import connections
from ..member.account import UserRecharge,account_tab



class RechargeReport(TablePage):
    def get_label(self):
        return '充值统计'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid']
        
        class search(RowSearch):
            names = ['accountid']
         
        
        class filters(RowFilter):
            range_fields = ['date']
    
            def getExtraHead(self):
                return [
                    {'name':'date','editor':'com-filter-datetime-range','label':'时间'}
                ]        
        
        class sort(RowSort):
            names = ['RequestAmount','DangerLevel','RequestTotal','FinishTotal','FinishAmount','UseCardTotal','OnlineTotal']        
        
        @classmethod
        def clean_search_args(cls, search_args):
            if not search_args.get('_has_default'):
                today = timezone.now()
                sp = timezone.timedelta(days=30)
                last = today - sp
                def_start = last.strftime('%Y-%m-%d 00:00:00')
                def_end = today.strftime('%Y-%m-%d %H:%M:%S')                
                search_args['_start_date'] = search_args.get('_start_date') or def_start
                search_args['_end_date'] = search_args.get('_end_date') or def_end
                search_args['_has_default'] =1
                
            return search_args        
        
        def get_context(self):
            ctx = super().get_context()
            ctx['named_ctx'] =  {
                'recharge_tabs':[{'name': 'UserRecharge',
                                 'label': '充值记录',
                                 'com': 'com-tab-table',
                                 'par_field': 'accountid',
                                 'table_ctx': UserRecharge(crt_user=self.crt_user).get_head_context(),
                                 'visible': True #can_touch(TbRecharge, self.crt_user),
                    }]
            }
            ctx['named_ctx'] .update( account_tab(self))
            return ctx
        
        def getExtraHead(self):
            return [
                {'name': 'Account', 'label': '账号 ', 'width': 150,'editor':'com-table-switch-to-tab','ctx_name':'recharge_tabs','tab_name':'UserRecharge'},
                {'name': 'DangerLevel', 'label': '用户安全等级', 'width': 100,'editor':'com-table-style-block', 'style_express':"""
                var style_map={'高危':'background-color:red;color:white;'};
                rt=style_map[scope.row.DangerLevel]
                """},
                {'name': 'FinishPer', 'label': '充值完成率', 'width': 100},
                
                {'name': 'RequestTotal', 'label': '申请充值次数', 'width': 100},
                {'name': 'FinishTotal', 'label': '完成充值次数', 'width': 100},
                         
                {'name': 'RequestAmount', 'label': '申请充值金额', 'width': 100},
                                         
                {'name': 'FinishAmount', 'label': '完成充值金额', 'width': 100},
                {'name': 'UseCardTotal', 'label': '转卡充值次数', 'width': 100},
                
                {'name': 'OnlineTotal', 'label': '第三方充值次数', 'width': 100},
                                           
            ]    
        
        def get_rows(self):
            self.getData()
            for row in self.data_rows:
                row['accountid'] = row['AccountID']
                #row['Amount'] = round(row['Amount'], 2)
                #row['BetAmount'] = round(row['BetAmount'], 2)
                #row['Turnover'] = round(row['Turnover'], 2)
                #row['BetOutcome'] = round(row['BetOutcome'], 2)
                #row['BetBonus'] = round(row['BetBonus'], 2)
                #row['FirstRechargeBonus'] = round(row['FirstRechargeBonus'], 2)
                #row['SecondRechargeBonus'] = round(row['SecondRechargeBonus'], 2)
                #row['RescueBonus'] = round(row['RescueBonus'], 2)
                #row['BirthdayBonus'] = round(row['BirthdayBonus'], 2)
                #row['AdjustAmount'] = round(row['AdjustAmount'], 2)
                #row['Profit'] = round(row['Profit'], 2)
                #row['GameCoinRechargeAmount'] = round(row['GameCoinRechargeAmount'], 2)
                #row['CommissionRechargeAmount'] = round(row['CommissionRechargeAmount'], 2)
                #row['ReservedAmount'] = round(row['ReservedAmount'], 2)
                #row['CommissionWithDrawAmount'] = round(row['CommissionWithDrawAmount'], 2)
            return self.data_rows  
        
        def getData(self):
            #nickname = ""
            #if self.search_args.get('_qf') == 'nickname':
                #nickname = self.search_args.get('_q', '')
            #sort = self.search_args.get('_sort') or '-Profit'
            #sortway = 'asc'
            #if sort.startswith('-'):
                #sort = sort[1:]
                #sortway = 'desc'
 
            #sort_dc = {
                #'FirstRechargeBonus':'1stRCBonus',
                #'SecondRechargeBonus':'2ndRCBonus',
                #'RescueBonus':'Rescue',
                #'BirthdayBonus':'BdBonus',
                #'GameCoinRechargeAmount': 'GameRCAmt',
                #'CommissionRechargeAmount':'CommRCAmt',
                #'CommissionWithDrawAmount':'CommWDAmt',
                #'ReservedAmount':'RvAmt',
                #'AdjustAmount':'AdjAmount'
            #}
            realsort = self.search_args.get('_sort') or 'NULL' #sort_dc.get(sort) or sort;
            order_d = 'Desc' if realsort.startswith('-') else 'Asc'
            realsort = realsort[1:] if realsort.startswith('-') else realsort
            AccountID = self.search_args.get('_q') or 'NULL'
            sql_args = {
                'AccountID':AccountID,
                'StartTime': self.search_args.get('_start_date', ''),
                'EndTime': self.search_args.get('_end_date', ''),
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'Sort': realsort,
                'order_d':order_d,
                #'SortWay': sortway,
                #'AccountType':self.search_args.get('AccountType','-1'),
            }
            sql = r"EXEC SP_RechargeMonitor '%(StartTime)s','%(EndTime)s',%(AccountID)s,%(PageIndex)s,%(PageSize)s,'%(Sort)s','%(order_d)s'" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                set0 = cursor.fetchall()
                self.total = set0[0][0]
 
                #footer = {}
                #for col_data, col in zip(set0[0], cursor.description):
                    #head_name = col[0]
                    #if head_name.startswith('Sum'):
                        #head_name = head_name[3:]
                    #footer[head_name] = round(col_data, 2)
                #self.footer = ['合计'] + self.footer_by_dict(footer)
 
                cursor.nextset()
                self.data_rows = []
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    self.data_rows.append(dc)
            
        def getRowPages(self):
            return {
                'crt_page': self.search_args.get('_page', 1),
                'total': self.total,
                'perpage': self.search_args.get('_perpage', 20)
            }            

director.update({
    'recharge_reports':RechargeReport.tableCls,
})

page_dc.update({
    'recharge_reports':RechargeReport,
})