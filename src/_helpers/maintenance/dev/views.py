from django.http import HttpResponse
from django.shortcuts import render

def fileupload(request):
    return render(request,'dev/fileupload.html')