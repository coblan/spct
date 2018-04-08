# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage,ModelTable,model_dc,page_dc,ModelFields,FieldsPage,\
     TabPage,RowSearch,RowSort,RowFilter,field_map,model_to_name
from helpers.director.model_func.dictfy import model_to_name
from .models import TbBanner
from .status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings

class BannerPage(TablePage):
    template='maindb/table_pop_edit_without_height.html'
    class tableCls(ModelTable):
        model = TbBanner
        include = ['title','status','picturename','order','createuser','createtime','description']
        
        def dict_head(self, head):
            dc={
                'title':80,
                'picturename':160,
                'order':80,
                'createtime':160,
                'createuser':80,
                'description':250,
                'status':60
            }
            if dc.get(head['name']):
                head['width'] =dc.get(head['name'])
          
            if head['name']=='picturename':
                head['editor']='com-table-picture'
               
            if head['name'] in ['createuser']:
                head['editor'] = 'com-table-label-shower'
            
            if head['name'] in ['status']:
                head['editor'] = 'com-table-mapper'  
                head['options'] = dict( BANNER_STATUS )
            
            return head
        
        def dict_row(self, inst):
            return {
                '_createuser_label':unicode(User.objects.get(pk=inst.createuser)) if inst.createuser else "",
            }
        
        class filters(RowFilter):
            names=['status']
        #class search(RowSearch):
            #names=['channel']
        class sort(RowSort):
            names=['name','order','createtime']
    
    class fieldsCls(ModelFields):
        readonly=['createuser']
        field_sort=['title','navigateurl','picturename','order','description']
        class Meta:
            model = TbBanner
            exclude=[]
            #fields=['title','navigateurl','picturename','order','description']
        
        #def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False):
            #if dc.get('picturename') :
                #mt = re.search(r'[^\/]+$',dc.get['picturename'])
                #dc['picturename']=mt.group(0)
                
        
        def dict_head(self, head):
            if head['name']=='picturename':
                head['editor']='picture'
                head['up_url']=reverse('banner_upload')
                head['config']={
                    'maxsize': settings.MAX_BANNER_SIZE #1024*1024*1
                }                
            if head['name'] =='createuser':
                head['editor']='com-field-label-shower'
            return head
        
        def dict_row(self, row):
            return {
                'createtime':row.createtime.strftime('%Y-%m-%d %H:%M:%S') if row.createtime else None,
                '_createuser_label':unicode(User.objects.get(pk=row.createuser)) if row.createuser else "",
                #'picturename':'/media/banner/'+row.picturename if row.picturename else ""
            }
        
        def save_form(self):
            ModelFields.save_form(self)
            if not self.instance.createuser:
                self.instance.createuser=self.crt_user.pk
                self.instance.save()
            return self.instance
        
    
    def get_context(self):
        ctx = TablePage.get_context(self)
        ctx['fields_heads']=self.fieldsCls(crt_user=self.crt_user).get_heads()
        ctx['model_class']= model_to_name(TbBanner)
        return ctx
    def get_label(self):
        return 'Banner管理'
    
    def get_operation(self):
        ops = TablePage.get_operation(self)
        ops.extend([
            {'name':'online','editor':'com-op-a','label':'在线'},
            {'name':'offline','editor':'com-op-a','label':'离线'}
        ])
        return ops

class PicturenameProc(object):
    def to_dict(self,inst,name):
        pic=getattr(inst,name,None)
        if pic:
            return '/media/banners/'+pic
        else:
            return '' 
    
    #def get_label(self,inst,name):
        #foreign=getattr(inst,name,None)
        #if foreign:
            #return unicode(foreign)
    
    def from_dict(self,value,field):
        if value:
            mt = re.search(r'[^\/]+$',value)
            return mt.group(0) 
        
            
        #if isinstance(value,models.Model):
            #return value
        #else:
            #model=field.rel.to
            #if not value:
                #return None
            #else:
                #return model.objects.get(pk=value)  
            
model_dc[TbBanner]={'fields':BannerPage.fieldsCls}
field_map[model_to_name(TbBanner)+'.picturename']=PicturenameProc
#TbBanner.picturename.attname
