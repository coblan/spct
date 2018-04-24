from .models import DakaRecord
import json
from helpers.director.db_tools import to_dict
def get_global():
    return globals()

def daka(pos,user,device=''):
    json_pos=json.dumps(pos)
    inst = DakaRecord.objects.create(user=user,pos=json_pos,device=device)
    return {'status':'success','row':to_dict(inst,filt_attr=lambda x: {'pos':pos})}

