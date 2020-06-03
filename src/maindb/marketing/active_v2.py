from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc ,director,director_view,RowSort,RowSearch,RowFilter
from ..models import TbActivityV2,TbActivitySettings,TbActivityTemplate,TbMerchants
from helpers.director.access.permit import can_touch,has_permit
from helpers.func.collection.container import evalue_container
from ..static_html_builder import StaticHtmlBuilder
from urllib.parse import urljoin
from helpers.func.sim_signal import sim_signal
from django.conf import settings
import os
from hello.merchant_user import get_user_merchantid,MerchantInstancCheck
from .help_center import MerchantSelect

class ActiviyV2Page(TablePage):
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    def get_label(self):
        return '优惠活动'
    
    def get_context(self):
        ctx = super().get_context()
        act_form = ActivityV2Form(crt_user=self.crt_user)
        act_setting= ActivitySettingTable(crt_user=self.crt_user)
        named_ctx={
            'activity_v2_tabs':[
                {'name':'activity_form',
                 'label':'活动编辑',
                 'com': 'com-tab-fields',
                 'heads':act_form.get_heads(),
                 'ops': act_form.get_operations(),
                 'get_data': {
                     'fun': 'table_row',
                 },
                 'after_save': {
                     'fun': 'update_or_insert'
                 },
                 },
                {'name':'activity_setting',
                 'label':'设置',
                 'com':'com-tab-table',
                 #'par_field': 'pk',
                 'pre_set':'rt={meta_par_pk:scope.par_row.pk}',
                 'table_ctx': act_setting.get_head_context(),
                 'visible': can_touch(TbActivitySettings, self.crt_user),                 
                 }
            ]
        }
        ctx['named_ctx']= evalue_container( named_ctx )
        return ctx
    
    
    class tableCls(ModelTable):
        #hide_fields=['rules','content','componentname','componentparams','templateid','ismutex']
        fields_sort=['id','merchant','title','subtitle','enabled','categoryid','begintime','endtime','banner','image','target','displaytype','sort','remark','editorid','creatorid','createtime','edittime']
        model = TbActivityV2
        exclude=['url']
        pop_edit_fields = ['id']
        
        def inn_filter(self, query):
            if self.crt_user.merchant:
                query = query.filter(merchant_id = self.crt_user.merchant.id)
            return query
        
        def dict_head(self, head):
            dc={
                'id':60,
                'title':140,
                'begintime':140,
                'endtime':140,
                'banner':140,
                'image':140,
                'remark':100,
                'createtime':140,
                'edittime':140,
            }
            if dc.get(head['name']):
                head['width']=dc.get(head['name'])
                
            if head['name']=='id':
                head['editor']='com-table-switch-to-tab'
                head['tab_name']='activity_form'
                head['ctx_name']='activity_v2_tabs'
            return head
        
        def get_operation(self):
            operations = ModelTable.get_operation(self)[0:1]
            operations.extend([
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '启用',
                    #'field': 'status',
                    #'value': 1,
                    'pre_set':'rt={enabled:1}',
                    'row_match': 'many_row',
                    'confirm_msg': '确认修改为在线吗?', 
                    'visible': 'enabled' in self.permit.changeable_fields(),
                },
                {
                    'fun': 'selected_set_and_save',
                    'editor': 'com-op-btn',
                    'label': '禁用',
                    #'field': 'status',
                    #'value': 0,
                     'pre_set':'rt={enabled:0}',
                    'row_match': 'many_row',
                    'confirm_msg': '确认修改为离线吗?', 
                     'visible': 'enabled' in self.permit.changeable_fields(),
                },
                #{
                    #'fun': 'director_call',
                    #'director_name': 'update_activity_file_v2',
                    #'label': '更新缓存',
                    #'editor': 'com-op-btn', 
                     #'visible': has_permit(self.crt_user, 'TbActivityV2.update_cache'),
                          #},
                 {
                    'action':'cfg.show_load();ex.director_call("update_activity_file_v2",{merchant:%s}).then(()=>{cfg.hide_load()})'%self.crt_user.merchant.id if self.crt_user.merchant else '',
                    'label': '更新缓存',
                    'editor': 'com-op-btn', 
                     'visible': has_permit(self.crt_user, 'TbActivityV2.update_cache') and self.crt_user.merchant,
                  },
                  {
                    'action':'cfg.pop_vue_com("com-local-form-one",scope.head.fields_ctx).then(resp=>{cfg.show_load(); return ex.director_call("update_activity_file_v2",resp.row)}).then(()=>{cfg.hide_load()})',
                    'fields_ctx':{'title':'选择一个商户', **MerchantSelect().get_head_context()},
                    'label': '更新缓存',
                    'editor': 'com-op-btn', 
                     'visible': has_permit(self.crt_user, 'TbActivityV2.update_cache') and not self.crt_user.merchant,
                  },
            ])
            return operations       
        
        class sort(RowSort):
            names=['sort']
        
        class filters(RowFilter):
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['enabled']
                else:
                    return ['merchant','enabled']
            
        class search(RowSearch):
            names = ['title']
    
