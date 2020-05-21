from helpers.director.shortcut import ModelTable,TablePage,director,page_dc,ModelFields,get_request_cache,RowFilter,RowSearch,director_view
from helpers.director.access.permit import can_touch

from maindb.models import TbMessage,TbMessageReceiver,TbMessagetype,TbAccount,TbMerchants
from django.utils.html import strip_tags
import jpush
from django.conf import settings
from helpers.func.collection.mylist import split_list
import re
import logging
operation_log = logging.getLogger('operation_log')

import requests
logger = logging.getLogger('jpush')
from jpush import common

class MyJpush(jpush.JPush):
    
    def __init__(self, key, secret, timeout=30, zone='default',proxy={}):
        super().__init__(key, secret, timeout, zone)
        self.proxy = proxy
    
    def _request(self, method, body, url, content_type=None, version=None, params=None):
        
        headers = {}
        headers['user-agent'] = 'jpush-api-python-client'
        headers['connection'] = 'keep-alive'
        headers['content-type'] = 'application/json;charset:utf-8'

        logger.debug("Making %s request to %s. Headers:\n\t%s\nBody:\n\t%s",
                     method, url, '\n\t'.join('%s: %s' % (key, value) for (key, value) in headers.items()), body)
        try:
            response = self.session.request(method, url, data=body, params=params,
                                            headers=headers, timeout=self.timeout,proxies=self.proxy )
        except requests.exceptions.ConnectTimeout:
            raise common.APIConnectionException("Connection to api.jpush.cn timed out.")
        except Exception:
            raise common.APIRequestException("Connection to api.jpush.cn error.")

        logger.debug("Received %s response. Headers:\n\t%s\nBody:\n\t%s", response.status_code, '\n\t'.join(
                '%s: %s' % (key, value) for (key, value) in response.headers.items()), response.content)

        if response.status_code == 401:
            raise common.Unauthorized("Please check your AppKey and Master Secret")
        elif not (200 <= response.status_code < 300):
            raise common.JPushFailure.from_response(response)
        return response
        

