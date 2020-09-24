from helpers.director.shortcut import TablePage,ModelTable,page_dc,ModelFields,director,RowFilter
from maindb.models import TbGamemoneyoutinfo
from . gamemoneyinfo import GameMoneyininfoPage
from helpers.func.dict_list import sort_by_name
from django.utils import timezone

class GamemoneyoutinfoPage(TablePage):
    def get_label(self):
        return '资金转出AG'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(GameMoneyininfoPage.tableCls):
        model = TbGamemoneyoutinfo
        exclude = []
        
        def get_heads(self):
            heads = super().get_heads()
            heads = sort_by_name(heads,['moneyoutid','account','account__nickname','username']) 
            return heads
        
        def get_operation(self):
            return [
                {'label':'重新转出',
                 'editor':'com-btn',
                 'row_match':'one_row',
                 'match_express':'scope.row.status==1 && scope.row._ordertime_life>300',
                 'match_msg':'只能选择下单时间超过5分钟且状态为正在转入的记录',
                 'preset_express':'rt={status:0}',
                 'click_express':'scope.ps.selected_set_and_save(scope.head)',
                 'visible':self.permit.can_edit()}
            ]   
        
        def dict_row(self, inst):
            now = timezone.now()
            return {
                '_ordertime_life': (now - inst.ordertime).seconds
            }        

class GamemoneyoutinfoForm(ModelFields):
    class Meta:
        model = TbGamemoneyoutinfo
        exclude = []

director.update({
    'gamemoneyoutinfo':GamemoneyoutinfoPage.tableCls,
    'gamemoneyoutinfo.edit':GamemoneyoutinfoForm,
})

page_dc.update({
    'gamemoneyoutinfo':GamemoneyoutinfoPage
})