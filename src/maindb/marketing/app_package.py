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
import os

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
    
    #def save_form(self): 
        #super().save_form()
    def clean_save(self): 
        if self.instance.terminal ==1:
            plist_fl = plist_template % {'ipa_download': settings.STATIC_SERVICE + self.instance.packageurl, 'version': self.instance.versionname,}
            fl_path = os.path.join(settings.MEDIA_ROOT, 'public', 'package', self.instance.md5 + '.plist')
            with open(fl_path, 'wb') as f:
                f.write(plist_fl.encode('utf-8'))
            self.instance.plisturl = '/package/%s' % self.instance.md5 + '.plist'
            
    


class AppPkgUrlProc(BaseFieldProc):
    def to_dict(self,inst,name):
        relative_url=getattr(inst,name,None)
        if relative_url:
            return {name:settings.STATIC_SERVICE+relative_url}
        else:
            return {name:''}
     
    def clean_field(self,dc,name):
        value = dc.get(name)
        if value and value.startswith(settings.STATIC_SERVICE):
            return value[len(settings.STATIC_SERVICE):]
        else:
            return value

field_map[model_to_name(TbAppversion)+'.packageurl']=AppPkgUrlProc

#model_dc[TbAppversion]={'fields':AppPackageForm}

director.update({
    'app_pkg':AppPackage.tableCls,
    'app_pkg.edit':AppPackageForm,
})
page_dc.update({
    'app_package':AppPackage
})
    

plist_template = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>items</key>
        <array>
            <dict>
                <key>assets</key>
                <array>
                    <dict>
                        <key>kind</key>
                        <string>software-package</string>
                        <key>url</key>
                        <string>%(ipa_download)s</string>
                    </dict>
                    <dict>
                        <key>kind</key>
                        <string>full-size-image</string>
                        <key>needs-shine</key>
                        <true/>
                        <key>url</key>
                        <string></string>
                    </dict>
                    <dict>
                        <key>kind</key>
                        <string>display-image</string>
                        <key>needs-shine</key>
                        <true/>
                        <key>url</key>
                        <string></string>
                    </dict>
                </array>
                <key>metadata</key>
                <dict>
                    <key>bundle-identifier</key>
                    <string>com.jingbo.DQGuess</string>
                    <key>bundle-version</key>
                    <string>%(version)s</string>
                    <key>kind</key>
                    <string>software</string>
                    <key>subtitle</key>
                    <string>飞球竞猜</string>
                    <key>title</key>
                    <string>飞球竞猜</string>
                </dict>
            </dict>
        </array>
    </dict>
</plist>
"""