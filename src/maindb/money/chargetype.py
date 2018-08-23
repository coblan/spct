# encoding:utf-8
import json
from helpers.director.fields.fields import ModelFields
from helpers.director.shortcut import TablePage, ModelTable, page_dc, director, RowFilter
from ..models import TbPaychanneljoinlevel, TbSetting, TbPaychannel


class ChargeTypePage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '充值渠道'

    class tableCls(ModelTable):
        model = TbPaychanneljoinlevel
        exclude = []
        fields_sort = ['tid', 'levelname', 'channelid', 'paychannelid']

        def getExtraHead(self):
            return [
                {'name': 'levelname', 'label': '用户等级'},
                {'name': 'channelid', 'label': '渠道ID'},
            ]

        def dict_head(self, head):
            dc = {
                'id': 120,
                'levelname': 150,
                'paychannelid': 150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        def dict_row(self, inst):
            dc = {}
            if not getattr(self, 'levels', None):
                self.levels = json.loads(TbSetting.objects.get(settingname='Static:VIPTOTier').settingvalue)

            for i in self.levels:
                if i['VipLv'] == inst.accountlevel:
                    dc['levelname'] = i['Memo']
                    break

            dc['channelid'] = inst.paychannelid.paychannelid
            return dc

        class filters(RowFilter):
            names = ['accountlevel']

            def dict_head(self, head):
                if head['name']=='accountlevel':
                    head['options']=getVipOptions()
                return head


class ChargeTypeForm(ModelFields):
    field_sort = ['accountlevel', 'paychannel']

    class Meta:
        model = TbPaychanneljoinlevel
        exclude = ['channelname', 'channeltype', 'levelname', 'paychannelid']

    def getExtraHeads(self):
        channels = TbPaychannel.objects.all()
        options = [{'value': x.paychannelid, 'label': x.channeltype} for x in channels]
        # head['editor'] = 'field_multi_chosen'
        # head['placeholder'] = '请选择'
        # head['options'] = options
        return [{
            'name': 'paychannel', 'label': 'TbPaychannel', 'options': options, 'editor': 'field_multi_chosen'
        }]

    def clean_dict(self, dc):
        if dc.get('paychannelid'):
            dc['paychannelid'] = int(dc['paychannelid'])
        return dc

    def dict_head(self, head):
        if head['name'] == 'accountlevel':
            head['editor'] = 'sim_select'
            head['fv_rule'] = ''
            head['placeholder'] = '请选择' 
            head['options'] = getVipOptions()

        return head

    def save_form(self):
        for i in self.kw['paychannel']:
            TbPaychanneljoinlevel.objects.update_or_create(accountlevel=self.kw['accountlevel'], paychannelid_id=i)
        return self.instance

def getVipOptions():
    level = TbSetting.objects.get(settingname='Static:VIPTOTier')
    level_dc = json.loads(level.settingvalue)
    options = [{'value': x['VipLv'], 'label': x['Memo']} for x in level_dc]
    return options

director.update({
    'ChargeType': ChargeTypePage.tableCls,
    'ChargeType.edit': ChargeTypeForm
})

page_dc.update({
    'ChargeType': ChargeTypePage,
})
