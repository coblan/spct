from helpers.common.download_response import downloadfy_response
import json
from helpers.director.db_tools import sim_dict
from .models import WebPage

def get_global():
    return globals()

def download_page(items):
    pk_list = items.split('-')
    pk_list=[x for x in pk_list if x ]
    str_list=[]
    for pk in pk_list:
        obj = WebPage.objects.get(pk=pk)
        str_list.append(sim_dict(obj))
        
    return downloadfy_response(json.dumps(str_list), 'pages.json')
