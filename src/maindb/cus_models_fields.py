# encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from helpers.director.shortcut import field_map,director_view,director_element,has_permit
from helpers.director.model_func.field_proc import BaseFieldProc
import re
from helpers.director.recv_file import GeneralUpload

class CusPictureField(models.CharField):
    pass

class CusPictureMap(BaseFieldProc):
    '''
    接收图片，以md5的形式，存储在public/images,默认folder是head['up_url']='/d/upload?path=public/images'
    如果要自定义，请在dict_head中，重新指定head['up_url']='/d/upload?path=public/{yourfolder}'
    '''
    
    #def __init__(self, instance=None, name=None, model=None, field=None):
        #super().__init__()

    def to_dict(self,inst,name):
        value = getattr(inst,name,None)
        #if value and value.startswith('/images/'):
        if value:
            out =  '/media/public%(file_path)s'%{'file_path':value}
        else:
            out = value
        return {
            name:out
        }
    
    def clean_field(self,dc,name):
        """
        """
        value = dc.get(name)
        if value:
            mt = re.search('/media/public(/.*)',value)
            if mt:
                return mt.group(1)
        else:
            return value
    
    def dict_table_head(self,head): 
        head['editor']='com-table-picture'
        head['show_tooltip'] = False
        head['width'] = 150
        return head
    
    def dict_field_head(self,head):
        head['editor']='com-field-picture'
        head['up_url']='/d/upload?path=public/images'
        head['maxsize'] = 300*1024
        if self.crt_user.merchant:
            head['up_url']='/d/upload?path=public/%s/images'% self.crt_user. merchant.merchantname
        return head


class CusFileField(models.CharField):
    pass

class CusFielFieldProc(CusPictureMap):
    def dict_field_head(self,head):
        head['editor']='com-field-plain-file'
        #head['up_url']='/d/upload?path=public/resource'
        head['config']={
            'upload_url':'/d/upload?path=public/resource', 
            'accept': '*',
        }
        if self.crt_user.merchant:
            head['upload_url']='/d/upload?path=public/%s/resource'% self.crt_user.merchant.merchantname
            
        return head    

#class CloudFileField(models.CharField):
    #pass

#class CloudFileFieldProc(CusPictureMap):
    #def dict_field_head(self,head):
        #head['editor']='com-field-plain-file'
        #head['config']={
            #'upload_url':'/d/upload?path=public/resource&director=cloudfile_uploader', 
            #'accept': '*',
        #}
        #return head   

@director_element('cloudfile_uploader')
class CloudFileUploader(GeneralUpload):
    def procFile(self,file_data,name):
        rt = super().procFile(file_data,name)
        print('hello')
        return rt


field_map[CusPictureField]=CusPictureMap
field_map[CusFileField] = CusFielFieldProc
#field_map[CloudFileField]=CloudFileFieldProc
