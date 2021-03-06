# encoding:utf-8
from __future__ import unicode_literals
from django.db import connections
from helpers.director.shortcut import ModelTable, TablePage, page_dc, RowSort, RowFilter
from helpers.director.table.row_search import SelectSearch
from ..models import TbAccount
from helpers.director.base_data import director
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from helpers.director.access.permit import has_permit
from helpers.func.sql import qn
from helpers.director.network import argument


class UserStatisticsPage(TablePage):
    template = 'jb_admin/table.html'

    def check_permit(self): 
        if not has_permit(self.crt_user, 'member_statistic'):
            raise PermissionDenied('没有权限访问会员统计页面')
        
    def get_label(self):
        return '会员统计'

    def get_context(self):
        from ..member.account import account_tab
        ctx = super().get_context()
        ctx['named_ctx'] = account_tab(self)
        return ctx
    
    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid','date']
        
        def dict_head(self, head):
            if head['name']=='accountid':
                head['fixed']=True
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'dashborad'
                head['ctx_name'] = 'account_tabs'
            if head['name'] =='GroupName':
                head['inn_editor'] = head['editor']
                head['editor'] = 'com-table-rich-span'
                head['style'] = 'if(scope.vc.light_level(scope.row.Extension) > 192){var mycolor="black"}else{var mycolor="white"};rt={background:scope.row.Extension,color:mycolor}'
            return head
        
        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d 00:00:00')
            def_end = today.strftime('%Y-%m-%d 23:59:59')
            if search_args.get('_first_access',1):
                search_args['_start_date'] = search_args.get('_start_date') or def_start
                search_args['_end_date'] = search_args.get('_end_date') or def_end
                search_args['AccountType'] = search_args.get('AccountType',0)
                search_args['_first_access'] = 0
            argument.validate_argument(search_args,{
                '_start_date':[argument.failmsg(argument.not_null,'必须输入开始日期'),],
                '_end_date':[argument.failmsg(argument.not_null,'必须输入结束日期')],
                'minAmount':[argument.null_break, argument.failmsg(argument.float_str,'投注金额输入格式不正确')],
                'MinProfit':[argument.null_break,argument.failmsg(argument.float_str,'亏盈输入格式不正确')]
            })
            
            #if not search_args.get('_start_date') :
                #raise UserWarning('必须输入开始日期')
            #if not search_args.get('_end_date'):
                #raise UserWarning('必须输入结束日期')
            #if 'minAmount' in search_args and search_args.get('minAmount').strip():
                #try:
                    #float(search_args.get('minAmount'))
                #except ValueError:
                    #raise UserWarning('投注金额输入格式不正确!')
            #if 'MinProfit' in search_args and search_args.get('MinProfit').strip():
                #try:
                    #float(search_args.get('MinProfit'))
                #except ValueError:
                    #raise UserWarning('亏盈输入格式不正确!')
                    
            return search_args

        class search(SelectSearch):
            names = ['nickname']

            def get_option(self, name):
                if name == 'nickname':
                    return {'value': 'nickname', 'label': '用户昵称', }
                else:
                    return super().get_option(name)

        class filters(RowFilter):
            range_fields = ['date']

            def getExtraHead(self):
                #return [{'name':'date','editor':'com-date-range-filter','label':'日期'}]
                
                return [
                    {'name':'minAmount','label':'投注金额大于等于','editor':'com-filter-text'},
                    {'name':'MinProfit','label':'亏盈大于等于','editor':'com-filter-text'},
                    {'name':'AccountType','label':'用户类型','editor':'com-filter-select','options':[
                        {'label':'普通用户','value':0},
                        {'label':'代理用户','value':1},
                        ]},
                    {'name':'date','editor':'com-filter-datetime-range','label':'时间'},
                ]

        class sort(RowSort):
            names = ['Amount', 'GameCoinRechargeAmount', 'CommissionRechargeAmount', 'ReservedAmount',
                     'CommissionWithDrawAmount', 'BetAmount', 'Turnover', 'BetOutcome', 'BetBonus', 'OrderCount',
                     'WinCount', 'WinRate', 'FirstRechargeBonus', 'SecondRechargeBonus', 'RescueBonus', 'BirthdayBonus',
                     'AdjustAmount', 'Profit','ProfitRate','WinDayRate','WinDay','TotalDay']
            
        def get_rows(self):
            self.getData()
            for row in self.matches:
                row['accountid'] = row['AccountID']
                row['_label'] = row['NickName']
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
                'minAmount':self.search_args.get('minAmount') or -10**10,
                'MinProfit':self.search_args.get('MinProfit') or -10**10,
            }
            sql = r"exec dbo.SP_UserStatistics %%s,%(AccountID)s,'%(StartTime)s','%(EndTime)s',%(PageIndex)s,%(PageSize)s,'%(Sort)s','%(SortWay)s','%(AccountType)s',%(minAmount)s,%(MinProfit)s" \
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
                footer.update({
                    '_label':'合计'
                })
                self.footer =  footer # ['合计'] + self.footer_by_dict(footer)

                cursor.nextset()
                self.matches = []
                for row in cursor:
                    dc = {}
                    for index, head in enumerate(cursor.description):
                        dc[head[0]] = row[index]
                    self.matches.append(dc)

        def getExtraHead(self):
            return [
                {'name': 'NickName', 'label': '昵称 ', 'width': 150,'fixed':True},
                {'name':'GroupName','label':'用户组','width':100,},
                {'name': 'Profit', 'label': '亏盈', 'width': 100,},
                {'name': 'WinRate', 'label': '中注率', 'width': 100},
                {'name':'ProfitRate','label':'亏盈率','width':120},
                {'name': 'BetAmount', 'label': '投注金额', 'width': 130},
                {'name': 'BetOutcome', 'label': '派奖金额', 'width': 100},
                {'name': 'AdjustAmount', 'label': '调账', 'width': 100},
                {'name': 'Amount', 'label': '余额', 'width': 130},
                {'name': 'GameCoinRechargeAmount', 'label': '充值金额', 'width': 130},
                {'name': 'CommissionRechargeAmount', 'label': '佣金充值金额', 'width': 130},
                {'name': 'ReservedAmount', 'label': '提现金额', 'width': 130},
                {'name': 'CommissionWithDrawAmount', 'label': '佣金提现金额', 'width': 130},
                
                {'name': 'Turnover', 'label': '流水', 'width': 100},
                
                {'name': 'BetBonus', 'label': '返水', 'width': 100},
                {'name': 'OrderCount', 'label': '注数', 'width': 100},
                {'name': 'WinCount', 'label': '中注数', 'width': 100},
               
              
                {'name': 'FirstRechargeBonus', 'label': '首存红利', 'width': 100},
                {'name': 'SecondRechargeBonus', 'label': '再存红利', 'width': 100},
                {'name': 'RescueBonus', 'label': '救援金', 'width': 100},
                {'name': 'BirthdayBonus', 'label': '生日礼金', 'width': 100},
                {'name':'WinDayRate','label':'盈利天数率','width':100},
                {'name':'WinDay','label':'盈利天数'},
                {'name':'TotalDay','label':'投注天数'},
                #{'name':'VoidRate','label':'划单率'},
                
            ]

        def getRowPages(self):
            return {
                'crt_page': self.search_args.get('_page', 1),
                'total': self.total,
                'perpage': self.search_args.get('_perpage', 20)
            }
        
        def get_operation(self): 
            return [
                {'fun': 'export_excel','editor': 'com-op-btn','label': '导出Excel','icon': 'fa-file-excel-o',}
            ]


director.update({
    'UserStatisticsPage': UserStatisticsPage.tableCls
})

page_dc.update({
    'user_statistics': UserStatisticsPage
})
