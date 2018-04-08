from .base import model_dc

def form_dict(inst,user):
    formcls=model_dc[inst.__class__]['fields']
    form_obj=formcls(instance=inst,crt_user=user)
    return form_obj.get_row()