from django.shortcuts import render,HttpResponse
from .app_update.app_upload import AppPackageReciever
# Create your views here.
from scripts.export_help import gen_help
from .ckeditor import CusCkeditor
from django.views.decorators.csrf import csrf_exempt

def test(request):
    gen_help()
    return HttpResponse('ok')

def recieve_app_pkg(request):
    return AppPackageReciever().asView(request)

@csrf_exempt
def recieve_ckeditor_img(request):
    return CusCkeditor().RecieveView(request)