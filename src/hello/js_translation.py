# this file maybe not use

from django.utils.translation import ugettext as _

def get_tr():
    
    tr={
        'base_setting':_('Basic Setting'),
        'language':_('Language'),
        'back':_('back'),
        'search':_('Search'),
        'change_password':_('Change Password'),
        'logout':_('LogOut'),
        'login':_('LogIn'),
    }
    return tr