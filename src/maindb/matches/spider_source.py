from helpers.director.shortcut import TablePage,PlainTable,Fields,page_dc,director
from maindb.mongoInstance import mydb
from maindb.status_code import MATCH_SOURCE
from bson.objectid import ObjectId
from maindb.rabbitmq_instance import notifyMapingSetting
import json

class SpiderSourcePage(TablePage):
    def get_label(self):
        return '跟水设置'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(PlainTable):
        selectable=False
        def get_heads(self):
            return [
                {'name':'Source','label':'源','editor':'com-table-mapper','options':[
                    {'value':x[0],'label':x[1]} for x in MATCH_SOURCE
                    ],'width':100},
                {'name':'Enabled','label':'启用','editor':'com-table-input-bool','width':80},
                {'name':'Index','label':'优先级','editor':'com-table-input-int','width':100,'required':True},
            ]
        
        def get_rows(self):
            rows = []
            for inst in mydb["SpiderSource"].find({}):
                inst['pk'] = str( inst.pop('_id'))
                inst['_director_name'] = self.get_edit_director_name()
                rows.append(inst)
            rows.sort(key=lambda x:x.get('Index'))
            return rows
        

class SpiderSourceForm(Fields):
    def save_form(self):
        dc = {}
        for k in self.kw:
            if k in ['Source','Enabled','Index']:
                dc[k] = self.kw[k]
        rt =mydb["SpiderSource"].update({'_id':ObjectId(self.kw.get('pk') )},{'$set':dc})
        notifyMapingSetting(json.dumps({}))
        out_dc ={'pk':self.kw.get('pk'),'model':'mongo/SpiderSource' ,**dc}
        self.save_log(out_dc)
    
    

director.update({
    'spidersource':SpiderSourcePage.tableCls,
    'spidersource.edit':SpiderSourceForm
})

page_dc.update({
    'spidersource':SpiderSourcePage
})
        