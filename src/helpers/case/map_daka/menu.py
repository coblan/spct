# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.engine import BaseEngine,can_list,can_touch,fa,page,and_list
#from .models import WorkRecord,Work,Index
from helpers.director.shortcut import ModelPermit
from helpers.case.organize.workpermit import WorkPermitModel
#from .pages.work_list import WorkReadValidDepart
#from .admin import WorkCheckValidDepart,WRselfValidDepart
from django.core.exceptions import PermissionDenied


#def can_check_work(request):
    #try:
        #permit = WorkCheckValidDepart.parse_request(request)
        #if permit.get_crt_depart():
            #return True
    #except PermissionDenied:
        #return False

#def can_create_work(request):
    #try:

        #valid_depart = WRselfValidDepart.parse_request(request)
        #if valid_depart.get_crt_depart():
            #return True
    #except PermissionDenied:
        #return False

    #permit=ModelPermit(WorkRecord, user)
    #return permit.can_add()

#def can_read_all(request):
    #try:
        #permit = WorkReadValidDepart.parse_request(request)
        #if permit.get_crt_depart():
            #return True
    #except PermissionDenied as e:
        #return False

#pc_menu= {'label':'工作统计','icon':fa('fa-users'),'visible':can_list((Work,WorkRecord,Index)),
          #'submenu':[{'label':'工作类别','url': page('work.workindex'),'visible':can_list([Work,Index])},
                    #{'label':'工作记录','url':page('work.workrecord'),'visible':can_touch(WorkRecord)}
                    #]
         #}

f7_menu=[
    {'name':'map_daka_dakarecord_f7','label':'地图打卡','url':page('map_daka.dakarecord.f7'),'icon':fa('fa-map fa-2x')}
]


