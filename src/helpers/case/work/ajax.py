from helpers.director.db_tools import from_dict
from .admin import WRselfForm

def get_global():
    return globals()

def save_workself(row,user,request):
    #instance=from_dict(row)
    fm = WRselfForm(row,crt_user=user,_depart=request.GET.get('_depart'))
    if fm.is_valid():
        fm.save_form()
        dc = fm.get_row()
        return {'status':'success','row':dc}
    else:
        return {'errors':dict(fm.errors)}

