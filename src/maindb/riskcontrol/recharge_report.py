from helpers.director.shortcut import TablePage,ModelTable
from ..models import TbAccount

class RechargeReport(TablePage):
    def get_label(self):
        return '充值统计'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid']
        
        def getExtraHead(self):
            return [
                {'name': 'Account', 'label': '账号 ', 'width': 150},
                {'name': 'RequestTotal', 'label': '请求次数', 'width': 100},
                {'name': 'FinishTotal', 'label': '完成次数', 'width': 100},
                         
                {'name': 'RequestAmount', 'label': '请求数量', 'width': 100},
                                         
                {'name': 'FinishAmount', 'label': '完成数量', 'width': 100},
                {'name': 'UseCardTotal', 'label': '用卡次数', 'width': 100},
                
                {'name': 'OnlineTotal', 'label': '在线次数', 'width': 100},
                {'name': 'FinishAmount', 'label': '完成数量', 'width': 100},
                {'name': 'FinishPer', 'label': '完成率', 'width': 100},
                {'name': 'DangerLevel', 'label': '安全等级', 'width': 100},
                                                        
            ]    
        
        def get_rows(self):
            self.getData()
            for row in self.matches:
                row['accountid'] = row['AccountID']
                row['Amount'] = round(row['Amount'], 2)
                row['BetAmount'] = round(row['BetAmount'], 2)
                row['Turnover'] = round(row['Turnover'], 2)
                row['BetOutcome'] = round(row['BetOutcome'], 2)
                row['BetBonus'] = round(row['BetBonus'], 2)
                row['FirstRechargeBonus'] = round(row['FirstRechargeBonus'], 2)
                row['SecondRechargeBonus'] = round(row['SecondRechargeBonus'], 2)
                row['RescueBonus'] = round(row['RescueBonus'], 2)
                row['BirthdayBonus'] = round(row['BirthdayBonus'], 2)
                row['AdjustAmount'] = round(row['AdjustAmount'], 2)
                row['Profit'] = round(row['Profit'], 2)
                row['GameCoinRechargeAmount'] = round(row['GameCoinRechargeAmount'], 2)
                row['CommissionRechargeAmount'] = round(row['CommissionRechargeAmount'], 2)
                row['ReservedAmount'] = round(row['ReservedAmount'], 2)
                row['CommissionWithDrawAmount'] = round(row['CommissionWithDrawAmount'], 2)
            return self.matches  
        
        def getData(self):
            nickname = ""
            if self.search_args.get('_qf') == 'nickname':
                nickname = self.search_args.get('_q', '')
            sort = self.search_args.get('_sort') or '-Profit'
            sortway = 'asc'
            if sort.startswith('-'):
                sort = sort[1:]
                sortway = 'desc'
 
            sort_dc = {
                'FirstRechargeBonus':'1stRCBonus',
                'SecondRechargeBonus':'2ndRCBonus',
                'RescueBonus':'Rescue',
                'BirthdayBonus':'BdBonus',
                'GameCoinRechargeAmount': 'GameRCAmt',
                'CommissionRechargeAmount':'CommRCAmt',
                'CommissionWithDrawAmount':'CommWDAmt',
                'ReservedAmount':'RvAmt',
                'AdjustAmount':'AdjAmount'
            }
            realsort = sort_dc.get(sort) or sort;
            AccountID = self.kw.get('accountid') or 0
            sql_args = {
                'NickName': qn(nickname),
                'AccountID':AccountID,
                'StartTime': self.search_args.get('_start_date', ''),
                'EndTime': self.search_args.get('_end_date', ''),
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'Sort': realsort,
                'SortWay': sortway,
                'AccountType':self.search_args.get('AccountType','-1'),
            }
            sql = r"exec dbo.SP_UserStatistics %%s,%(AccountID)s,'%(StartTime)s','%(EndTime)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s','%(SortWay)s','%(AccountType)s'" \
                  % sql_args
            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql, [nickname])
                set0 = cursor.fetchall()
                self.total = set0[0][0]
 
                footer = {}
                for col_data, col in zip(set0[0], cursor.description):
                    head_name = col[0]
                    if head_name.startswith('Sum'):
                        head_name = head_name[3:]
                    footer[head_name] = round(col_data, 2)
                self.footer = ['合计'] + self.footer_by_dict(footer)
 
                cursor.nextset()
                self.matches = []
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    self.matches.append(dc)
         