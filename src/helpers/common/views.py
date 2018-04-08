from django.shortcuts import render

# Create your views here.
def donwload_views(request,app):
    conf= apps.get_app_config(app)
    app_dot_path=conf.module.__name__
    ajax_module=locate('%(app)s.ajax'%{'app':app_dot_path})
    
    try:
        # 返回 未经过任何修改的 response对象
        return naked_router(request, ajax_module.get_global())
    except KeyError as e:
        rt={'status':'error','msg':'key error '+str(e) +' \n may function name error'}
        return HttpResponse(json.dumps(rt),content_type="application/json")  