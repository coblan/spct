# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,model_to_name,field_map
from .models import TbAppversion
from .status_code import *
from django.core.urlresolvers import reverse
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from django.conf import settings

class AppPackage(TablePage):
    template='jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    def get_label(self):
        return 'App包管理'
    
    class tableCls(ModelTable):
        pop_edit_field='versionid'
        model=TbAppversion
        exclude=['id']
        fields_sort=['versionid','versionname','md5','terminal','required','size','packageurl','description']
        def dict_head(self, head):
            dc={
                'terminal':80,
                'packageurl':180,
                'md5':160,
                'versionid':80,
                'versionname':80,
                'description':250,
                'required':60,
                'size':60                
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])  
            return head
              
    
class AppPackageForm(ModelFields):
    extra_mixins=['app_pkg']
    class Meta:
        model = TbAppversion
        exclude = []
    
    def dict_head(self, head):

        if head['name'] in ['md5','versionid','versionname','size']:
            head['readonly']=True
        if head['name'] == 'packageurl':
            head['editor']= 'com-field-app-pkg-uploader' #'com-field-plain-file'
            head['config']={
                'multiple':False,
                'accept':'.apk,.ipa',
                'upload_url':reverse('app_pkg_upload')
            }
            
        return head


class AppPkgUrlProc(object):
    def to_dict(self,inst,name):
        relative_url=getattr(inst,name,None)
        if relative_url:
            return settings.APP_PKG_ACCESS_URL+relative_url
        else:
            return '' 
    
    #def get_label(self,inst,name):
        #foreign=getattr(inst,name,None)
        #if foreign:
            #return unicode(foreign)
    
    def from_dict(self,value,field):
        if value:
            if value.startswith(settings.APP_PKG_ACCESS_URL):
                return value[len(settings.APP_PKG_ACCESS_URL):]
            else:
                return value

field_map[model_to_name(TbAppversion)+'.packageurl']=AppPkgUrlProc

model_dc[TbAppversion]={'fields':AppPackageForm}


page_dc.update({
    'maindb.TbAppversion':AppPackage
})
    