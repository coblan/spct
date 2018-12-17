from django.contrib.auth.models import User

#def user_label(pk): 
    #try:
        #user = User.objects.get(pk = pk)
        #return str(user)
    #except User.DoesNotExist:
        #return pk


from django.db.models import IntegerField
from helpers.director.model_func.field_proc  import BaseFieldProc
from helpers.director.base_data import field_map
from helpers.director.middleware.request_cache import get_request_cache

class CreateUserField(IntegerField):
    pass

class UpdateUserField(IntegerField):
    pass

class CreateUserProc(BaseFieldProc):
    
    def to_dict(self,inst,name):
        pk = getattr(inst,name)
        try:
            user = User.objects.get(pk = pk)
            return {
                name: pk, 
                '_%s_label' % name: str(user),
            }
        
        except User.DoesNotExist:
            return {
                name: pk, 
                '_%s_label' % name: pk,
                    }
    def dict_table_head(self,head):
        """
        """
        head['editor'] = 'com-table-label-shower'
        return head 
    
    def clean_field(self,dc,name):
        """ 
        fields类里，从前端穿过来的row dict数据进行清洗， dc里面有的 字段，才会被调用
        """
        if not dc.get(name):
            catch =  get_request_cache()
            request = catch['request']
            dc[name] = request.user.pk
        return dc.get(name)

class UpdateUserPorc(CreateUserProc):
    def clean_field(self,dc,name):
        """ 
        fields类里，从前端穿过来的row dict数据进行清洗， dc里面有的 字段，才会被调用
        """
        catch =  get_request_cache()
        request = catch['request']
        dc[name] = request.user.pk
        return dc.get(name)    

field_map.update({
    CreateUserField:CreateUserProc,
    UpdateUserField:UpdateUserPorc,
})
