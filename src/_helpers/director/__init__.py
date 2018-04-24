# -*- encoding:utf-8 -*-

"""
2.在使用views中引入装饰器
  from django.contrib.auth.decorators import login_required
  
3.在views函数上带上装饰器
@login_required
def qiangda(request):
    return render(request,'nianhui/qiang_da.html')
"""

# do not import model,because may cause "app is not load" error

#from model_admin.base import model_dc,model_page_dc
#from model_admin.render import TablePage,FormPage
#from model_admin.tabel import ModelTable
#from model_admin.fields import ModelFields