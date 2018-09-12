from .black_users import *
from . import max_payout

from helpers.director.access.permit_data import model_full_permit, model_to_name, add_permits

permits = [
    ('Whiteuserlist', model_full_permit(Whiteuserlist), model_to_name(Whiteuserlist), 'model'),]

add_permits(permits)
