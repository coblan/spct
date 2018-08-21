from .blanklist import * 
from .rc_filter import * 
from .rc_level import * 
from .rc_user import * 
from .withdraw_limit_log import * 
from . import admin_limit

from helpers.director.access.permit_data import model_full_permit, model_to_name, add_permits
permits = [ 
    ('TbRcFilter', model_full_permit(TbRcFilter), model_to_name(TbRcFilter) , 'model'), 
    ('TbRcLevel', model_full_permit(TbRcLevel), model_to_name(TbRcLevel) , 'model'), 
    ('TbRcUser', model_full_permit(TbRcUser), model_to_name(TbRcUser) , 'model'), 
    ('TbWithdrawlimitlog', model_full_permit(TbWithdrawlimitlog), model_to_name(TbWithdrawlimitlog) , 'model'), 
     
    
    ('TbBlackuserlist', model_full_permit(TbBlackuserlist), model_to_name(TbBlackuserlist) , 'model'), 
    ('TbBlackuserlistLog', model_full_permit(TbBlackuserlistLog), model_to_name(TbBlackuserlistLog), 'model'), 
    ('Blackiplist', model_full_permit(Blackiplist), model_to_name(Blackiplist), 'model'),
    ('Blackiprangelist', model_full_permit(Blackiprangelist), model_to_name(Blackiprangelist), 'model'),
    ('Whiteiplist', model_full_permit(Whiteiplist), model_to_name(Whiteiplist), 'model'),
    ('Whiteuserlist', model_full_permit(Whiteuserlist), model_to_name(Whiteuserlist), 'model'),
    ]

add_permits(permits)    