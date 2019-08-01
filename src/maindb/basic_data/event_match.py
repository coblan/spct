from helpers.director.shortcut import TablePage,PlainTable,page_dc,director,Fields
from maindb.mongoInstance import mydb

class OtherWebMatchPage(TablePage):
    def get_label(self):
        return '三方比赛数据匹配'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(PlainTable):
        def get_heads(self):
            return [
                {'name':'Team1En','label':'主队英文名','editor':'com-table-click','width':130,
                 'fields_ctx':WebMatchForm().get_head_context(),
                 'action':"scope.head.fields_ctx.row=scope.row;cfg.pop_vue_com('com-form-one',scope.head.fields_ctx)"},
                {'name':'Team1Zh','label':'主队中文名','editor':'com-table-span','width':130},
                {'name':'Team2En','label':'客队英文名','editor':'com-table-span','width':130},
                {'name':'Team2Zh','label':'客队英文名','editor':'com-table-span','width':130},
                {'name':"MatchID",'label':'比赛','editor':'com-table-span','width':130},
            ]
        
        def get_rows(self):
            start_index = ( self.page -1 ) * self.perpage
            #for item in mydb['Event'].find(self.filter_args).sort('CreateTime',-1).skip(start_index).limit(self.perpage):
            rows =[]
            for item in mydb['Event'].find({}).skip(start_index).limit(self.perpage):
                dc ={}
                for k,v in item.items():
                    if k in ['Team1En','Team1Zh','Team2En','Team2Zh','MatchID']:
                        dc[k]=v
                rows.append(dc)
            return rows

class WebMatchForm(Fields):
    def get_heads(self):
        return [
            {'name':'Team1En','label':'英文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team1Zh','label':'主队中文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team2En','label':'客队英文名','editor':'com-field-linetext','readonly':True},
            {'name':'Team2Zh','label':'客队英文名','editor':'com-field-linetext','readonly':True},
            {'name':'MatchID','label':'比赛','editor':'com-field-linetext'},
        ]
    
    def save_form(self):
        pass

director.update({
    'web_match_data':OtherWebMatchPage.tableCls
})

page_dc.update({
    'web_match_data':OtherWebMatchPage
})