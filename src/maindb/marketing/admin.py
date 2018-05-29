from .admin_banner import *
from .admin_TbNotice import *
from .admin_TbCurrency import *
from .admin_help import *
from .admin_activity import *
from .admin_app_resource import *
from .admin_app_package import *


from helpers.director.shortcut import model_to_name, model_full_permit, add_permits


permits = [('TbBanner', model_full_permit(TbBanner), model_to_name(TbBanner) , 'model'), 
           ('TbAppversion', model_full_permit(TbAppversion), model_to_name(TbAppversion) , 'model'), 
           ('TbNotice', model_full_permit(TbNotice), model_to_name(TbNotice), 'model'), 
           ('TbCurrency', model_full_permit(TbCurrency), model_to_name(TbCurrency), 'model'), 
           ('TbQa', model_full_permit(TbQa), model_to_name(TbQa), 'model'), 
           ('TbActivity', model_full_permit(TbActivity), model_to_name(TbActivity), 'model'), 
           ('TbAppresource', model_full_permit(TbAppresource), model_to_name(TbAppresource), 'model')
           ]

add_permits(permits)