class MessagePage(TablePage):
    def get_label(self):
        return '消息推送'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    
    def get_context(self):
        ctx = super().get_context()
        named_ctx =  {
            'message_edit_tags':[
                {'name':'baseinfo',
                'label':'消息编辑',
                'com':'com-tab-fields-v1',
                'init_express':'ex.vueAssign(scope.row,scope.vc.par_row)',
                'after_save':'cfg.toast("操作成功sssss");scope.ps.update_or_insert(scope.row)',
                'fields_ctx':MessageForm().get_head_context(),
                'visible':can_touch(TbMessage,self.crt_user)
                },
            ]
        }
        ctx['named_ctx'] = named_ctx
        return ctx
    
    class tableCls(ModelTable):
        model = TbMessage
        exclude =[]
        #pop_edit_fields=['id']
        hide_fields = ['content','receivertype']
        
        def inn_filter(self, query):
            if self.crt_user.merchant:
                return query.filter(merchant = self.crt_user.merchant)
            else:
                return query
        
        def dict_head(self, head):
            width = {
                'title':160,
                'abstract':200,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            if head['name'] =='id':
                head['editor'] = 'com-table-switch-to-tab'
                head['ctx_name'] = 'message_edit_tags'
                head['tab_name'] = 'baseinfo'
            return head
        
        def get_operation(self):
            ops = super().get_operation()
            for op in ops:
                if op['name'] =='add_new':
                    op.update({
                         'tab_name': 'baseinfo',
                         'ctx_name': 'message_edit_tags',
                    })
            ops = [op for op in ops if op['name'] !='delete_selected']
            ops += [
                {'fun':'selected_set_and_save',
                 'editor':'com-op-btn',
                 'label':'删除',
                 'row_match':'many_row',
                 'pre_set':'rt = {status:0}'
                 }
            ]
            return ops
        
        class filters(RowFilter):
            @property
            def names(self):
                if self.crt_user.merchant:
                    return ['typeid','status']
                else:
                    return ['merchant','typeid','status']

        
        class search(RowSearch):
            names = ['title']
        
    
class MessageForm(ModelFields):
    
    @property
    def hide_fields(self):
        if self.crt_user.merchant:
            return ['merchant','issent','receivertype']
        else:
            return ['issent','receivertype']

    class Meta:
        model = TbMessage
        exclude =['sender','abstract']
    
    def clean_dict(self, dc):
        if dc.get('userids'):
            ls = re.split('[^\d]+',dc.get('userids'))
            ls = [x for x in ls if x !='']
            dc['userids'] = ';'.join(ls)
        if self.crt_user.merchant:
            dc['merchant'] = self.crt_user.merchant.id
        return dc
    
    def clean_save(self):
        if self.instance.typeid.needread == True:
            if not self.instance.userids and not self.instance.usergroupids and not self.instance.vipgroupids:
                raise UserWarning('非广播类型消息，必须选择筛选条件')
        if self.instance.userids and (self.instance.usergroupids or self.instance.vipgroupids) :
            raise UserWarning('选择[玩家id]后不能再选择[用户组别]和[VIP组别]')
        self.instance.sender = self.crt_user.username
        self.instance.abstract = strip_tags( self.instance.content)[:50]
        # 0 全部,1 用户ID,2 用户组别,3 vip组别,4 用户组别+vip组别
        if not self.instance.typeid.needread:
            self.instance.receivertype=0
        else:
            if self.instance.userids:
                self.instance.receivertype=1
            elif self.instance.usergroupids:
                if self.instance.vipgroupids:
                    self.instance.receivertype=4
                else:
                    self.instance.receivertype =2
            else:
                self.instance.receivertype =3
        

    #def after_save(self):
        #if self.instance.sendway ==0 :
            #self.instance.refresh_from_db()
            #if 'issent' in self.changed_data and self.instance.issent:
                #if self.instance. typeid . needread :
                    #send_user_message(self.instance)
                #else:
                    #broad_message(self.instance)
    
    def dict_head(self, head):
        if getattr(self,'allids',None) == None:
            self.allids = [x.pk for x in TbMessagetype.objects.filter(needread=False)]
        if head['name']=='sendtime':
            head['show']='scope.row.sendway ==1'
            head['required'] = True
        if head['name'] in ['userids','usergroupids','vipgroupids']:
            head['allids'] = self.allids
            head['show'] = '!ex.isin(scope.row.typeid,scope.head.allids)'
        if head['name'] == 'title':
            head['css'] = '.title-form input{width:400px !important}'
            head['class'] = 'title-form'
        if head['name'] == 'content':
            head['config']={
                'imageUploadUrl':'/d/ckeditor_image?save_path=public/images',
                'filebrowserImageUploadUrl':'/d/ckeditor_image?save_path=public/images',
            }
        return head
    
    def dict_row(self, inst):
        return {
            'sender':inst.sender,
            'abstract':inst.abstract,
            'createtime':inst.createtime,
        }
    
    def get_operations(self):
        ops = super().get_operations()
        ops+= [
            {'label':'立即推送',
             'editor':'com-field-op-btn',
             'class':'btn btn-warning btn-sm',
             'action':''' cfg.confirm("确认推送内容正确且已经保存,定时任务被手动推送后不会再被定时推送,确认要手动推送?")
             .then(()=>{cfg.show_load();return ex.director_call("do_push_message",{pk:scope.row.pk})})
             .then(()=>{cfg.hide_load();cfg.toast("推送命令发送成功！")})''' }
        ]
        return ops

@director_view('do_push_message')
def do_push_message(pk):
    try:
        instance = TbMessage.objects.get(pk = pk)
        if instance. typeid . needread :
            send_user_message(instance)
        else:
            broad_message(instance)
    
        dispatch_message(instance)
        instance.issent = True
        instance.save()
    except TbMessage.DoesNotExist:
        raise UserWarning('请先保存消息后，再推送消息。')
    
    
def send_user_message(inst):
    query =TbAccount.objects.all()
    if inst.userids:
        userids = inst.userids.split(';')
        query = query.filter(accountid__in = userids,)
    if inst.usergroupids:
        usergroupids = inst.usergroupids.split(';')
        query = query.filter(groupid_id__in = usergroupids,)
    if inst.vipgroupids:
        vipgroupids= inst.vipgroupids.split(';')
        query = query.filter(viplv__in =  vipgroupids,)
    userids = [str( account.accountid ) for account in query]
    jiguang_push_message(userids, inst ) #inst.title,inst.pk)

#def broad_message(inst):
    #jiguang_broad_message(inst)
  
def dispatch_message(inst):
    "写sql数据库，TbMessageReceiver,用户查询自己的消息列表"
    total_list =[]
    
    TbMessageReceiver.objects.filter(messageid = inst.pk) .delete()
    
    if inst.typeid . needread:
        if inst.userids:
            userids = inst.userids.split(';')
            reciever_insts = [TbMessageReceiver(messageid=inst.pk,receiverid = userid,receivertype=1, ) for userid in userids if userid !='']
            total_list += reciever_insts 
        if inst.usergroupids:
            groupids = inst.usergroupids.split(';')
            reciever_insts = [TbMessageReceiver(messageid=inst.pk,receiverid = groupid,receivertype=2, ) for groupid in groupids if groupid !='']
            total_list += reciever_insts 
        if inst.vipgroupids:
            vipgroupids = inst.vipgroupids.split(';')
            reciever_insts = [TbMessageReceiver(messageid=inst.pk,receiverid = groupid,receivertype=3, ) for groupid in vipgroupids if groupid !='']
            total_list += reciever_insts
    else:
        total_list.append(TbMessageReceiver(messageid=inst.pk,receiverid = 0,receivertype=0,))
    
    TbMessageReceiver.objects.bulk_create(total_list)

def broad_message(inst):
    merchantname = inst.merchant.merchantname
    push_cfg = settings.JPUSH.get(merchantname)
    msg,msgid = inst.title,inst.pk
    app_key,master_secret,proxy = push_cfg.get('app_key'),push_cfg.get('master_secret'),push_cfg.get('proxy') 
    _jpush = MyJpush(app_key, master_secret,proxy)
    push = _jpush.create_push()
    push.audience = jpush.all_
    #push.message =  jpush.message(msg_content='',extras= {'message_id':msgid} )
    android = jpush.android(alert=msg,extras={'message_id':msgid})
    ios = jpush.ios(alert=msg,extras={'message_id':msgid})
    push.notification = jpush.notification(alert= msg,android=android,ios=ios)
    push.options = {'apns_production':push_cfg.get('ios_production')}
    push.platform = jpush.all_
    
    operation_log.info('发送广播命令!')
    response=push.send()
    operation_log.info('广播消息返回结果: %s'%response)
    #print(response)
    
def jiguang_push_message(uids,inst) : # msg,msgid):
    merchantname = inst.merchant.merchantname
    push_cfg = settings.JPUSH.get(merchantname)
    msg,msgid = inst.title,inst.pk
    app_key,master_secret,proxy = push_cfg.get('app_key'),push_cfg.get('master_secret'),push_cfg.get('proxy') 
     
    #app_key,master_secret = settings.JPUSH.get('app_key'),settings.JPUSH.get('master_secret')
    for batch_uids in split_list(uids, 1000):
        _jpush = MyJpush(app_key, master_secret,proxy)
        push = _jpush.create_push()
        push.audience = jpush.audience(
                    jpush.alias(*batch_uids)
                )
        
        #push.message =  jpush.message(msg_content='',extras= {'message_id':msgid} )
        android = jpush.android(alert=msg,extras={'message_id':msgid})
        ios = jpush.ios(alert=msg,extras={'message_id':msgid},)
        push.notification = jpush.notification(alert= msg,android=android,ios=ios)
        push.options = {'apns_production':push_cfg.get('ios_production')}
        push.platform = jpush.all_
        try:
            operation_log.info('发送推送命令:uids=%s'%batch_uids)
            response=push.send()
            operation_log.info('推送消息:uids=%s ;返回结果: %s'%(batch_uids,response))
            #print(response)
        except jpush.common.JPushFailure as e:
            operation_log.info('推送消息:uids=%s ;返回结果报错: %s'%(batch_uids,e))
 
director.update({
    'message':MessagePage.tableCls,
    'message.edit':MessageForm,
})
    
page_dc.update({
    'message':MessagePage
})