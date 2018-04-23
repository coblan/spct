from django.shortcuts import render,HttpResponse

# Create your views here.
from scripts.export_help import gen_help

def test(request):
    gen_help()
    return HttpResponse('ok')