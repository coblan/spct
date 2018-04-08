from helpers.director.shortcut import ModelFields
from django.contrib.auth.models import User
from ..models import Employee,Department

class EmployeeFields(ModelFields):
    
    class Meta:
        model=Employee
        exclude=['baseinfo']
    
    # def get_row(self):
        # row = super(EmployeeFields,self).get_row()
        # if 'depart' in row.keys() and self.instance.depart:
            # row['depart_obj']={'pk':self.instance.depart.pk,'name':self.instance.depart.name}
        # return row
    
    def dict_head(self, head):
        if head['name']=='eid':
            head['readonly']=True
        return head
    
    def dict_options(self):
        users =list(User.objects.filter(employee=None))
        if self.instance.user:
            users.append(self.instance.user) 
        
        user_options=[{'value':None,'label':'---'}]
        options=[{'value':user.pk,'label':unicode(user)}for user in users]
        options=sorted(options,cmp=lambda x,y: cmp(x['label'],y['label']) )
        user_options.extend(options)
        return {
            'user':user_options,
            # 'depart':[],
        }