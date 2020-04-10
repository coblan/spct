from helpers.authuser.admin_login import LoginFormPage
from helpers.director.shortcut import page_dc

class SportLoginPage(LoginFormPage):
    need_login = False
    need_staff = False
    def get_context(self): 
        ctx = super().get_context()
        next_url= self.request.GET.get('next','/')
        dc={
            'page_cfg': {     
                'next':next_url,
                'title': '用户登录',
                'subtitle': '欢迎登录SportsCenter系统',
                'copyright': 'Copyright @2020  All Right Reserve',
                'heads': self.get_heads(),
                'login_item': '账号',
                },
        } 
        
        ctx.update(dc)
        return ctx

page_dc.update({
    'login':SportLoginPage
})