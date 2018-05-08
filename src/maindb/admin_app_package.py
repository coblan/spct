# encoding:utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,model_to_name
from .models import TbAppversion
from .status_code import *
from django.core.urlresolvers import reverse
from helpers.maintenance.update_static_timestamp import js_stamp_dc

class AppPackage(TablePage):
    template='jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    def get_label(self):
        return 'App包管理'
    
    class tableCls(ModelTable):
        pop_edit_field='id'
        model=TbAppversion
        exclude=[]
    
class AppPackageForm(ModelFields):
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
                'accept':'application/apk',
                'upload_url':reverse('app_pkg_upload')
            }
        return head

model_dc[TbAppversion]={'fields':AppPackageForm}


page_dc.update({
    'maindb.TbAppversion':AppPackage
})
    