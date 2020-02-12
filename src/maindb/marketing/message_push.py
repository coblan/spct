from helpers.director.shortcut import ModelTable,TablePage,director,page_dc,ModelFields
from maindb.models import TbMessage,TbMessageReceiver,TbMessagetype,TbAccount
from django.utils.html import strip_tags
import jpush
from django.conf import settings

class MessagePage(TablePage):
    def get_label(self):
        return '消息推送'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbMessage
        exclude =[]
        pop_edit_fields=['id']
        hide_fields = ['content']
        
    
class MessageForm(ModelFields):

    class Meta:
        model = TbMessage
        exclude =['sender','abstract']
    
    def clean_save(self):
        self.instance.sender = self.crt_user.username
        self.instance.abstract = strip_tags( self.instance.content)[:50]

    def after_save(self):
        if self.instance.sendway ==0 :
            if 'issent' in self.changed_data and self.instance.issent:
                if self.instance. typeid . needread :
                    send_user_message(self.instance)
                else:
                    broad_message(self.instance)
    
    def dict_head(self, head):
        if getattr(self,'allids',None) == None:
            self.allids = [x.pk for x in TbMessagetype.objects.filter(needread=False)]
        if head['name']=='sendtime':
            head['show']='scope.row.sendway ==1'
            head['required'] = True
        if head['name'] in ['userids','usergroupids','vipgroupids']:
            head['allids'] = self.allids
            head['show'] = '!ex.isin(scope.row.typeid,scope.head.allids)'
        return head
    
    def dict_row(self, inst):
        return {
            'sender':inst.sender,
            'abstract':inst.abstract,
        }
    
    
def send_user_message(inst):
    dispatch_message(inst)
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
    userids = [account.accountid for account in query]
    jiguang_push_message(userids, inst.title)

def broad_message(inst):
    jiguang_broad_message(inst.msg)
  
def dispatch_message(inst):
    total_list =[]
    if inst.userids:
        userids = inst.userids.split(';')
        reciever_insts = [TbMessageReceiver(messageid=inst.pk,receiverid = userid,receivertype=1, ) for userid in userids]
        total_list.append(reciever_insts)
    if inst.usergroupids:
        groupids = inst.usergroupids
        reciever_insts = [TbMessageReceiver(messageid=inst.pk,receiverid = groupid,receivertype=2, ) for groupid in groupids]
        total_list.append(reciever_insts)
    if inst.vipgroupids:
        vipgroupids = inst.vipgroupids
        reciever_insts = [TbMessageReceiver(messageid=inst.pk,receiverid = groupid,receivertype=3, ) for groupid in vipgroupids]
        total_list.append(reciever_insts)
        
    TbMessageReceiver.objects.bulk_create(total_list)

def jiguang_broad_message(msg):
    app_key,master_secret = settings.JPUSH.get('app_key'),settings.JPUSH.get('master_secret')
    _jpush = jpush.JPush(app_key, master_secret)
    push = _jpush.create_push()
    #single_payload_list = [
        #{'platform':'all', "audience" : "all", 'notification':{'alert':msg}},
        ##{'platform':'all', 'target':'regid2', 'notification':{'alert':'alert content'}}
    #]
    #response = push.batch_push_by_regid(single_payload_list)
    push.audience = jpush.all_
    push.notification = jpush.notification(alert=msg)
    push.platform = jpush.all_
    response=push.send()
    print(response)
    
def jiguang_push_message(uids,msg):
    app_key,master_secret = settings.JPUSH.get('app_key'),settings.JPUSH.get('master_secret')
    _jpush = jpush.JPush(app_key, master_secret)
    push = _jpush.create_push()
    #single_payload_list = [
        #{'platform':'all', 'audience':{'alias':uids}, 'notification':{'alert':msg}},
        ##{'platform':'all', 'target':'regid2', 'notification':{'alert':'alert content'}}
    #]
    #response = push.batch_push_by_regid(single_payload_list)
    
    push.audience = jpush.audience(
                jpush.alias(*uids)
            )
    push.notification = jpush.notification(alert=msg)
    push.platform = jpush.all_
    response=push.send()
    
    print(response)
 
director.update({
    'message':MessagePage.tableCls,
    'message.edit':MessageForm,
})
    
page_dc.update({
    'message':MessagePage
})