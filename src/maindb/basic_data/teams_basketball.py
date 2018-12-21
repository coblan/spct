from helpers.director.shortcut import page_dc,director,ModelFields,field_map,model_to_name,RowFilter,director_view
from ..models import TbTeamsBasketball
from .teams import TeamsPage,TeamIconProc
import os

class TeamBasketballPage(TeamsPage):
    def get_label(self):
        return '篮球队资料'
    
    class tableCls(TeamsPage.tableCls):
        model=TbTeamsBasketball
        
        class filters(RowFilter):
            names = ['country','leaguename', 'status']
            fields_sort=['country', 'leaguename', 'status']
    
            def getExtraHead(self):
                return [
                    {
                        'name': 'leaguename',
                        'label': '联赛',
                        #'editor': 'com-related-select-filter',
                        'editor': 'com-filter-select',
                        'options': [],
                        #'related': 'country',
                        'director_name': 'basketball-league-options', 
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
                        {'event':'input','express':'scope.ts.$emit("country.changed",scope.event)'},
                        {'par_event':'row.update_or_insert','express':'rt=scope.vc.get_options({post_data:{} })'},
                        
                        #{'par_event':'row.update_or_insert','express':'rt=scope.vc.get_options({post_data:{} })'},
                        
                    ]
                    #head['update_options_on'] = 'row.update_or_insert'
                    #head['on_changed_express'] = 'scope.ts.$emit("country.changed",scope.value)'
                    head['director_name'] = 'basketball-contry-options'
                return head
        
@director_view('basketball-contry-options')  # contry-options
def getCountry(**kws): 
    query = TbTeamsBasketball.objects.values('country').distinct()
    options = [{'value': x.get('country'), 'label': x.get('country')} for x in query]
    return options

@director_view('basketball-league-options')
def getLeagueOptions(country):
    #country = search_args.get('country')
    #contry = related  # kws.get('related')
    query = TbTeamsBasketball.objects.filter(country=country).values_list('leaguename', flat=True).distinct()
    options = [{'value': x, 'label': str(x)} for x in query]
    return options


class TeamsBasketballFields(ModelFields):
    class Meta:
        model = TbTeamsBasketball
        exclude = []
    
    def dict_head(self, head): 
        if head['name'] == 'enname':
            head['fv_rule'] = 'length(~50)'
        return head

    def save_form(self):
        super().save_form()
        if 'icon' in self.changed_data and self.cleaned_data.get('icon'):
            flPath = os.path.join(settings.MEDIA_ROOT, 'public', 'team_basketball_icon', self.cleaned_data.get('icon'))
            procImage(flPath)


class TeamBasketballIconProc(TeamIconProc):
    icon_dir='team_basketball_icon'


field_map[model_to_name(TbTeamsBasketball) + '.icon'] = TeamBasketballIconProc


director.update({
    'teams_basketball':TeamBasketballPage.tableCls,
    'teams_basketball.edit':TeamsBasketballFields
    
})

page_dc.update({
    'teams_basketball': TeamBasketballPage,
})