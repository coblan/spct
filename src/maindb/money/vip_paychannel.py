# encoding:utf-8
import json
from helpers.director.fields.fields import ModelFields
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from ..models import TbPaychanneljoinlevel, TbSetting, TbPaychannel


class VIPPayChannelPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值渠道'

    class tableCls(ModelTable):
        model = TbPaychanneljoinlevel
        exclude = []
        fields_sort = ['accountlevel', 'paychannelid']
        #pop_edit_field = 'levelname'
        def getExtraHead(self):
            return [
                {'name': 'accountlevel', 'label': '用户等级'},
                #{'name': 'channelid', 'label': '渠道ID'},
            ]

        def get_rows(self): 
            inst_list = TbPaychanneljoinlevel.objects.all()
            rows = []
            row_dc = {}
            for inst in inst_list:
                if inst.accountlevel not in row_dc:
                    row_dc[inst.accountlevel] = []
                row_dc[inst.accountlevel].append(inst.paychannelid_id)
            for k, v in row_dc.items():
                rows.append({'pk': k,'accountlevel': k, 'paychannelid': v, '_director_name': 'ChargeType.edit',})
            self.total = len(rows)
            return rows
        
        def getRowPages(self): 
            return {
                'total': self.total,
                'crt_page': 1,
                'perpage': self.search_args.get('_perpage', 20),
            }
        def dict_head(self, head):
            dc = {
                'id': 120,
                'accountlevel': 150,
                'paychannelid': 500
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            if head['name'] == 'accountlevel':
                form_obj = ChargeTypeForm(crt_user= self.crt_user)
                head['editor'] = 'com-table-pop-fields'
                head['get_row'] = {
                    'fun': 'get_table_row',
                }
                head['after_save'] = {
                    'fun': 'update_or_insert',
                }
                head['fields_ctx'] = form_obj.get_head_context()
                head['relat_field'] = 'accountlevel'
                head['inn_editor'] = 'com-table-mapper'
                head['options'] = getVipOptions()
                
            if head['name'] == 'paychannelid':
                head['show_tooltip'] = False
                head['editor'] = 'com-table-array-mapper'
                head['options'] = [{'value': x.paychannelid, 'label': x.channeltype} for x in TbPaychannel.objects.all()]
            return head

        #def dict_row(self, inst):
            #dc = {}
            #if not getattr(self, 'levels', None):
                #self.levels = json.loads(TbSetting.objects.get(settingname='Static:VIPTOTier').settingvalue)

            #for i in self.levels:
                #if i['VipLv'] == inst.accountlevel:
                    #dc['levelname'] = i['Memo']
                    #break

            #dc['channelid'] = inst.paychannelid.paychannelid
            #return dc

        #class filters(RowFilter):
            #names = ['accountlevel']

            #def dict_head(self, head):
                #if head['name']=='accountlevel':
                    #head['options']=getVipOptions()
                #return head


class ChargeTypeForm(ModelFields):
    field_sort = ['accountlevel', 'paychannelid']
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        self.kw = dc.copy()
        self.kw.update(kw)
        self.crt_user = crt_user
        self.nolimit = True
        self.custom_permit()
    
    def is_valid(self): 
        return True
    
    def get_row(self):
        accountlevel = self.kw.get('accountlevel')
        paychanel_list = []
        pk = None
        for relation in TbPaychanneljoinlevel.objects.filter(accountlevel = accountlevel):
            paychanel_list.append(relation.paychannelid_id)
            pk = accountlevel
        return {'pk': pk,'accountlevel': accountlevel, 'paychannelid': paychanel_list, '_director_name': 'ChargeType.edit',}

    class Meta:
        model = TbPaychanneljoinlevel
        exclude = []
    
    def get_heads(self): 
        heads = [
            {'name': 'accountlevel', 'label': '用户等级',}, 
            {'name': 'paychannelid','label': '渠道',}
        ]
        heads = [self.dict_head(head) for head in heads]
        return heads
    
    def getExtraHeads(self):
        channels = TbPaychannel.objects.all()
        options = [{'value': x.paychannelid, 'label': x.channeltype} for x in channels]
        # head['editor'] = 'field_multi_chosen'
        # head['placeholder'] = '请选择'
        # head['options'] = options
        return [{
            'name': 'paychannel', 'label': 'TbPaychannel', 'options': options, 'editor': 'field_multi_chosen'
        }]

    #def clean_dict(self, dc):
        #if dc.get('paychannelid'):
            #dc['paychannelid'] = int(dc['paychannelid'])
        #return dc

    def dict_head(self, head):
        if head['name'] == 'accountlevel':
            #head['editor'] = 'sim_select'
            head['editor'] = 'com-field-select'
            head['remote_options'] = 'get_no_relation_vip_level'
            head['required'] = True
            head['fv_rule'] = ''
            head['placeholder'] = '请选择' 
            head['options'] = []
            #head['options'] = getVipOptions()
        if head['name'] == 'paychannelid':
            head['required'] = True
            channels = TbPaychannel.objects.all()
            head['options'] = [{'value': x.paychannelid, 'label': x.channeltype} for x in channels] 
            head['editor'] = 'field_multi_chosen'
        return head

    def save_form(self):
        paychannelid_list =  [int(x) for x in self.kw['paychannelid'] ]
        for inst in  TbPaychanneljoinlevel.objects.filter(accountlevel=self.kw['accountlevel']):
            if inst.paychannelid_id not in paychannelid_list:
                inst.delete()
        for i in paychannelid_list:
            TbPaychanneljoinlevel.objects.update_or_create(accountlevel=self.kw['accountlevel'], paychannelid_id=i)
    
    def del_form(self): 
        accountlevel = self.kw.get('accountlevel')
        if accountlevel:
            TbPaychanneljoinlevel.objects.filter(accountlevel = accountlevel).delete()
      

def getVipOptions():
    level = TbSetting.objects.get(settingname='Static:VIPTOTier')
    level_dc = json.loads(level.settingvalue) 
    options = [{'value': x['VipLv'], 'label': x['Memo']} for x in level_dc ]       
    return options

def get_left_vip_options(**kw): 
    print(kw)
    crt_value = kw.get('crt_value')
    already = [x.accountlevel for x in TbPaychanneljoinlevel.objects.exclude(accountlevel = crt_value)]
    level = TbSetting.objects.get(settingname='Static:VIPTOTier')
    level_dc = json.loads(level.settingvalue) 
    options = [{'value': x['VipLv'], 'label': x['Memo']} for x in level_dc if x['VipLv'] not in already]  
    return options


director.update({
    'ChargeType': VIPPayChannelPage.tableCls,
    'ChargeType.edit': ChargeTypeForm, 
    'get_no_relation_vip_level': get_left_vip_options,
})

page_dc.update({
    'VIPPayChannel': VIPPayChannelPage,
})
