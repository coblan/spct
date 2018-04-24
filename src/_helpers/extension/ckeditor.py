from django.http import HttpResponse
from django.conf import settings
import os
from datetime import datetime
import json
import hashlib
import io
import urlparse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_image(request):
    """
    # urls.py
    
    from helpers.msic.ckeditor import upload_image
    
    urlpattern=[
        ...
        url(r'ckeditor/upload_image',upload_image),
    ]
    
    # setting.py
    
    MEDIA_ROOT= os.path.join( os.path.dirname(BASE_DIR),'media')
    
    """
    if request.method == 'POST':
        callback=request.GET.get('CKEditorFuncNum')
        f= request.FILES['upload']
        
        file_dir= os.path.join(settings.MEDIA_ROOT,'ckeditor')
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        catch = io.BytesIO()
        m = hashlib.md5()
        for chunk in f.chunks():
            catch.write(chunk) 
            m.update(chunk)
        catch.flush()
        file_name=m.hexdigest()+'_'+f.name
        file_path=os.path.join(file_dir,file_name)
        if not os.path.exists( file_path ):
            with open(file_path,'wb') as image_file:
                image_file.write(catch.getvalue())
                
        file_url=urlparse.urljoin(settings.MEDIA_URL, 'ckeditor/{file_name}'.format(file_name=file_name))
        if callback:
            return HttpResponse("""
            <script type="text/javascript">
            window.parent.CKEDITOR.tools.callFunction({callback},'{img_url}')
            </script>
            """.format(callback=callback,img_url=file_url))
        else:
            dc={"uploaded": 1,
                "fileName": f.name,
                'url':file_url
            }
            return HttpResponse(json.dumps(dc),content_type="application/json")

