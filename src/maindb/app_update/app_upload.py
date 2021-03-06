# encoding:utf-8

from __future__ import unicode_literals
from helpers.director.recv_file import BasicReciever
from django.conf import settings
import requests

from androguard import misc
import hashlib
import os
from maindb.tool_bucket.ios_ipa_parse import analyze_ipa_with_plistlib

class AppPackageReciever(BasicReciever):

    def getParDir(self):
        return os.path.join(settings.MEDIA_ROOT,'public','package')
    
    def procFile(self,file_data,name):
        par_dir = self.getParDir()
        file_name = self.getFileName(file_data,name)
        file_path = os.path.join(par_dir,file_name)
        
        with open(file_path,'wb') as general_file:
            general_file.write(file_data)
            general_file.flush()
            
            ext = self.getSufix(name)
            
            #relative_path = self.sendToService(file_data, ext)
            relative_path = '/package/%s'%file_name
            md5= self.getMd5(file_data)
            size = float( len(file_data) )/(1024*1024)
            size=round(size,2)
            if ext=='apk':
                pkg_code,pkg_name = self.parsePKGInfo(file_path)            
                relative_path+='?version_code=%(code)s&version_name=%(name)s&md5=%(md5)s&size=%(size)s'%{'code':pkg_code,'name':pkg_name,'md5':md5,'size':size}
            elif ext =='ipa':
                dc = analyze_ipa_with_plistlib(file_path)
                relative_path+='?version_code=%(code)s&version_name=%(name)s&md5=%(md5)s&size=%(size)s'%{'code':dc.get('version_code'),'name':dc.get('version_name'),'md5':md5,'size':size}
            else:
                relative_path+='?md5=%(md5)s&size=%(size)s'%{'md5':md5,'size':size}
                
            return settings.STATIC_SERVICE + relative_path
    
    def parsePKGInfo(self,file_path):
        a, d, dx = misc.AnalyzeAPK(file_path)
        return a.get_androidversion_code(),a.get_androidversion_name()
    
    def getMd5(self,file_data):
        m = hashlib.md5()   
        m.update(file_data)  
        return  m.hexdigest() 
    