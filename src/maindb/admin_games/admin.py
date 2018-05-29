from .ticket_admin import *
from .ViewTicketSingleByMatch import *
from .matchs import *
from helpers.director.access.permit_data import model_full_permit, model_to_name, add_permits
permits = [ 
           ('TbMatches', model_full_permit(TbMatches), model_to_name(TbMatches) , 'model'), 
           #('TbTicketmaster', model_full_permit(TbTicketmaster), model_to_name(TbTicketmaster), 'model'), 
           ]

add_permits(permits)    