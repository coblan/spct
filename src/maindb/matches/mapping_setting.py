from helpers.director.shortcut import FieldsPage,Fields,page_dc,director
from maindb.status_code import OUT_MATCH_SOURCE
from maindb.mongoInstance import mydb

class MappingSetting(FieldsPage):
    def get_label(self):
        return '跟水设置'
    
    def get_template(self, prefer=None):
        return 'jb_admin/fields.html'
    
    class fieldsCls(Fields):
        def get_heads(self):
            return [
                {'name':'EnabledSource','label':'跟水来源','editor':'com-field-select','required':True,'options':[
                    {'value':x[0],'label':x[1] } for x in OUT_MATCH_SOURCE
                ]}
            ]
        
        def dict_row(self):
            dd = mydb['Settings'].find_one()
            if dd:
                EnabledSource= dd.get('EnabledSource',2)
            else:
                EnabledSource = 2
            return {
                'EnabledSource':EnabledSource
            }
        
        def save_form(self):
            EnabledSource =  self.kw.get('EnabledSource')
            dd = mydb['Settings'].find_one()
            if dd:
                mydb['Settings'].update({'_id':dd.get('_id')},{'$set':{'EnabledSource': EnabledSource }})
            else:
                mydb['Settings'].insert({'EnabledSource': EnabledSource })
     

director.update({
    'mapping-setting':MappingSetting.fieldsCls,
})

page_dc.update({
    'mapping-setting':MappingSetting,
})