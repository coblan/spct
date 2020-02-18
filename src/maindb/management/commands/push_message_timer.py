
from django.core.management.base import BaseCommand
from django.conf import settings
from helpers.director.base_data import director
from helpers.director.models import PermitModel
import os

from django.contrib.auth.models import Group,User
from django.db import connection
from helpers.director.models import KVModel,PermitModel
from django.utils import timezone
from maindb.models import TbMessage
from maindb.marketing.message_push import send_user_message,broad_message,dispatch_message
import logging

operation_log = logging.getLogger('operation_log')

class Command(BaseCommand):
    """
    """
    def handle(self, *args, **options):
        now = timezone.now()
        push = []
        for instance in TbMessage.objects.filter(issent=False,sendway=1,sendtime__lte= now):
            if instance. typeid . needread :
                send_user_message(instance)
            else:
                broad_message(instance)
            
            dispatch_message(instance)
            instance.issent = True
            instance.save()
            push.append(instance.pk)
            
        operation_log.info('推送定时消息 %s '%push)