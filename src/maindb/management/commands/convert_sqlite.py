# encoding:utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import director
from helpers.director.models import PermitModel
from django.conf import settings
import os
import sqlite3
from django.contrib.auth.models import Group,User
from django.db import connection
from helpers.director.models import KVModel,PermitModel

base_dir = settings.BASE_DIR
conn = sqlite3.connect(os.path.join(base_dir,'db.sqlite3'))

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        self.cursor = conn.cursor()
        print('清空当前数据库')
        User.objects.all().delete()
        Group.objects.all().delete()
 
        KVModel.objects.all().delete()
        PermitModel.objects.all().delete()
        print('导入用户信息')
        self.import_model(User,'auth_user',include=lambda x:x.get('is_staff'))
        print('导入角色分组')
        self.import_model(Group,'auth_group')
        
        rows = []
        user_dc={}
        for row in self.cursor.execute('''SELECT * from auth_user_groups'''):
            user_pk = row[1]
            group_pk = row[2]
            if  user_pk not in user_dc:
                user_dc[user_pk] =[group_pk]
        print('导入用户分组信息')
        for k,v in user_dc.items():
            user = User.objects.get(pk = k)
            user.groups.add(*v)
        print('导入kvmodel')
        self.import_model(KVModel,'director_kvmodel')
        print('导入权限')
        self.import_model(PermitModel,'director_permitmodel',include=lambda x: x.get('group_id') )
            
        #with connection.cursor() as db_cursor:
            #ls = ['insert into auth_user_groups (id,user_id,group_id) VALUES %s'%str(x) for x in rows]
            #db_cursor.execute('alter table auth_user_groups  NOCHECK constraint all; ')
            #db_cursor.execute(';'.join(ls))
            #db_cursor.execute('alter table auth_user_groups  CHECK constraint all;  ')
        
                    

    def import_model(self,Model,model_name,include=None):
        rows =[]
        for row in self.cursor.execute('''SELECT * from %s'''%model_name):
            dc = {}
            for index, head in enumerate(self.cursor.description):
                dc[head[0]] = row[index]
            if include:
                if include(dc):
                    rows.append( Model(**dc) )
            else:
                rows.append( Model(**dc) )
        Model.objects.bulk_create(rows)
    
    