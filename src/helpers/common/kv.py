from .models import KVModel

def get_value(key,default=None):
    try:
        inst=KVModel.objects.get(key=key)
        return inst.value
    except KVModel.DoesNotExist:
        return default

def set_value(key,value):
    KVModel.objects.update_or_create(key=key,defaults={'value':value})