from helpers.director.access.permit import ModelPermit
from helpers.director.base_data import permit_dc
from .models import TbBanner, TbAppversion, TbNotice, TbAccount

from helpers.director.shortcut import model_to_name, model_full_permit, add_permits

import json



permits = [('TbBanner', json.dumps(model_full_permit(TbBanner)), model_to_name(TbBanner) ), 
           ('TbAppversion', json.dumps(model_full_permit(TbAppversion)), model_to_name(TbAppversion) )
           ]

add_permits(permits)


