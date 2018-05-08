# encoding:utf-8

from __future__ import unicode_literals
from helpers.director.recv_file import BasicReciever
from django.conf import settings
import requests
import urlparse
from androguard import misc
import hashlib



class AppPackageReciever(BasicReciever):
    #def asView(self,request):
        #file_dict = request.FILES
        #file_url_list=[]
        #for name, fl in file_dict.items():
            #file_data= self.readFile(fl)
            #file_url = self.procFile(file_data,name)
            #file_url_list.append(file_url)
            
        #return HttpResponse(json.dumps(file_url_list),content_type="application/json")
    
    def procFile(self,file_data,name):
        file_path,file_name = self.getFilePath(file_data,name)
        with open(file_path,'wb') as general_file:
            general_file.write(file_data)
            general_file.flush()
            pkg_code,pkg_name = self.parsePKGInfo(file_path)
            ext = self.getSufix(name)
            relative_path = self.sendToService(file_data, ext)
            
            md5= self.getMd5(file_data)
            size = float( len(file_data) )/(1024*1024)
            size=round(size,2)
            relative_path+='?version_code=%(code)s&version_name=%(name)s&md5=%(md5)s&size=%(size)s'%{'code':pkg_code,'name':pkg_name,'md5':md5,'size':size}
            return settings.APP_PKG_ACCESS_URL + relative_path
    
    def parsePKGInfo(self,file_path):
        a, d, dx = misc.AnalyzeAPK(file_path)
        return a.get_androidversion_code(),a.get_androidversion_name()
    
    def getMd5(self,file_data):
        m = hashlib.md5()   
        m.update(file_data)  
        return  m.hexdigest() 
    
    def sendToService(self,file_data,ext):
        """
        blob:文件二进制
        ext:文件扩展名   .jpg
        """
        
        upload_url =settings.APP_PKG_UPLOAD_URL

        header={ 'Authorization': '76bbc167ed744ddd9d409b09705ddf13',
                 'X-Extension':'.'+ext}

        rt = requests.post(upload_url,data=file_data,headers=header)
        return rt.text

    