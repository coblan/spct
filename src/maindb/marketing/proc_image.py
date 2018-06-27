from PIL import Image
import io
import os
import re
def procImage(flPath): 
    flSize = os.path.getsize(flPath)
    if flSize <  10 * 1024:
        return
    
    min_size = 200
    img = Image.open(flPath)
    imgSize = ','.join([str(x) for x in img.size])
    mt = org_ext = re.search(r'\.(\w+)', flPath)
   
    if mt.group(1) == 'png':
        flContent = try_png(img)
    else:
        flContent = try_jpg(img)        
    #flContent, ext = (jpg, 'jpg') if len(jpg) < len(png) else (png, 'png')
    
    if len(flContent) > 15 * 1024:
        if min(img.size) > min_size:
            ratio =  float(min_size) / min(img.size)
            img = img.resize( tuple([int(x * ratio) for x in img.size]) , Image.ANTIALIAS)
            
            if mt.group(1) == 'png':
                flContent = try_png(img)
            else:
                flContent = try_jpg(img)  
                
            #jpg = try_jpg(img)
            #png = try_png(img)                    
            #flContent = jpg if len(jpg) < len(png) else png
    if len(flContent) < flSize:
        writeFile(flContent, flPath)
        #print(flName)


def try_jpg(img): 
    catch = io.BytesIO()
    img.save(catch, format = 'JPEG', optimize = True, progressive=True)
    return catch.getvalue()

def try_png(img): 
    catch = io.BytesIO()
    img.save(catch, format = 'PNG', optimize = True )
    return catch.getvalue()

def writeFile(flContent, flpath): 
    with open(flpath, 'wb') as f:
        f.write(flContent)
