from .banner import *
from .notice import *
from maindb.basic_data.currency import *
from .help_center import *
from .activity import *
from maindb.basic_data.app_resource import *
from .app_package import *

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