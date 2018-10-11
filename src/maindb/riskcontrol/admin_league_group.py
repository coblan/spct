from helpers.director.shortcut import TablePage, ModelFields, ModelTable, page_dc, director, Fields
from ..models import TbLeagueGroup, TbLeagueidInGroup,TbLeagueGroupSpread, TbTournament, TbOddstypegroup
from django.utils.translation import ugettext as _
from urllib.parse import urljoin
from django.conf import settings
import requests
import json
from django.core.exceptions import ValidationError

class LeagueGroupPage(TablePage):
    template = 'jb_admin/table.html'
    def get_label(self): 
        return '联赛组'
    
    class tableCls(ModelTable):
        model = TbLeagueGroup
        exclude = ['id', 'enabled']
        
        def dict_head(self, head): 
            if head['name'] == 'groupname':
                head['editor'] = 'com-table-switch-to-tab'
                head['tab_name'] = 'baseinfo'
                head['width'] = 200
            return head
        
        def get_operation(self): 
            ops = super().get_operation()
            for op in ops:
                if op['name'] == 'add_new':
                    op['tab_name'] = 'baseinfo'
            return ops[0:1]
                
        
    
    def get_context(self): 
        ctx = super().get_context()
        baseinfo = LeagueGroupForm(crt_user= self.crt_user)
        leagueingroup_form = LeagueidInGroupForm(crt_user = self.crt_user)
        spreadform = LeagueGroupSpreadForm(crt_user= self.crt_user)
        ls = [
              {'name': 'baseinfo',
               'label': _('Basic Info'),
               'com': 'com_tab_fields',
               'get_data': {
                   'fun': 'get_row',
                   'kws': {
                       'director_name': baseinfo.get_director_name(),
                       'relat_field': 'groupid',
                   }
               },
               'after_save': {
                   'fun':  'update_or_insert'#'update_or_insert'
               },
               'heads': baseinfo.get_heads(),
               'ops': baseinfo.get_operations()
               },  
              
              {'name': 'league_list',
               'label': '联赛列表',
               'com': 'com_tab_fields',
               'get_data': {
                   'fun': 'get_row',
                   'kws': {
                       'director_name': leagueingroup_form.get_director_name(),
                       'relat_field': 'groupid',
                   }
               },
               'after_save': {
                   'fun':  'update_or_insert'#'update_or_insert'
               },
               'heads': leagueingroup_form.get_heads(),
               'ops': leagueingroup_form.get_operations(), 
               'show': 'groupid!=null',
               },               
              {'name': 'spreadform',
               'label':'水位',
               'com': 'com_tab_fields',
               'get_data': {
                   'fun': 'get_row',
                   'kws': {
                       'director_name': spreadform.get_director_name(),
                       'relat_field': 'groupid',
                   }
               },
               'after_save': {
                   'fun':  'do_nothing' #'update_or_insert'
               },
               'heads': spreadform.get_heads(),
               'ops': spreadform.get_operations(), 
               'show': 'groupid!=null',
               },               
              
        ]
        ctx['tabs'] = ls
        return ctx
        
class LeagueGroupForm(ModelFields):
    readonly = ['groupid']
    class Meta:
        model = TbLeagueGroup
        exclude = ['enabled']
    
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        if kw.get('groupid'):
            inst = TbLeagueGroup.objects.get(groupid = kw.get('groupid'))
            pk = inst.pk
        super().__init__(dc, pk, crt_user, nolimit, *args, **kw)    
    
    def dict_head(self, head): 
        if head['name'] == 'groupname':
            head['readonly'] = 'scope.row.groupid!=null'
        return head
    
    def save_form(self): 
        url = urljoin( settings.SPREAD_SERVICE, 'spread/group/create')
        rt = requests.post(url, json = {"groupName":self.instance.groupname})
        print(rt.text)
        rt_dc = json.loads(rt.text)
        if not rt_dc.get('success'):
            raise ValidationError({'groupname': rt_dc.get('error')} )
        self.instance.groupid = rt_dc.get('data')
        self.instance.save()


