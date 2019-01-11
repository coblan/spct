from helpers.director.base_data import js_tr_list, js_lib_list
from django.utils.translation import ugettext as _
from helpers.maintenance.update_static_timestamp import js_stamp_dc

def get_tr():
    return {
    }

js_tr_list.append(get_tr)

def get_lib(request): 
    dc = {
        'maindb': '/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js'),
        'activity_v2':'/static/js/activity_v2.pack.js?t=%s&test=19bba27'%js_stamp_dc.get('activity_v2_pack_js')
    }
    return dc

js_lib_list.append(get_lib)