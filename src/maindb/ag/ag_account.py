from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch,RowSort,RawTable,director_view
from .. models import TbAgaccount
from helpers.func.dict_list import sort_by_name
from django.db.models import Sum
from helpers.director.model_func.dictfy import sim_dict,to_dict
from maindb.models import TbAccount,TbGamemoneyoutinfo
from django.utils import timezone
import time

class AgAccountPage(TablePage):
    def get_label(self):
        return '用户列表'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(RawTable):
        model = TbAgaccount
        exclude = ['fishavailablescores','lastfishupdatetime',]
        hide_fields=['accountid']
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
            names = self.get_model_field_name()
            fields = ','.join( ['main.%s'%x for x in names] )
            if where:
                sql = '''
                IF OBJECT_ID('tempdb..#tmp') IS NOT NULL
                BEGIN
                DROP TABLE #tmp;
                END;
                SELECT %(fields)s, TB_Account.NickName AS account__nickname
                INTO #tmp
                FROM TB_AgAccount main WITH (NOLOCK)
                INNER JOIN TB_Account WITH(NOLOCK) ON TB_Account.AccountID = main.AccountId
                %(where)s
    
                SELECT  * FROM #tmp main %(sort)s %(page)s;
                SELECT COUNT(1) as count FROM #tmp;
                SELECT SUM(winorloss) as winorloss,
                    SUM(transferin) as transferin,
                    SUM(transferout) AS transferout,
                    SUM(rebate) AS rebate,
                    SUM(availablescores) as availablescores FROM #tmp;
                '''%{'where':where,'sort':sort,'page':page,'fields':fields}
            else:
                sql ='''
                SELECT %(fields)s,TB_Account.NickName AS account__nickname FROM TB_AgAccount main WITH(NOLOCK) INNER JOIN TB_Account WITH( NOLOCK ) 
                ON TB_Account.AccountID = main.AccountId %(sort)s %(page)s;
                
                SELECT COUNT(1) as count FROM TB_AgAccount  WITH(NOLOCK);
                SELECT SUM(winorloss) as winorloss,
                    SUM(transferin) as transferin,
                    SUM(transferout) AS transferout,
                    SUM(rebate) AS rebate,
                    SUM(availablescores) as availablescores FROM TB_AgAccount WITH(NOLOCK);
                '''%{'where':where,'sort':sort,'page':page,'fields':fields}

            return sql

        def dict_row(self, row_dc):
            return {
                'pk':row_dc.get('accountid')
            }
        
        def get_operation(self):
            changeable_fields = self.permit.changeable_fields()
            return [
                {'fun':'selected_set_and_save','editor': 'com-op-btn','label':'打开资金开关','row_match':'many_row','pre_set':'rt={fundswitch:true}',
                 'confirm_msg':'确定要打开选中用户的资金开关?',
                 'visible': 'fundswitch' in changeable_fields},
                {'fun':'selected_set_and_save','editor': 'com-op-btn','label':'关闭资金开关','row_match':'many_row','pre_set':'rt={fundswitch:false}',
                  'confirm_msg':'确定要关闭选中用户的资金开关?',
                 'visible': 'fundswitch' in changeable_fields},
                {'label':'余额收回','editor':'com-op-btn','row_match':'many_row',
                 'confirm_msg':'确定要回收这些用户的余额?',
                 'visible':'availablescores' in changeable_fields,
                 'action':'var rows= ex.map(scope.ps.selected,(item)=>{return item.pk});cfg.show_load();ex.director_call("ag/redraw_left_money",{rows:rows}).then(()=>{cfg.hide_load();cfg.toast("提交成功")})'},
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
            #names = ['account__nickname','agusername']
            exact_names=['account__nickname','agusername','accountid',]
            db_map={
                'account__nickname':'TB_Account.NickName',
                'accountid':'main.AccountID',
            }
            def get_option(self, name):
                if name == 'accountid':
                    return {'value':name,'label':'账号ID'}
                elif name == 'account__nickname':
                    return {'value': name,
                                    'label': '用户昵称', }
                else:
                    return super().get_option(name)
        
        class sort(RowSort):
            names = ['transferin','transferout','winorloss','availablescores']
            general_sort ='-main.AccountId'

class AgAccountForm(ModelFields):
    class Meta:
        model = TbAgaccount
        exclude = []
        
@director_view('ag/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbAgaccount.objects.filter(accountid_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        out_list.append( TbGamemoneyoutinfo(account=inst.accountid,amount=inst.availablescores,status=0,username=inst.agusername,ordertime=now,orderid=orderid) )
    TbGamemoneyoutinfo.objects.bulk_create(out_list)

director.update({
    'agaccount':AgAccountPage.tableCls,
    'agaccount.edit':AgAccountForm
})

page_dc.update({
    'agaccount':AgAccountPage
})