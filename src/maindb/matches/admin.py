from .ticket_master import *
from .odds import *

from helpers.director.access.permit_data import model_full_permit, model_to_name, add_permits
#permits = [ 
           #('TbMatches', model_full_permit(TbMatches), model_to_name(TbMatches) , 'model'), 
           #('TbTicketmaster', model_full_permit(TbTicketmaster), model_to_name(TbTicketmaster), 'model'), 
           #('TbTicketstake', model_full_permit(TbTicketstake), model_to_name(TbTicketstake), 'model'), 
           #('TbTicketparlay', model_full_permit(TbTicketparlay), model_to_name(TbTicketparlay), 'model'), 
           
            #('TbTicketmaster.all', 'TbTicketmaster;TbTicketstake;TbTicketparlay', '', 'set'), 
           #]

#add_permits(permits)    