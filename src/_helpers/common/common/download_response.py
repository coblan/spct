
from django.http import HttpResponse

def downloadfy_response(response_or_content,name):
    if isinstance(response_or_content,HttpResponse):
        rs=response_or_content
    else:
        rs=HttpResponse(response_or_content)
    rs['Content-type'] = 'application/octet-stream'  # 'text/plain'
    rs['Content-Disposition'] = 'attachment; filename="{name}"'.format(name=name)
    return rs     
    
    
# class DownLoadWrap(object):
    # def __init__(self,name,request):
        
# def proxy_download(request):
    # url = request.GET.get('url')
    # resolution = request.GET.get('resolution')
    # mt = re.search('([^/-]+)-?(\d+x\d+)?(.jpg)',url,re.I)
    # if resolution:
        # name = mt.group(1)+'-'+str(resolution)+mt.group(3)
    # else:
        # name = mt.group(1)+mt.group(3)
    # url = url[:mt.start(1)]+name
    # rt = requests.get(url)
    # if rt.status_code!=200:
        # name = mt.group(1)+mt.group(3)
        # url = url[:mt.start(1)]+name 
        # rt = requests.get(url)
    # rs = HttpResponse(rt.content)
    # rs['Content-type'] = 'application/octet-stream'  # 'text/plain'
    # # rs['Content-type'] = 'image/jpeg'
    # rs['Content-Disposition'] = 'attachment; filename="{name}"'.format(name=name)
    # return rs   