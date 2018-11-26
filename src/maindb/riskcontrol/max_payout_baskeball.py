from .max_payout import MaxPayoutPage, MaxPayoutForm, MatchSelect, LeagueSelect
from ..models import TbMaxpayoutBasketball, TbMatchesBasketball, TbTournamentBasketball, TbOddstypegroup
from helpers.director.shortcut import page_dc, director, field_map, model_to_name
from helpers.director.model_func.field_procs.intBoolProc import IntBoolProc

class MaxPayoutBasketballPage(MaxPayoutPage):
    def get_label(self): 
        return '篮球最大赔付'
    class tableCls(MaxPayoutPage.tableCls):
        model = TbMaxpayoutBasketball
        exclude = ['updatetime']
        pop_edit_field = 'tid'
          

class MaxPayoutBasketballForm(MaxPayoutForm):
    class Meta:
        model = TbMaxpayoutBasketball
        exclude = ['createtime', 'updatetime']
    
    def dict_head(self, head):
        head = super().dict_head(head)
        if head['name'] == 'oddstypegroup':
            head['placeholder'] = '请选择'
            head['options'] = [{'value': x.pk, 'label': str(x)} for x in TbOddstypegroup.objects.filter(sportid = 1)]

        if head['name'] == 'tournamentid':
            table_obj = LeagueBasketballSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
            head['options'] = []

        if head['name'] == 'matchid':
            table_obj = MatchBasketballSelect(crt_user=self.crt_user)
            head['editor'] = 'com-field-pop-table-select'
            head['table_ctx'] = table_obj.get_head_context()
            head['options'] = []
        return head

class MatchBasketballSelect(MatchSelect):
    model = TbMatchesBasketball

class LeagueBasketballSelect(LeagueSelect):
    model = TbTournamentBasketball


field_map.update({
    model_to_name(TbMaxpayoutBasketball) + '.status': IntBoolProc,
})

director.update({
    'maxpayout_basketball': MaxPayoutBasketballPage.tableCls,
    'maxpayout_basketball.edit': MaxPayoutBasketballForm,
    'match_basketball.select': MatchBasketballSelect,
    'tourname_basketball.select': LeagueBasketballSelect,
    
    
})
page_dc.update({
    'maxpayout_basketball': MaxPayoutBasketballPage,
})