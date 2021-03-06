# encoding:utf-8
from __future__ import unicode_literals
from django.contrib import admin
from helpers.director.shortcut import TablePage, ModelTable, model_dc, page_dc, ModelFields, FieldsPage, \
    TabPage, RowSearch, RowSort, RowFilter, field_map, model_to_name
from helpers.director.model_func.dictfy import model_to_name
from maindb.models import TbTeams
from maindb.status_code import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import re
from django.conf import settings
from helpers.director.base_data import director
from helpers.maintenance.update_static_timestamp import js_stamp_dc
from helpers.director.model_func.cus_fields.cus_picture import PictureProc
import os
from maindb.marketing.proc_image import procImage


class TeamsPage(TablePage):
    template = 'jb_admin/table.html'

    def get_label(self):
        return '足球队资料'

    class tableCls(ModelTable):
        model = TbTeams
        exclue = []
        pop_edit_field = 'enname'
        fields_sort = ['enname', 'saenname', 'status', 'zhname', 'country', 'leaguename', 'icon']

        def get_operation(self):
            return [super().get_operation()[0]]
        
        def dict_head(self, head):
            dc = {
                'enname': 160,
                'saenname': 160,
                'leaguename': 150,
                'icon': 280,
                'zhname':150
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head

        class filters(RowFilter):
            names = ['country', 'status']
            fields_sort=['country', 'leaguename', 'status']

            def getExtraHead(self):
                return [
                    {
                        'name': 'leaguename',
                        'placeholder': '联赛',
                        #'editor': 'com-related-select-filter',
                        'editor': 'com-filter-select',
                        'options': [],
                        #'related': 'country',
                        'director_name': 'league-options', 
                        #'update_options_on': ['row.update_or_insert', 'country.changed'],
                        #'clear_value_on': ['country.changed'], # 清除一下，否则 由于当前选中的是别的联赛，新来的联赛不能匹配。
                        'event_slots':[
                            {'par_event':'country.changed','express':'rt=scope.vc.get_options({post_data:{country:scope.event} })'},
                            {'par_event':'country.changed','express':'rt=scope.vc.clear_value()'},
                           
                        ]
                    }
                ]

            def dict_head(self, head):
                head['order'] = True
                if head['name'] == 'country':
                    head['event_slots']=[
                        {'event':'input','express':'scope.ps.$emit("country.changed",scope.event)'},
                        {'par_event':'row.update_or_insert','express':'rt=scope.vc.clear_value()'},
                        {'par_event':'row.update_or_insert','express':'rt=scope.vc.get_options({post_data:{} })'},
                        
                        
                        #{'par_event':'row.update_or_insert','express':'rt=scope.vc.get_options({post_data:{} })'},
                        
                    ]
                    #head['update_options_on'] = 'row.update_or_insert'
                    #head['on_changed_express'] = 'scope.ps.$emit("country.changed",scope.value)'
                    head['director_name'] = 'contry-options'
                return head
            
            @staticmethod  # contry-options
            def getCountry(**kws): 
                query = TbTeams.objects.values('country').distinct()
                options = [{'value': x.get('country'), 'label': x.get('country')} for x in query]
                return options
            
            @staticmethod
            def getLeagueOptions(country):
                #country = search_args.get('country')
                #contry = related  # kws.get('related')
                query = TbTeams.objects.filter(country=country).values_list('leaguename', flat=True).distinct()
                options = [{'value': x, 'label': str(x)} for x in query]
                return options

        class search(RowSearch):
            names = ['enname', 'saenname', 'zhname']

        class sort(RowSort):
            names = ['enname', 'zhname', 'saenname']




class TeamsFields(ModelFields):
    icon_dir='team_icon'
    class Meta:
        model = TbTeams
        exclude = []
    
    #def dict_head(self, head): 
        #if head['name'] == 'enname':
            #head['fv_rule'] = 'length(~20)'
        #return head

    def save_form(self):
        super().save_form()
        if 'icon' in self.changed_data and self.cleaned_data.get('icon'):
            flPath = os.path.join(settings.MEDIA_ROOT, 'public', self.icon_dir, self.cleaned_data.get('icon'))
            procImage(flPath)


class TeamIconProc(PictureProc):
    icon_dir='team_icon'
    def to_dict(self, inst, name):
        value = getattr(inst, name, None)
        if value:
            out = '/media/public/%(icon_dir)s/%(file_path)s' % {'icon_dir':self.icon_dir,'file_path': value}
        else:
            out = value
        return {
            name: out
        }

    def clean_field(self, dc, name):
        """
        """
        value = dc.get(name)
        if value:
            mt = re.search('/media/public/%(icon_dir)s/(.+)'%{'icon_dir':self.icon_dir}, value)
            if mt:
                return mt.group(1)
        else:
            return value

    def dict_field_head(self, head):
        head['editor'] = 'com-field-picture'
        head['up_url'] = '/d/upload?path=public/%(icon_dir)s'%{'icon_dir':self.icon_dir}
        return head


field_map[model_to_name(TbTeams) + '.icon'] = TeamIconProc

director.update({
    'maindb.teams': TeamsPage.tableCls,
    'maindb.teams.edit': TeamsFields,

    'league-options': TeamsPage.tableCls.filters.getLeagueOptions,
    'contry-options': TeamsPage.tableCls.filters.getCountry,
})

page_dc.update({
    'teams': TeamsPage,
})
