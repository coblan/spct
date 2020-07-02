# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,model_to_name,field_map,director,has_permit
from ..models import TbAppversion
from ..status_code import *
from django.core.urlresolvers import reverse
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from django.conf import settings
from helpers.director.model_func.field_proc import BaseFieldProc
import os
from subprocess import Popen
from hello.merchant_user import get_user_merchantid,MerchantInstancCheck
from helpers.director.access.permit import can_write

import logging
general_log = logging.getLogger('general_log')

operation_log = logging.getLogger('operation_log')

class AppPackage(TablePage):
    template='jb_admin/table.html'
  
    def get_label(self):
        return 'App包管理'
    
    class tableCls(ModelTable):
        pop_edit_field='versionid'
        model=TbAppversion
        exclude=[]
        fields_sort=['merchant','versionid','versionname','md5','terminal','required','size','valid','description']
        
        def inn_filter(self, query):
            if self.crt_user.merchant:
                return query.filter(merchant_id = self.crt_user.merchant.id)
            else:
                return query
        
        def dict_head(self, head):
            dc={
                'valid':80,
                'terminal':80,
                'packageurl':180,
                'md5':180,
                'versionid':80,
                'versionname':120,
                'description':250,
                'required':100,
                'size':60                
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])  
            return head
    
        def get_operation(self):
            ops = super().get_operation()
            ls =[]
            for op in ops:
                if op['name'] == 'add_new':
                    ls.append(op)
            ls += [
                {'fun': 'selected_set_and_save', 'editor': 'com-op-btn', 
                 'label': '作废', 'confirm_msg': '确认作废已选中项？',
                 'pre_set': 'rt={valid:false}', 'row_match': 'many_row',
                 'visible':can_write(TbAppversion,self.crt_user)},
            ]
            return ls
                         #'after_save':'ex.director_call("notify_match_recommend",{rows:scope.rows})',
        class filters(RowFilter):
            icontains=['description']
            
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['description','terminal','valid']
                else:
                    return ['merchant','description','terminal','valid']
              
    
class AppPackageForm(MerchantInstancCheck,ModelFields):
    extra_mixins=['app_pkg']
    readonly = ['plisturl']
    
    class Meta:
        model = TbAppversion
        exclude = []
    
    @property
    def hide_fields(self):
        if self.crt_user.merchant:
            return ['merchant']
        else:
            return []
    
    def clean_dict(self, dc):
        if self.crt_user.merchant:
            dc['merchant'] = self.crt_user.merchant.id
        return dc
    
    def dict_head(self, head):
        if head['name'] in ['md5','size']:
            head['readonly']=True
        if head['name'] == 'plisturl':
            head['show'] = 'scope.row.terminal==1'
            
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
            head['fv_rule'] = 'length(~200)'
            
        return head
    
    
    def clean_save(self): 
        if self.instance.terminal ==1:
            if self.instance.merchant:
                merchantname = self.instance.merchant
            elif self.crt_user.merchant:
                merchantname = self.crt_user.merchant.merchantname
            
            PACKAGE_NAME = settings.MERCHANT.get(merchantname).PACKAGE_NAME
            PRODUCT_NAME = settings.MERCHANT.get(merchantname).PRODUCT_NAME
            
            plist_fl = plist_template % {'ipa_download': settings.CLOUD_STORAGE + self.instance.packageurl, 
                                         'package_name': PACKAGE_NAME,
                                         'prod_name': PRODUCT_NAME,
                                         'version': self.instance.versionname,}
            fl_path = os.path.join(settings.MEDIA_ROOT, 'public', merchantname,'package', self.instance.md5 + '.plist')
            with open(fl_path, 'wb') as f:
                f.write(plist_fl.encode('utf-8'))
            self.instance.plisturl = '/%s/package/%s' % (merchantname,self.instance.md5 + '.plist')
    
    def save_form(self): 
        super().save_form()
        #if 'packageurl' in self.changed_data:
        # 现在要求每次都重传S3服务器
        if 'md5' in self.changed_data:
            plateform = {1:'ios',2:'android'}.get(self.instance.terminal)
            if getattr(settings,'UPLOAD_CLOUD_SHELL',None):
                shell_file = getattr(settings,'UPLOAD_CLOUD_SHELL')
                Popen('%(shell)s %(plateform)s'%{'shell':shell_file,'plateform':plateform},shell=True)
                general_log.info('执行批处理 %s'%shell_file)
                #os.system('%(shell)s %(arg)s'%{'shell':shell,'arg':arg})  

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
                    <string>%(package_name)s</string>
                    <key>bundle-version</key>
                    <string>%(version)s</string>
                    <key>kind</key>
                    <string>software</string>
                    <key>subtitle</key>
                    <string>%(prod_name)s</string>
                    <key>title</key>
                    <string>%(prod_name)s</string>
                </dict>
            </dict>
        </array>
    </dict>
</plist>
"""