from helpers.director.shortcut import TablePage,ModelTable,page_dc,director,director_view,get_request_cache
from maindb.models import TbAccount
import requests
from django.conf import settings
from .member.chum_user import ChumUser
from .models import TbUserex
import logging

general_log = logging.getLogger('general_log')


class KefuPage(TablePage):
    def get_label(self):
        return '客服'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ChumUser.tableCls):
        #model = TbAccount
        #include =['accountid','nickname']
        
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
                #{'fun':'director_call','label':'联系客户',
                 #'row_match':'scope.ps.selected.length ==1',
                 #'match_msg':'cfg.toast("请选择一个客户")',
                 #'editor':'com-op-btn',
                 #'director_name':'call_client',}
            ]
        
        def inn_filter(self, query):
            return  query #query.filter(sumrechargecount__lte=1)
        
@director_view('call_client')
def call_client(rows,**kws):
    client_dict = rows[0]
    client = TbAccount.objects.get(pk = client_dict.get('pk'))
    user = get_request_cache()['request'].user
    try:
        info = TbUserex.objects.get(userid = user.pk)
    except TbUserex.DoesNotExist:
        raise UserWarning('当前账号不具备分机号，请联系管理员!')
    url = '%(domain)s/api/ola/agents/%(fenji)s/dial/%(mobile)s'%{'domain':getattr(settings,'OLA_DOMAIN','http://115.28.186.246:8080'),'fenji':info.extnumber,'mobile':client.phone}
    #http://115.28.186.246:8080/api/ola/agents/1551/dial/17380565153
    general_log.info('给用户%s打电话'%client)
    rt = requests.put(url)
    if rt.status_code != 200:
        raise UserWarning('请求网络电话出现问题,请联系管理员')
    


director.update({
    'kefupage':KefuPage.tableCls,
})

page_dc.update({
    'kefupage':KefuPage
})