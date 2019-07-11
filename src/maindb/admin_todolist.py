from helpers.director.shortcut import ModelTable,TablePage,ModelFields,page_dc,director,director_view,RowSort,RowFilter
from .models import TbTodolist
from helpers.director.access.permit import has_permit
from helpers.director.decorator import get_request_cache
from django.utils import timezone

class TodoList(TablePage):
    def get_label(self):
        return '待办事项'
    
    def get_template(self, prefer=None):
        return 'jb_admin/table.html'
    
    class tableCls(ModelTable):
        model = TbTodolist
        exclude =['rfid']
        pop_edit_fields=['tid']
        
        @classmethod
        def clean_search_args(cls,search_args):
            if '_sort' not in search_args:
                search_args['_sort'] = 'status'
            return search_args
        
        def inn_filter(self, query):
            cat_list = get_todolist_catlist()
            return query.filter(category__in=cat_list)
        
        def get_operation(self):
            return [
                 {'fun': 'selected_set_and_save', 
                  'editor': 'com-op-btn', 
                  'label': '已经处理', 
                  'confirm_msg': '确认修改为已经处理？',
                 'pre_set': 'rt={status:1}', 
                 'row_match': 'many_row', 
                 'after_save':'rootStore.$emit("todolist_count_updated")',
                 'visible': 'status' in self.permit.changeable_fields(),},
            ]
        
        def dict_head(self, head):
            width ={
                'title':200,
                'content':250,
            }
            if head['name'] in width:
                head['width'] = width.get(head['name'])
            return head
        
        class sort(RowSort):
            names=['status','createtime']
        
        class filters(RowFilter):
            names=['title','status']
            icontains=['title']
            range_fields=['createtime']

class TodoForm(ModelFields):
    overlap_fields=[]
    hide_fields =['operatetime','operateuser']
    class Meta:
        model = TbTodolist
        exclude =['rfid']
    
    def dict_head(self, head):
        if head['name'] =='content':
            head['editor']='com-field-blocktext'
        return head
    
    def dict_row(self, inst):
        return {
            'operatetime':inst.operatetime.strftime('%Y-%m-%d %H:%M:%S') if inst.operatetime else '',
        }

def get_todolist_catlist():
    crt_user = get_request_cache()['request'].user
    cat_list=[]
    if has_permit(crt_user,'todolist_1'):
        cat_list.append(1) 
    return cat_list

@director_view('todolist.hasnew_todolist')
def hasnew_todolist(lasttime):
    cat_list=get_todolist_catlist()
    #new_todo = TbTodolist.objects.filter(createtime__gte=lasttime,category__in=cat_list).order_by('-createtime').first()
    if TbTodolist.objects.filter(createtime__gte=lasttime,category__in=cat_list).exist():
        count = TbTodolist.objects.filter(status=0,category__in=cat_list).count()
        dc={
            'count':count,
            'hasnew':True,
            'title':'有新的待办事项,请尽快处理', #new_todo.title,
            'lasttime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'), #new_todo.createtime.strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        dc={
            'hasnew':False,
        }
    return dc

@director_view('todolist.get_counter')
def get_counter():
    cat_list=get_todolist_catlist()
    count = TbTodolist.objects.filter(status=0,category__in=cat_list).count()
    return count


director.update({
    'todolist':TodoList.tableCls,
    'todolist.edit':TodoForm
})

page_dc.update({
    'todolist':TodoList
})