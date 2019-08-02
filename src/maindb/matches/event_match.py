from helpers.director.shortcut import TablePage,PlainTable,page_dc,director,Fields,ModelTable
from maindb.mongoInstance import mydb
from maindb.models import TbMatch
from maindb.matches.matches import MatchsPage

class OtherWebMatchPage(TablePage):
    def get_label(self):
        return '三方比赛数据匹配'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(PlainTable):
        
        def __init__(self, *arg,**kws):
            super().__init__(*arg,**kws)
            self.filter_args={}
            if self.search_args.get('EventDate'):
                self.filter_args['EventDate'] = {'$regex' : ".*%s.*"%self.search_args.get('EventDate')}
            if self.search_args.get('LeagueZh'):
                self.filter_args['LeagueZh'] = {'$regex' : ".*%s.*"%self.search_args.get('LeagueZh')}
            if self.search_args.get('Team'):
                self.filter_args['$or'] = [{'Team1En':{'$regex' : ".*%s.*"%self.search_args.get('Team')}},
                                           {'Team2En':{'$regex' : ".*%s.*"%self.search_args.get('Team')}},
                                           {'Team1Zh':{'$regex' : ".*%s.*"%self.search_args.get('Team')}},
                                           {'Team2Zh':{'$regex' : ".*%s.*"%self.search_args.get('Team')}}]
  
        
        def get_heads(self):
            return [
                {'name':'Team1En','label':'主队英文名','editor':'com-table-click','width':130,
                 'fields_ctx':WebMatchForm().get_head_context(),
                 'action':"scope.head.fields_ctx.row=scope.row;cfg.pop_vue_com('com-form-one',scope.head.fields_ctx).then(row=>{ex.vueAssign(scope.row,row)})"},
                {'name':'Team1Zh','label':'主队中文名','editor':'com-table-span','width':130},
                {'name':'Team2En','label':'客队英文名','editor':'com-table-span','width':130},
                {'name':'Team2Zh','label':'客队英文名','editor':'com-table-span','width':130},
                {'name':'EventDate','label':'比赛日期','editor':'com-table-span','width':80},
                {'name':'LeagueZh','label':'联赛','editor':'com-table-span','width':120},
                {'name':"MatchID",'label':'比赛(比对结果)','editor':'com-table-label-shower','width':300},
            ]
        
        def get_rows(self):
            start_index = ( self.page -1 ) * self.perpage
            #for item in mydb['Event'].find(self.filter_args).sort('CreateTime',-1).skip(start_index).limit(self.perpage):
            rows =[]
            
            for item in mydb['Event'].find(self.filter_args).skip(start_index).limit(self.perpage):
                dc ={
                    '_director_name':'web_match_data.edit_self'
                }
                for k,v in item.items():
                    if k in ['Team1En','Team1Zh','Team2En','Team2Zh','MatchID','Eid','EventDate','LeagueZh']:
                        dc[k]=v
                rows.append(dc)
            
            matchid_list = [x.get('MatchID') for x in rows if x.get('MatchID')]
            dc ={}
            for inst in TbMatch.objects.filter(matchid__in=matchid_list):
                dc[inst.matchid] = str(inst)
            for row in rows:
                if row.get('MatchID'):
                    row['_MatchID_label'] = dc.get(row.get('MatchID'))
            return rows
        
        def getRowFilters(self):
            return [
                {'name':'Team','label':'球队名字','editor':'com-filter-text'},
                {'name':'EventDate','label':'日期','editor':'com-filter-text'},
                {'name':'LeagueZh','label':'联赛','editor':'com-filter-text'},
            ]
        
        def getRowPages(self):
            return {
                'crt_page':self.page,
                'total':mydb['Event'].find(self.filter_args).count(),
                'perpage':self.perpage,
            }
        

class WebMatchForm(Fields):
    def get_heads(self):
        return [
            {'name':'Team1En','label':'英文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team1Zh','label':'主队中文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team2En','label':'客队英文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team2Zh','label':'客队英文名','editor':'com-field-linetext','readonly':True},
            {'name':'MatchID','label':'比赛','editor':'com-field-pop-table-select',
             'table_ctx':MatchPicker().get_head_context(),'options':[]},
            
        ]
    
    
    def get_row(self):
        dc = mydb['Event'].find_one({'Eid':self.kw.get('Eid')})
        out_dc = {
             '_director_name':'web_match_data.edit_self'
        }
        for k,v in dc.items():
            if k in ['Team1En','Team1Zh','Team2En','Team2Zh','MatchID','Eid','EventDate','LeagueZh']:
                out_dc[k]=v
            if out_dc.get('MatchID'):
                inst = TbMatch.objects.get(matchid=out_dc.get('MatchID') )
                out_dc.update({
                    '_MatchID_label':str(inst)
                })
                
        return out_dc
    
    def save_form(self):
        dc = {'MatchID':self.kw.get('MatchID')}
        mydb['Event'].update({'Eid':self.kw.get('Eid')}, {'$set': dc})
        

class MatchPicker(MatchsPage.tableCls):
    def dict_head(self, head):
        head = super().dict_head(head)
        if head['name'] =='matchid':
            head['editor'] ='com-table-foreign-click-select'
        return head
    
    def get_operation(self):
        return []


director.update({
    'web_match_data':OtherWebMatchPage.tableCls,
    'web_match_data.edit_self':WebMatchForm,
    'matchpicker':MatchPicker
})

page_dc.update({
    'web_match_data':OtherWebMatchPage
})