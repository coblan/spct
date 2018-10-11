from helpers.director.shortcut import ModelTable, TablePage, page_dc, director, RowFilter, RowSort, RowSearch
from helpers.director.table.row_search import SelectSearch
from ..models import TbAccount
from django.db import connections
from django.utils import timezone
from ..member.account import account_tab


class AgentUser(TablePage):
    template = 'jb_admin/table.html'
    def check_permit(): 
        pass
    
    def get_label(self):
        return '代理用户'

    class tableCls(ModelTable):
        model = TbAccount
        include = ['accountid','createtime']
        fields_sort = ['accountid', 'NickName', 'SumActive', 'AgentAmount', 'BeaeAmount', 'AgentRuleAmount',
                       'BalanceLostAmount', 'SumLostAmount', 'BonusRate', 'SumBonusAmount', 'SumExpend',
                       'SumRechargeAmount', 'Poundage', 'AgentRulePercentage', 'SumBetAmount', 'SumWithdrawalAmount',
                       'SumTurnover', 'CreateTime']

        @classmethod
        def clean_search_args(cls, search_args):
            today = timezone.now()
            sp = timezone.timedelta(days=30)
            last = today - sp
            def_start = last.strftime('%Y-%m-%d')
            def_end = today.strftime('%Y-%m-%d')
            search_args['_start_createtime'] = search_args.get('_start_createtime') or def_start
            search_args['_end_createtime'] = search_args.get('_end_createtime') or def_end
            return search_args

        class filters(RowFilter):
            range_fields = ['createtime']

            def dict_head(self, head):
                if head['name'] == 'createtime':
                    head['label'] = '产生时间'
                return head

        class sort(RowSort):
            names = ['AgentAmount', 'BeaeAmount', 'SumActive', 'AgentRuleAmount', 'BalanceLostAmount', 'SumLostAmount',
                     'SumBonusAmount', 'SumWithdrawalAmount', 'SumBetAmount', 'Poundage',
                     'SumTurnover', 'BonusRate', 'SumExpend', 'SumRechargeAmount', 'AgentRulePercentage']

        class search(SelectSearch):
            names = ['nickname']

            def get_option(self, name):
                if name == 'nickname':
                    return {'value': 'nickname', 'label': '用户昵称', }
                else:
                    return super().get_option(name)

        def getData(self):
            """
            @AccountID INT,    --用户编号  
            @PageIndex INT =1,    --页码   默认1  
            @PageSize INT =10,    --页条数 默认10  
            @BeginDate DATE=NULL,   --查询开始时间 默认上月今天  
            @EndDate DATE=NULL,   --查询结算时间 默认今天  
            @NickName VARCHAR(20) =NULL --帐号查询昵称 默认全部  
            """

            order_by = self.search_args.get('_sort', '')
            par = self.search_args.get('_par', 0)
            nickname = self.search_args.get('_q', '')

            cach_par = self.search_args.get('_cach_par')
            cach_nickname = self.search_args.get('_cach_nickname')
            cach_sort = self.search_args.get('_cach_sort')

            self.search_args['_cach_nickname'] = nickname
            self.search_args['_cach_par'] = par
            self.search_args['_cach_sort'] = order_by
            if par != cach_par:
                # 点击的par
                nickname = ''
                order_by = ''
                self.search_args['_cach_op'] = 'click_par'

            elif nickname and cach_nickname != nickname:
                # 搜索昵称，第一次点击[搜索]
                par = 0
                order_by = ''
                self.search_args['_cach_op'] = 'search_nickname'
            elif order_by != cach_sort:
                # 排序
                cach_op = self.search_args.get('_cach_op')
                if cach_op == 'click_par':
                    nickname = ''
                elif cach_op == 'search_nickname':
                    par = 0
            else:
                # 点击 [搜索] 刷新
                pass

            if order_by.startswith('-'):
                order_by = order_by[1:] + ' DESC'
            sql_args = {
                'AccountID': par,
                'PageIndex': self.search_args.get('_page', 1),
                'PageSize': self.search_args.get('_perpage', 20),
                'BeginDate': self.search_args.get('_start_createtime', ''),
                'EndDate': self.search_args.get('_end_createtime', ''),
                'NickName': nickname,
                'OrderBy': order_by,
            }

            sql = "exec dbo.SP_AgentUser %(AccountID)s,%(PageIndex)s,%(PageSize)s,'%(BeginDate)s','%(EndDate)s','%(NickName)s','%(OrderBy)s'" \
                  % sql_args

            with connections['Sports'].cursor() as cursor:
                cursor.execute(sql)
                # cursor.commit()
                self.parent_agents = []
                for par in cursor:
                    self.parent_agents.append({'value': par[3], 'label': par[1], })
                self.parent_agents.append({'value': 0, 'label': '根用户', })
                self.parent_agents.reverse()

                cursor.nextset()
                self.child_agents = []
                for row in cursor:
                    dc = {}
                    for index, desp_item in enumerate(cursor.description):
                        head_name = desp_item[0]
                        dc[head_name] = row[index]
                    self.child_agents.append(dc)
                if self.child_agents:
                    row1 = self.child_agents[0]
                    footer = {}
                    for k, v in row1.items():
                        if k != 'Total' and k.startswith('Total'):
                            footer[k[5:]] = round(v, 2)
                    self.footer = ['合计'] + self.footer_by_dict(footer)
            # 保持 _par参数为空状态，可以判断 前端操作是 搜索or点击

        def dict_head(self, head):
            if head['name'] == 'SumActive':
                head['editor'] = 'com-table-call-fun'
                head['fun'] = 'get_childs'
                head['field'] = 'accountid'
            if head['name'] == 'accountid':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'baseinfo'
            return head

        def getExtraHead(self):
            return [
                # {'name': 'accountid', 'label': '账号ID ', 'width': 100, },
                {'name': 'NickName', 'label': '昵称 ', 'width': 100, },
                # {'name': 'VIPLv', 'label': 'VIP等级', },
                {'name': 'SumActive', 'label': '活跃用户数', 'width': 100, },
                {'name': 'AgentAmount', 'label': '预估佣金', },
                {'name': 'BeaeAmount', 'label': '佣金计算基数', 'width': 120, },
                {'name': 'AgentRuleAmount', 'label': '佣金计算金额', 'width': 120, },
                {'name': 'BalanceLostAmount', 'label': '累计净盈利', 'width': 100, },
                {'name': 'SumLostAmount', 'label': '本月净盈利', 'width': 100, },
                {'name': 'BonusRate', 'label': '返水比例', },
                {'name': 'SumBonusAmount', 'label': '返水', 'width': 80, },
                {'name': 'SumExpend', 'label': '系统红利', 'width': 80, },
                {'name': 'SumRechargeAmount', 'label': '充值金额', 'width': 100, },
                {'name': 'Poundage', 'label': '充值手续费', 'width': 100, },
                {'name': 'AgentRulePercentage', 'label': '佣金比例', },
                {'name': 'SumBetAmount', 'label': '投注金额', 'width': 120, },
                {'name': 'SumWithdrawalAmount', 'label': '提现金额', 'width': 100, },
                {'name': 'SumTurnover', 'label': '流水', 'width': 120, },
                {'name': 'CreateTime', 'label': '创建时间', 'width': 140, },
            ]

        def get_rows(self):
            self.getData()
            for row in self.child_agents:
                row['accountid'] = row['AccountID']
                row['NickName'] = row['NickName']
                row['BeaeAmount'] = round(row['BeaeAmount'], 2)
                row['BonusRate'] = round(row['BonusRate'], 3)
                row['Poundage'] = round(row['Poundage'], 2)
                row['AgentRuleAmount'] = round(row['AgentRuleAmount'], 2)
                row['BalanceLostAmount'] = round(row['BalanceLostAmount'], 2)
                row['AgentAmount'] = round(row['AgentAmount'], 2)
                row['SumExpend'] = round(row['SumExpend'], 2)
                row['AgentRulePercentage'] = round(row['AgentRulePercentage'], 3)
                row['SumLostAmount'] = round(row['SumLostAmount'], 2)
                row['SumBonusAmount'] = round(row['SumBonusAmount'], 2)
                row['SumBetAmount'] = round(row['SumBetAmount'], 2)
                row['SumRechargeAmount'] = round(row['SumRechargeAmount'], 2)
                row['SumWithdrawalAmount'] = round(row['SumWithdrawalAmount'], 2)
                row['SumTurnover'] = round(row['SumTurnover'], 2)

            return self.child_agents

        def getRowPages(self):
            if self.child_agents:
                total = self.child_agents[0]['Total']
            else:
                total = 0

            return {
                'crt_page': self.search_args.get('_page', 1),
                'total': total,
                'perpage': self.search_args.get('_perpage', 20)
            }

        # def get_context(self):
        # ctx = super().get_context()
        # ctx['parents'] = self.parent_agents
        # return ctx

        def getParents(self):
            return self.parent_agents

        def get_context(self):
            ctx = super().get_context()
            ctx['tabs'] = account_tab(self)
            return ctx

        def get_operation(self):
            return [
                {'fun': 'export_excel', 'editor': 'com-op-btn', 'label': '导出Excel', 'icon': 'fa-file-excel-o', }
            ]


director.update({
    'AgentUser': AgentUser.tableCls,
})

page_dc.update({
    'agent_user': AgentUser,
})
