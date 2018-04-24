from django.shortcuts import render
from helpers.director.port import jsonpost
from helpers.common.dir_man import DirMan
from .models import Work,Index
import inspect
# Create your views here.

def dir_man(request):
    mana=DirMan(Index, Work)
    scope= dict(inspect.getmembers(mana,inspect.ismethod))
    return ajax_router(request, scope)