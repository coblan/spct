# encoding:utf-8
from __future__ import unicode_literals

from helpers.director.engine import BaseEngine,can_list,can_touch,fa,page,and_list
from .models import WorkRecord,Work,Index
from helpers.director.shortcut import ModelPermit
from helpers.case.organize.workpermit import WorkPermitModel
from .pages.work_list import WorkReadValidDepart
from .admin import WorkCheckValidDepart,WRselfValidDepart
from django.core.exceptions import PermissionDenied


def can_check_work(request):
     try:
          permit = WorkCheckValidDepart.parse_request(request)
          if permit.get_crt_depart():
               return True
     except PermissionDenied:
          return False

def can_create_work(request):
     try:
          
          valid_depart = WRselfValidDepart.parse_request(request)
          if valid_depart.get_crt_depart():
               return True
     except PermissionDenied:
          return False
     
     permit=ModelPermit(WorkRecord, user)
     return permit.can_add()

def can_read_all(request):
     try:
          permit = WorkReadValidDepart.parse_request(request)
          if permit.get_crt_depart():
               return True
     except PermissionDenied as e:
          return False

pc_menu= {'label':'工作统计','icon':fa('fa-users'),'visible':can_list((Work,WorkRecord,Index)),
         'submenu':[{'label':'工作类别','url': page('work.workindex'),'visible':can_list([Work,Index])},
                    {'label':'工作记录','url':page('work.workrecord'),'visible':can_touch(WorkRecord)}
                    ]
         }

wx_menu=[
    {'label':'工作类别','url':page('work.workindex.wx'),'icon':'<img src="/static/res/image/work_types.ico" />','visible':can_list((Work,Index))}, 
    {'label':'个人工作提交','url':page('work.wkself.wx'),'icon':fa('fa-list-ol fa-2x'),'visible':can_create_work},  
    {'label':'工作审核','url':page('work.workrecord.wx'),'icon':fa('fa-check-square-o fa-2x'),'visible':can_check_work},  

    {'label':'工作记录','url':page('work.worklist.wx'),'icon':fa('fa-calendar-check-o fa-2x'),'visible':can_read_all},     
]

f7_menu=[
     {'name':'work_workindex_f7','label':'工作类别','url':page('work.workindex.f7'),'icon':'<img src="/static/res/image/work_types.ico" />','visible':can_list((Work,Index))}, 
    {'name':'work_wkself_f7','label':'个人工作提交','url':page('work.wkself.f7'),'icon':fa('fa-list-ol fa-2x'),'visible':can_create_work},  
    {'name':'work_workrecord_f7','label':'工作审核','url':page('work.workrecord.f7'),'icon':fa('fa-check-square-o fa-2x'),'visible':can_check_work},  

    {'name':'work_worklist_f7','label':'工作记录','url':page('work.worklist.f7'),'icon':fa('fa-calendar-check-o fa-2x'),'visible':can_read_all},     
]
    

