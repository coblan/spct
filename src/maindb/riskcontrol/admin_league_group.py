from helpers.director.shortcut import TablePage, ModelFields, ModelTable, page_dc, director, Fields,director_view
from ..models import TbLeagueGroup, TbLeagueidInGroup,TbLeagueGroupSpread, TbTournament, TbOddstypegroup,TbSporttypes
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
                head['ctx_name'] = 'leaguegroup_tabs'
                head['width'] = 200
            return head
        
        def get_operation(self): 
            ops = super().get_operation()
            for op in ops:
                if op['name'] == 'add_new':
                    op['tab_name'] = 'baseinfo'
                    op['ctx_name'] = 'leaguegroup_tabs'
            return ops[0:1]
                
        
    
    def get_context(self): 
        ctx = super().get_context()
        ctx['named_ctx'] = self.get_tabs()
        #ctx['tabs'] = ls
        return ctx
    
    def get_tabs(self): 
        baseinfo = LeagueGroupForm(crt_user= self.crt_user)
        leagueingroup_form = LeagueidInGroupForm(crt_user = self.crt_user)
        spreadform = LeagueGroupSpreadForm(crt_user= self.crt_user)
        ls = [
              {'name': 'baseinfo',
               'label': _('Basic Info'),
               'com': 'com-tab-fields',
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
               'com': 'com-tab-fields',
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
               'show': 'scope.par_row.groupid!=null',
               },               
              {'name': 'spreadform',
               'label':'水位',
               'com': 'com-tab-fields',
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
               'show': 'scope.par_row.groupid!=null',
               },               
              
        ]
        return {
            'leaguegroup_tabs': ls,
        }
        
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
        # 如果有groupid了，就不能再去请求service了
        if self.instance.groupid:
            return
        
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
        #options =  TbTournament.objects.all()
        return [
            {'name': 'league_list',
             'label': '联赛列表',
             'required':True,
             'validate_showError':'rt=cfg.showError(scope.msg)',
             #'editor': 'field_multi_chosen',
             'editor':'com-field-multi-chosen',
             'style': 'width:300px',
             'options':[],
             'director_name':'league_group.league_options',
             'event_slots':[
                  {'par_event':'row.update_or_insert','express':'rt=scope.vc.update_options({row:scope.event})'},
             ]
             #'options': [{'value': x.tournamentid, 'label': str(x),} for x in options]
             }
            ]
    
    def clean(self):
        super().clean()
        new_league_list = [int(x) for x in self.kw.get('league_list')]
        new_in = []
        
        source = TbSporttypes.objects.get(sportid=0,enabled=1).source
        
        for k in new_league_list:
            if k not in self.league_list:
                new_in.append(k)
        
        old_overlap=[]
        for tie in TbLeagueidInGroup.objects.filter(leagueid__in=new_league_list).extra(select={'label':'SELECT TB_Tournament.TournamentName '},tables=['TB_Tournament'],where=['TB_Tournament.TournamentID =TB_LeagueId_In_Group.LeagueId','TB_Tournament.Source=%s'%source])\
            .exclude(groupid=self.kw.get('groupid')):
            old_overlap.append('【%s】'%tie.label)
        if old_overlap:
            #raise UserWarning(','.join(old_overlap)+' 已经包含在其他联赛组中')
            self.add_error('league_list',','.join(old_overlap)+' 已经被其他联赛组选中')
        self.new_in =new_in
        if TbLeagueidInGroup.objects.filter(leagueid__in=new_in).exists():
            self.add_error('league_list', '新选择的联赛已经被其他联赛组选中')
        self.new_out = [x for x in self.league_list if x not in new_league_list]
        self.new_league_list = new_league_list
    
    def save_form(self): 
        
        new_in_obj = [TbLeagueidInGroup(groupid = self.kw.get('groupid'), leagueid = x) for x in self.new_in]
        TbLeagueidInGroup.objects.bulk_create(new_in_obj)
        TbLeagueidInGroup.objects.filter(leagueid__in = self.new_out).delete()
        abslate_league_tie = TbLeagueidInGroup.objects.raw(r'SELECT a.* FROM TB_LeagueId_In_Group a LEFT JOIN TB_Tournament b ON a.LeagueId=b.TournamentID WHERE b.TournamentID is NULL AND a.GroupId=%s'%self.kw.get('groupid'))
        for tie in abslate_league_tie:
            tie.delete()
        
        url = urljoin(settings.SPREAD_SERVICE, 'spread/group/league')
        group = TbLeagueGroup.objects.get(groupid = self.kw.get('groupid'))
        rt = requests.post(url, json = {"groupName":group.groupname,"leagueGroupId":self.kw.get('groupid'),"leagueIds":self.new_league_list})
        self.save_log({'model': 'TbLeagueidInGroup', 'service_return': rt.text, 'leagueIds': self.new_league_list,})
        
@director_view('league_group.league_options')
def league_options(row):
    source = TbSporttypes.objects.get(sportid=0,enabled=1).source
    
    exclude_league =[]
    already_include_league=[]
    
    for tie in TbLeagueidInGroup.objects.all():
        if tie.groupid == row.get('groupid'):
            already_include_league.append(tie.leagueid)
        else:
            exclude_league.append(tie.leagueid)
    exclude_league = list(set(exclude_league)-set(already_include_league))

    options = TbTournament.objects.filter(source=source).exclude(tournamentid__in=exclude_league).order_by('tournamentname')

    #[x.leagueid for x in TbLeagueidInGroup.objects.filter(groupid = row.get('groupid'))]
    #print('here')
    return [{'value': x.tournamentid, 'label': str(x),} for x in options]

class LeagueGroupSpreadForm(Fields):
    def __init__(self, dc={}, pk=None, crt_user=None, nolimit=False, *args, **kw): 
        super().__init__(dc, pk, crt_user, nolimit, *args, **kw)     
        self.oddstypes = TbOddstypegroup.objects.filter(sportid=0,isspecial=0).order_by('periodtype')
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