class LeagueidInGroupForm(Fields):
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        super().__init__(dc, pk, crt_user, nolimit, *args, **kw)     
        if self.kw.get('groupid'):
            
            self.league_list = [x.leagueid for x in TbLeagueidInGroup.objects.filter(groupid = self.kw.get('groupid'))]
        else:
            self.league_list = []
        
    
    def get_row(self): 
        self.league_list = [x.leagueid for x in TbLeagueidInGroup.objects.filter(groupid = self.kw.get('groupid'))]
        group = TbLeagueGroup.objects.get(groupid = self.kw.get('groupid'))
        return {
            'pk': group.pk,
            'groupid': self.kw.get('groupid'),
            'league_list': self.league_list,
            '_director_name': self.get_director_name(),
        }
    
    
    def get_heads(self):
        options =  TbTournament.objects.all()
        return [
            {'name': 'league_list','label': '联赛列表','editor': 'field_multi_chosen','style': 'width:300px',
             'options': [{'value': x.tournamentid, 'label': str(x),} for x in options]
             }
            ]
    
    def save_form(self): 
        new_league_list = [int(x) for x in self.kw.get('league_list')]
        new_in = []
        
        for k in new_league_list:
            if k not in self.league_list:
                new_in.append(k)
        new_out = [x for x in self.league_list if x not in new_league_list]
        
        new_in_obj = [TbLeagueidInGroup(groupid = self.kw.get('groupid'), leagueid = x) for x in new_in]
        TbLeagueidInGroup.objects.bulk_create(new_in_obj)
        TbLeagueidInGroup.objects.filter(leagueid__in = new_out).delete()
        
        url = urljoin(settings.SPREAD_SERVICE, 'spread/group/league')
        group = TbLeagueGroup.objects.get(groupid = self.kw.get('groupid'))
        rt = requests.post(url, json = {"groupName":group.groupname,"leagueGroupId":self.kw.get('groupid'),"leagueIds":new_league_list})
        self.save_log({'model': 'TbLeagueidInGroup', 'service_return': rt.text, 'leagueIds': new_league_list,})
        

class LeagueGroupSpreadForm(Fields):
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        super().__init__(dc, pk, crt_user, nolimit, *args, **kw)     
        self.oddstypes = TbOddstypegroup.objects.all().order_by('periodtype')
        if self.kw.get('groupid'):
            pass
        
    def get_row(self): 
        hased_data = {'%s__%s' % (x.periodtype, x.bettype): x.spread for x in TbLeagueGroupSpread.objects.filter(groupid = self.kw.get('groupid'))} 
        dc = {
            'groupid': self.kw.get('groupid'),
            '_director_name': self.get_director_name(),
        }
        dc.update(hased_data)
        return dc
    
    def get_heads(self): 
        heads = [{'name': '%s__%s' % (x.periodtype, x.bettype), 'label': x.oddstypenamezh, 
                  'editor': 'number', 'step': 0.01, 'min': 0, 'max': 1, 'fv_rule': 'range(0~1)',} for x in self.oddstypes]
        return heads
    
    def save_form(self): 
        spreads = []
        for x in self.oddstypes:
            name =  '%s__%s' % (x.periodtype, x.bettype)
            if self.kw.get(name) or self.kw.get(name) == 0:
                TbLeagueGroupSpread.objects.update_or_create(groupid = self.kw.get('groupid'), periodtype = x.periodtype, bettype = x.bettype , defaults = {'spread': self.kw.get(name) })
                spreads.append({
                    "betType":x.bettype,
                    "periodType":x.periodtype,
                    "spread":self.kw.get(name)
                })
                
                #TbLeagueGroupSpread.objects.update_or_create( spread = self.kw.get(name), defaults = {'groupid' : self.kw.get('groupid'), 'periodtype' : x.periodtype, 'bettype' : x.bettype,})
        url = urljoin(settings.SPREAD_SERVICE, 'spread/set/group')
        rt = requests.post(url, json = {'leagueGroupId': self.kw.get('groupid'), 'spreads': spreads,})
        self.save_log({'model': 'TbLeagueGroupSpread', 'service_return': rt.text, 'spreads': spreads,})
            

director.update({
    'LeagueGroupPage': LeagueGroupPage.tableCls,
    'LeagueGroupPage.edit': LeagueGroupForm,
    
    'LeagueidInGroupForm': LeagueidInGroupForm,
    'LeagueGroupSpreadForm': LeagueGroupSpreadForm,
    
    
})
page_dc.update({
    'LeagueGroupPage': LeagueGroupPage,
    
})