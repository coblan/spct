from helpers.director.shortcut import TablePage,ModelTable,ModelFields,page_dc,director,SelectSearch,ModelFields
from ..ag.ag_account import AgAccountPage
from ..models import TbSportaccount

class SportAccountPage(TablePage):
    def get_label(self):
        return '沙巴账号'
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(AgAccountPage.tableCls):
        model = TbSportaccount
        exclude =[]
        
        class search(SelectSearch):
            names = ['account__nickname','username']
            exact_names=['account']
            
            def get_option(self, name):
                if name == 'account':
                    return {'value':name,'label':'账号ID'}
                elif name == 'account__nickname':
                    return {'value': name,
                                    'label': '用户昵称', }
                else:
                    return super().get_option(name)

class SportAccountForm(ModelFields):
    class Meta:
        model = TbSportaccount
        exclude =[]

director.update({
    'sportaccount':SportAccountPage.tableCls,
    'sportaccount.edit':SportAccountForm
})

page_dc.update({
    'sportaccount':SportAccountPage
})