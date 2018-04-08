# encoding:utf-8
from __future__ import unicode_literals

class DelPage(object):
    template=''
    ajax_scope={}
    def __init__(self,request):
        self.request=request

    def get_template(self,prefer=None):
        if self.template:
            return self.template
        elif prefer=='f7':
            return 'f7/del_rows.html'
        else:
            return 'director/del_rows.html'

    def get_context(self):
        ctx = {}
        # pop = self.request.GET.get('_pop')
        # if not pop:
            # ctx['menu']=evalue_container(render_dc.get('menu',{}),user=self.request.user) 

        ls_str = self.request.GET.get('rows')
        rows_stream = [x for x in ls_str.split(',') if x]


        infos = {}
        rows=[]
        for row in rows_stream:
            ls = row.split(':')
            _class=ls[0]
            model = apps.get_model(_class)
            model_util= model_dc.get(model)
            fields_cls = model_util.get('fields') 
            for pk in ls[1:]:
                dc={'pk':pk,'crt_user':self.request.user}
                fields_obj= fields_cls(**dc)
                infos.update(fields_obj.get_del_info())
                rows.append(to_dict(fields_obj.instance,include=fields_obj.permit.readable_fields()))
        ctx['infos']=infos
        ctx['rows']=rows  
        # ctx['page_label']=self.get_label()
        return ctx   
    def get_label(self):
        return '数据表行删除'