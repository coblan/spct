from .blanklist import * 
from .rc_filter import * 
from .rc_level import * 
from .rc_user import * 
from .withdraw_limit_log import * 

from helpers.director.access.permit_data import model_full_permit, model_to_name, add_permits
permits = [ 
           ('TbBlackuserlist', model_full_permit(TbBlackuserlist), model_to_name(TbBlackuserlist) , 'model'), 
           ('TbBlackuserlistLog', model_full_permit(TbBlackuserlistLog), model_to_name(TbBlackuserlistLog), 'model'), 
            ('Blackiplist', model_full_permit(Blackiplist), model_to_name(Blackiplist), 'model'),
            ('Blackiprangelist', model_full_permit(Blackiprangelist), model_to_name(Blackiprangelist), 'model'),
            ('Whiteiplist', model_full_permit(Whiteiplist), model_to_name(Whiteiplist), 'model'),
            ('Whiteuserlist', model_full_permit(Whiteuserlist), model_to_name(Whiteuserlist), 'model'),
           ]

add_permits(permits)    