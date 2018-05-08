from django.shortcuts import render,HttpResponse
from .app_update.app_upload import AppPackageReciever
# Create your views here.
from scripts.export_help import gen_help


def test(request):
    gen_help()
    return HttpResponse('ok')

def recieve_app_pkg(request):
    return AppPackageReciever().asView(request)