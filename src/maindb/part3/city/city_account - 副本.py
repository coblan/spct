from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch,ModelFields,director_view
from ..ag.ag_account import AgAccountPage
from maindb.models import TbLcityaccount,TbLcitymoneyoutinfo
from django.utils import timezone
import time

class LCityAccountPage(TablePage):
    def get_label(self):
        return '龙城账号'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(AgAccountPage.tableCls):
        model = TbLcityaccount
        exclude =[]
        redraw_left_money_director = 'city/redraw_left_money'
        
        def get_sql(self):
            where = self.get_where()
            sort = self.get_sort()
            start,end = self.pagenum.get_slice_index()
            page ='OFFSET %(start)s ROWS  FETCH NEXT %(pagesize)s ROWS ONLY'%{'start':start,'pagesize':self.pagenum.perPage}
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
                FROM TB_LCityAccount main WITH (NOLOCK)
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
                SELECT %(fields)s,TB_Account.NickName AS account__nickname FROM TB_LCityAccount main WITH(NOLOCK) INNER JOIN TB_Account WITH( NOLOCK ) 
                ON TB_Account.AccountID = main.AccountId %(sort)s %(page)s;
                
                SELECT COUNT(1) as count FROM TB_LCityAccount  WITH(NOLOCK);
                SELECT SUM(winorloss) as winorloss,
                    SUM(transferin) as transferin,
                    SUM(transferout) AS transferout,
                    SUM(rebate) AS rebate,
                    SUM(availablescores) as availablescores FROM TB_LCityAccount WITH(NOLOCK);
                '''%{'where':where,'sort':sort,'page':page,'fields':fields}

            return sql
        
        class search(AgAccountPage.tableCls.search):
            exact_names = ['account__nickname','username']
            #exact_names=['account']
            
            #def get_option(self, name):
                #if name == 'account':
                    #return {'value':name,'label':'账号ID'}
                #elif name == 'account__nickname':
                    #return {'value': name,
                                    #'label': '用户昵称', }
                #else:
                    #return super().get_option(name)
        

class LCityAccountForm(ModelFields):
    class Meta:
        model = TbLcityaccount
        exclude =[]


@director_view('city/redraw_left_money')
def redraw_left_money(rows):
    out_list =[]
    now = timezone.now()
    start = int(time.time() *100000)
    for inst in TbLcityaccount.objects.filter(accountid_id__in=rows):
        start += 1
        orderid = 'B%s'%start
        if inst.availablescores >=1:
            out_list.append( TbLcitymoneyoutinfo(account=inst.accountid,amount= int( inst.availablescores),status=0,username=inst.username,ordertime=now,orderid=orderid) )
    TbLcitymoneyoutinfo.objects.bulk_create(out_list)


director.update({
    'lcityaccount':LCityAccountPage.tableCls,
    'lcityaccount.edit':LCityAccountForm
})

page_dc.update({
    'lcityaccount':LCityAccountPage
})