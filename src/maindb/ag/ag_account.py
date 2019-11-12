from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch,RowSort,RawTable
from .. models import TbAgaccount
from helpers.func.dict_list import sort_by_name
from django.db.models import Sum
from helpers.director.model_func.dictfy import sim_dict,to_dict
from maindb.models import TbAccount

class AgAccountPage(TablePage):
    def get_label(self):
        return '用户列表'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(RawTable):
        model = TbAgaccount
        exclude = ['fishavailablescores','lastfishupdatetime','account']
        db ='Sports'
        def getExtraHead(self):
            return [
                {'name':'account__nickname','label':"账号昵称",}
            ]
        
        def get_sql(self):
            
            where = self.get_where()
            sort = self.get_sort()
            start,end = self.pagenum.get_slice_index()
            page ='OFFSET %(start)s ROWS  FETCH NEXT %(pagesize)s ROWS ONLY'%{'start':start,'pagesize':self.pagenator.perPage}
      
            sql = '''
            IF OBJECT_ID('tempdb..#tmp') IS NOT NULL
            BEGIN
            DROP TABLE #tmp;
            END;
            SELECT TB_AgAccount.*, TB_Account.NickName AS account__nickname
            INTO #tmp
            FROM TB_AgAccount WITH ( NOLOCK )
            INNER JOIN TB_Account ON TB_Account.AccountID = TB_AgAccount.AccountId
            %(where)s

            SELECT  * FROM #tmp %(sort)s %(page)s;
            SELECT COUNT(1) as count FROM #tmp;
            SELECT SUM(winorloss) as winorloss,
                SUM(transferin) as transferin,
                SUM(transferout) AS transferout,
                SUM(rebate) AS rebate,
                SUM(availablescores) as availablescores FROM #tmp;
            '''%{'where':where,'sort':sort,'page':page}
            return sql
        
        def inject_sql(self):
            
            self.sql = 'SELECT TB_AgAccount.* , TB_Account.Nickname as account__nickname FROM TB_AgAccount with(nolock) INNER JOIN TB_Account with(nolock) ON TB_Account.AccountID=TB_AgAccount.AccountID'
            search_args = self.kw.get('search_args')
            
            if search_args.get('_q'):
                value = search_args.get('_q')
                if search_args.get('_qf') =='account__nickname':
                    self.sql += " WHERE TB_Account.Nickname like %s "
                    self.params.append('%s%%'%value)
                elif search_args.get('_qf') =='account':
                    self.sql += r' WHERE TB_Account.AccountID =%s'%value
                elif search_args.get('_qf') =='agusername':
                    self.sql += ' WHERE TB_AgAccount.agusername = %s '
                    self.params.append(value)
            if search_args.get('_sort'):
                if search_args.get('_sort').startswith('-'):
                    self.order_by = ' ORDER BY %s DESC '%search_args.get('_sort')[1:] 
                else:
                    self.order_by = ' ORDER BY %s'%search_args.get('_sort')
        
        
        def get_operation(self):
            return [
                {'fun':'selected_set_and_save','editor': 'com-op-btn','label':'打开资金开关','row_match':'many_row','pre_set':'rt={fundswitch:true}',
                 'confirm_msg':'确定要打开选中用户的资金开关?',
                 'visible': 'fundswitch' in self.permit.changeable_fields()},
                {'fun':'selected_set_and_save','editor': 'com-op-btn','label':'关闭资金开关','row_match':'many_row','pre_set':'rt={fundswitch:false}',
                  'confirm_msg':'确定要关闭选中用户的资金开关?',
                 'visible': 'fundswitch' in self.permit.changeable_fields()},
            ]
        
        def dict_head(self, head):
            width={
                'account__nickname':150,
                'agusername':150,
                'transferin':140,
                'transferout':140,
                'winorloss':140,
                'availablescores':140,
                'rebate':140,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            if head['name'] =='account':
                head['label'] = '用户ID'
                head['editor'] = 'com-table-span'
            return head
                
        
        def dict_row(self, inst):
            return {
                'account':inst.account_id,
                'account__nickname':inst.account__nickname
                #'account__nickname':inst.account.nickname,
            }
        
        def get_heads(self):
            heads = super().get_heads()
            heads = sort_by_name(heads,['account','account__nickname']) 
            return heads
        
        def get_foot_sql(self):
            return ''' 
            SELECT SUM(winorloss) as winorloss,
                   SUM(transferin) as transferin,
                   SUM(transferout) AS transferout,
                   SUM(rebate) AS rebate,
                   SUM(availablescores) as availablescores FROM (''' +self.sql +') bba'
        
        #def _statistics(self, query):
            #st_query = TbAgaccount.objects.raw(''' 
            #SELECT SUM(winorloss) as total_winorloss,
                   #SUM(transferin) as total_transferin,
                   #SUM(transferout) AS total_transferout,
                   #SUM(rebate) AS total_rebate,
                   #SUM(availablescores) as total_availablescores FROM (''' +self.sql +') bba',self.params )
            ##dc = query.aggregate(total_winorloss=Sum('winorloss'),
                                 ##total_transferin=Sum('transferin'),
                                 ##total_transferout=Sum('transferout'),
                                 ##total_rebate=Sum('rebate'),
                                 ##total_availablescores=Sum('availablescores'))
            #mapper = {
                #'total_winorloss': 'winorloss' ,
                #'total_transferin':'transferin',
                #'total_transferout':'transferout',
                #'total_rebate':'rebate',
                #'total_availablescores':'availablescores'
            #}

            #normed_dc = {mapper.get(k): v for (k, v) in dc.items()}
            #normed_dc.update({
                #'_label':'合计'
            #})
            #self.footer = normed_dc
            #return query
       
        
        class search(SelectSearch):
            names = ['account__nickname','agusername']
            exact_names=['account']
            db_map={
                'account__nickname':'TB_Account.NickName'
            }
            def get_option(self, name):
                if name == 'account':
                    return {'value':name,'label':'账号ID'}
                elif name == 'account__nickname':
                    return {'value': name,
                                    'label': '用户昵称', }
                else:
                    return super().get_option(name)
        
        class sort(RowSort):
            names = ['transferin','transferout','winorloss','availablescores']
            general_sort ='-AccountId'

class AgAccountForm(ModelFields):
    class Meta:
        model = TbAgaccount
        exclude = []
        


director.update({
    'agaccount':AgAccountPage.tableCls,
    'agaccount.edit':AgAccountForm
})

page_dc.update({
    'agaccount':AgAccountPage
})