# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,model_to_name,field_map,director
from ..models import TbAppversion
from ..status_code import *
from django.core.urlresolvers import reverse
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from django.conf import settings
from helpers.director.model_func.field_proc import BaseFieldProc

class AppPackage(TablePage):
    template='jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    def get_label(self):
        return 'App包管理'
    
    class tableCls(ModelTable):
        pop_edit_field='versionid'
        model=TbAppversion
        exclude=[]
        fields_sort=['versionid','versionname','md5','terminal','required','size','valid','description']
        def dict_head(self, head):
            dc={
                'valid':80,
                'terminal':80,
                'packageurl':180,
                'md5':160,
                'versionid':80,
                'versionname':120,
                'description':250,
                'required':100,
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
            head['required'] = True
            head['config']={
                'multiple':False,
                'accept':'.apk,.ipa',
                'upload_url':reverse('app_pkg_upload'), 
            }
        if head['name'] == 'description':
            head['editor'] = 'blocktext'
            
        return head


class AppPkgUrlProc(BaseFieldProc):
    def to_dict(self,inst,name):
        relative_url=getattr(inst,name,None)
        if relative_url:
            return {name:settings.APP_PKG_ACCESS_URL+relative_url}
        else:
            return {name:''}
     
    def clean_field(self,dc,name):
        value = dc.get(name)
        if value and value.startswith(settings.APP_PKG_ACCESS_URL):
            return value[len(settings.APP_PKG_ACCESS_URL):]
        else:
            return value

field_map[model_to_name(TbAppversion)+'.packageurl']=AppPkgUrlProc

#model_dc[TbAppversion]={'fields':AppPackageForm}

director.update({
    'app_pkg':AppPackage.tableCls,
    'app_pkg.edit':AppPackageForm,
})
page_dc.update({
    'maindb.TbAppversion':AppPackage
})
    