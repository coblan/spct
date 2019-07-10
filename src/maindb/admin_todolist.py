from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director,director_view
from .models import TbTodolist

class TodoList(TablePage):
    def get_label(self):
        return '待办事项'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbTodolist
        exclude =['rfid']
        pop_edit_fields=['tid']

class TodoForm(ModelFields):
    hide_fields =['operatetime','operateuser']
    class Meta:
        model = TbTodolist
        exclude =['rfid']
    
    def dict_row(self, inst):
        return {
            'operatetime':inst.operatetime.strftime('%Y-%m-%d %H:%M:%S') if inst.operatetime else '',
        }

@director_view('todolist.hasnew_todolist')
def hasnew_todolist(lasttime):
    count = TbTodolist.objects.count()
    new_todo = TbTodolist.objects.filter(createtime__gte=lasttime).order_by('-createtime').first()
    if new_todo:
        dc={
            'count':count,
            'hasnew':True,
            'title':new_todo.title,
            'lasttime':new_todo.createtime.strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        dc={
            'count':count,
            'hasnew':False,
        }
    return dc


director.update({
    'todolist':TodoList.tableCls,
    'todolist.edit':TodoForm
})

page_dc.update({
    'todolist':TodoList
})