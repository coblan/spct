# encoding:utf-8
from __future__ import unicode_literals
from helpers.director.shortcut import ModelTable,TablePage,page_dc,ModelFields,model_dc
from ..models import TbMatches
from helpers.maintenance.update_static_timestamp import js_stamp_dc

class MatchsPage(TablePage):
    template='jb_admin/table.html'
    extra_js=['/static/js/maindb.pack.js?t=%s'%js_stamp_dc.get('maindb_pack_js','')]
    def get_label(self, prefer=None):
        return '比赛信息'
    
    class tableCls(ModelTable):
        model = TbMatches
        exclude=[]
        def get_context(self):
            ctx = ModelTable.get_context(self)
            ctx['extra_table_logic'] = 'match_logic'
            return ctx
        
        def get_operation(self):
            ops =[
                #{'name':'save_changed_rows','editor':'com-op-a','label':'保存','hide':'!changed'},
                
                {'fun':'close_match','editor':'com-op-a','label':'结束比赛'},
                {'fun':'manual_end_money',
                 'editor':'com-op-a',
                 'label':'产生赛果',
                 #'disabled':'!only_one_selected',
                 'heads':[{'name':'matchid','label':'赛事ID','editor':'linetext'},
                          {'name':'home_score','label':'主队分数','editor':'linetext'},
                          {'name':'home_corner','label':'主队角球','editor':'linetext'},
                          {'name':'away_score','label':'客队分数','editor':'linetext'},
                          {'name':'away_corner','label':'客队角球','editor':'linetext'},
                          {'name':'statuscode','label':'赛事状态','editor':'linetext'},
                          {'name':'close_time','label':'结束时间','editor':'com-field-datetime'}],
                 'ops':[{"fun":'xxx','label':'保存','editor':'com-field-op-btn'}]},
                {'fun':'jie_suan_pai_cai','editor':'com-op-a','label':'结算派彩'},
                {'fun':'recommendate','editor':'com-op-a','label':'推介'},
                {'fun':'livebet','editor':'com-op-a','label':'滚球'},
                
            ]
            return ops
        
        
        #def get_heads(self):
            #heads = [{'name':'operations',
                    #'label':'操作',
                    #'editor':'com-table-operations',
                    #'operations':[
                        #{'name':'manul_end','label':'手动结算'},
                        #{'name':'has_end_match','label':'已结束'} #100
                    #],
                    #'width':130,
                          #}]
            #org_heads = ModelTable.get_heads(self)
            #heads.extend(org_heads)
            #return heads
        
        #def dict_row(self, inst):
            #dc={}
            #if inst.statuscode != 100:
                #dc['_op_has_end_match_hide']=True
            #if inst.statuscode == 100:
                #dc['_op_manul_end_hide']=True
                
            #return dc

class MatchForm(ModelFields):
    class Meta:
        model=TbMatches
        exclude=[]

model_dc[TbMatches]={'fields':MatchForm}

page_dc.update({
    'maindb.Matches':MatchsPage
})