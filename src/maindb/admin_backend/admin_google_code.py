from helpers.director.kv import get_value,set_value
from helpers.director.shortcut import FieldsPage,Fields,page_dc,director
from maindb.google_validate import random_base32
from django.core.exceptions import PermissionDenied

class GoogleCode(FieldsPage):
    def get_label(self):
        return '谷歌身份验证'
    
    def get_template(self, prefer=None):
        return 'jb_admin/fields.html'
    
    def check_permit(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied('没有权限访问')

    class fieldsCls(Fields):
        def get_heads(self):
            return [
                {'name':'code','label':'二维码','editor':'com-field-picture','readonly':True}
            ]
        
        def get_row(self):
            if not get_value('google_validate_code'):
                code = random_base32()
                set_value('google_validate_code',code)
            url = 'otpauth://totp/sportscenter?secret=%s'%get_value('google_validate_code')
            return {
                'code':'/d/qr?content=%s'%url,
                '_director_name':'googlecode'
            }
        
        def save_form(self):
            code = random_base32()
            set_value('google_validate_code',code)
        
        def get_operations(self):
            ops = super().get_operations()
            for op in ops:
                if op['name'] =='save':
                    op['label'] = '重新生成'
            return ops
            
            


director.update({
    'googlecode':GoogleCode.fieldsCls
})

page_dc.update({
    'googlecode':GoogleCode
})