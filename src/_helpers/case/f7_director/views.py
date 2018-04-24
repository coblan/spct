from django.shortcuts import render

# Create your views here.
def f7_frame_wraper(request):
    src= request.GET.get('src')
    name=request.GET.get('name','noname')
    src=urllib.unquote( src)
    return render(request,'f7/frame_wraper.html',context={'src':src,'name':name})