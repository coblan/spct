from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director
from .models import TbBackendwhiteip
from .riskcontrol.white_ip_rangelist import WhiteIPRangeList,WhiteIPRangeForm
class AdminIpPage(TablePage):
    def get_label(self):
        return '后台登录IP白名单'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(WhiteIPRangeList.tableCls):
        model = TbBackendwhiteip
        exclude = ['type']

class AdminIpForm(WhiteIPRangeForm):
    class Meta:
        model = TbBackendwhiteip
        exclude =['type']
        


director.update({
    'admin_ip':AdminIpPage.tableCls,
    'admin_ip.edit':AdminIpForm
})

page_dc.update({
    'admin_ip':AdminIpPage
})