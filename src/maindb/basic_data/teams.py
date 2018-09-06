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
        return '球队资料'

    class tableCls(ModelTable):
        model = TbTeams
        exclue = []
        pop_edit_field = 'enname'
        fields_sort = ['enname', 'saenname', 'status', 'zhname', 'country', 'leaguename', 'icon']

        class filters(RowFilter):
            names = ['country', 'leaguename', 'status']

            def getExtraHead(self):
                return [
                    {
                        'name': 'leaguename',
                        'label': '联赛',
                        'editor': 'com-related-select-filter',
                        'options': [],
                        'related': 'country',
                        'director_name': 'league-filter', }
                ]

            def dict_head(self, head):
                head['order'] = True
                return head

            @staticmethod
            def getLeagueOptions( related): 
                contry = related  #kws.get('related')
                query = TbTeams.objects.filter(country = contry).values_list('leaguename', flat = True).distinct()
                options = [{ 'value':x,'label':str(x)} for x in query]
                return options

        class search(RowSearch):
            names = ['enname', 'saenname', 'zhname']

        class sort(RowSort):
            names = ['enname', 'zhname', 'saenname']

        def dict_head(self, head):
            dc = {
                'enname': 160,
                'saenname': 160,
                'leaguename': 150,
                'icon': 280,
            }
            if dc.get(head['name']):
                head['width'] = dc.get(head['name'])
            return head


class TeamsFields(ModelFields):
    class Meta:
        model = TbTeams
        exclude = []

    def save_form(self):
        super().save_form()
        if 'icon' in self.changed_data and self.cleaned_data.get('icon'):
            flPath = os.path.join(settings.MEDIA_ROOT, 'public', 'team_icon', self.cleaned_data.get('icon'))
            procImage(flPath)


class TeamIconProc(PictureProc):
    def to_dict(self, inst, name):
        value = getattr(inst, name, None)
        if value:
            out = '/media/public/team_icon/%(file_path)s' % {'file_path': value}
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
            mt = re.search('/media/public/team_icon/(.+)', value)
            if mt:
                return mt.group(1)
        else:
            return value

    def dict_field_head(self, head):
        head['editor'] = 'com-field-picture'
        head['up_url'] = '/d/upload?path=public/team_icon'
        return head


field_map[model_to_name(TbTeams) + '.icon'] = TeamIconProc

director.update({
    'maindb.teams': TeamsPage.tableCls,
    'maindb.teams.edit': TeamsFields,

    'league-filter': TeamsPage.tableCls.filters.getLeagueOptions,
})

page_dc.update({
    'maindb.teams': TeamsPage,
})