class ActivityV2Form(MerchantInstancCheck,ModelFields):
    
    @property
    def hide_fields(self):
        if self.crt_user.merchant:
            return ['merchant','creatorid','editorid']
        else:
            return ['creatorid','editorid']
        
    class Meta:
        model = TbActivityV2
        exclude=['url']
    
    def clean_dict(self, dc):
        if self.crt_user.merchant:
            dc['merchant'] = self.crt_user.merchant.id
        return dc
        
    def dict_head(self, head):
        if head['name']=='rules':
            head['editor']='com-field-richtext'
        if head['name']=='content':
            head['editor']='com-field-richtext'
        if head['name']=='banner':
            head['up_url'] = '/d/upload?path=public/images'      
        if head['name'] =='templateid':
            head['editor']='com-field-select'
            head['options']=[ {'value':0,'label':'缺省值'}]+[
                {'value':x.pk ,'label':str(x)} for x in TbActivityTemplate.objects.all()
            ]
        return head
    
    def clean_save(self):
        if not self.instance.templateid:
            self.instance.templateid=0
    
class ActivitySettingTable(ModelTable):
    model=TbActivitySettings
    exclude=[]
    hide_fields=['activityid']
    pop_edit_field='id'
    def inn_filter(self, query):
        return query.filter(activityid__id = self.kw.get('meta_par_pk'))
    
    def get_operation(self):
        ops = super().get_operation()
        for op in ops:
            if op['name']=='add_new':
                op['pre_set']='rt={activityid_id:scope.search_args.meta_par_pk}'
        return ops    

class ActivitySettingForm(ModelFields):
    hide_fields=['activityid']
    class Meta:
        model=TbActivitySettings
        exclude=[]
    
    def get_row(self):
        row = super().get_row()
        if self.kw.get('activityid') !=None:
            row['activityid'] = self.kw.get('activityid')    
        return row


#####################################
@director_view('update_activity_file_v2')
def update_activity_file_v2(merchant):
    has_download_url=[]
    merchant_inst = TbMerchants.objects.get(pk = merchant)
    root_path = os.path.join(settings.MEDIA_ROOT, 'public/%s/activityv2'%merchant_inst.merchantname)
    
    index_url = urljoin(settings.SELF_URL, '/actv2/index?merchant=%s'%merchant)
    spd = StaticHtmlBuilder(url= index_url, root_path= root_path,downloaded_urls=has_download_url)
    spd.run()
    
    index_url = urljoin(settings.SELF_URL, '/actv2/index1?merchant=%s'%merchant)
    spd = StaticHtmlBuilder(url= index_url, root_path= root_path,downloaded_urls=has_download_url)
    spd.run()    
    
    for itm in TbActivityV2.objects.filter(enabled=True):
        page_url =  urljoin(settings.SELF_URL, '/actv2/%s' % itm.pk )
        spd = StaticHtmlBuilder(url= page_url, root_path= root_path,downloaded_urls=has_download_url)
        spd.run()        
    sim_signal.send('activityv2.static.changed')
    return {'success':True}

  

director.update({
    'activity_v2':ActiviyV2Page.tableCls,
    'activity_v2.edit':ActivityV2Form,
    'activity_v2.setting':ActivitySettingTable,
    'activity_v2.setting.edit':ActivitySettingForm
})


page_dc.update({
    'activity_v2':ActiviyV2Page
})
