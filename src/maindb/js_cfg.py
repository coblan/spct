from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.update_static_timestamp import js_stamp_dc

def get_tr():
    return {
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {
        'maindb': '/static/js/maindb.pack.js?t=%s&t2=123'%js_stamp_dc.get('maindb_pack_js'),
    }
    return dc

js_lib_list.append(get_lib)