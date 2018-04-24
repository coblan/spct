

class LogPage(object):
    template='director/model_log.html'
    def __init__(self, request):
        """
        ?rows=pkg.model:1:2,pkg.model2:1:2,
        
        """
        self.request=request
       
    
    def get_context(self):
        ls_str = self.request.GET.get('rows')
        rows_stream = [x for x in ls_str.split(',') if x]
        rows =[]
        for row in rows_stream:
            ls   = row.split(':')
            _class=ls[0]
            model = apps.get_model(_class)
            model_util= model_dc.get(model)            
            fields_cls = model_util.get('fields') 
            perm = ModelPermit(model, self.request.user)
            if perm.can_log(): 
                for pk in ls[1:]:
                    querys =LogModel.objects.filter(key='%s.%s'%(_class,pk)).order_by('-id')
                    rows.extend(list(querys))
        ctx = {'rows':[sim_dict(x,filt_attr=lambda y:{'user':unicode(y.user)}) for x in rows],
               'heads':model_to_head(LogModel)}

        ctx['can_add']=False
        ctx['can_del']=False
        return ctx         