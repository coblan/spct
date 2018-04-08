# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import json
import inspect
from django.http import HttpResponse
from helpers.director.port import jsonpost
from helpers.common.dir_man import DirMan
from .models import Department
from helpers.common.layer_tree import LayerTree

def manage_department(request):
    manager=DirMan(Department)
    scope= dict(inspect.getmembers(manager,inspect.ismethod))
    return ajax_router(request, scope)

def tree_department(request):
    manager=LayerTree(Department)
    scope= dict(inspect.getmembers(manager,inspect.ismethod))
    if request.GET.get('get_class'):
        return HttpResponse( json.dumps(scope.keys()),content_type="application/json")
    else:
        return ajax_router(request, scope)