# encoding:utf-8
from __future__ import unicode_literals

from django.utils.timezone import localtime,datetime

def localstr(date_obj):
    return localtime(date_obj).strftime('%Y-%m-%d %H:%M:%S')
