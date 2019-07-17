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
        nolimit=True
        #@classmethod
        #def clean_search_args(cls,search_args):
            #if '_sort' not in search_args:
                #search_args['_sort'] = 'status'
            #return search_args
        
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
            if head['name']=='status':
                head['inn_editor'] = head['editor']
                head['editor'] = 'com-table-rich-span'
                #head['css']='''
                #td.mymiddle{text-align: center !important;}
                #.mymiddle .com-table-rich-span{border-radius:3px;font-size:80%;display:inline-block;height: 16px;padding: 0 5px;line-height: 16px}
                #.unprocessed{color:white;background-color:red;}
                #.processed{color:white;background-color:green}
                #'''
                head['cell_class']='scope.row.status==0?"warning":"success"'
                head['class']='middle-col btn-like-col'
       
            return head
        
        class sort(RowSort):
            names=['status','createtime']
            def clean_search_args(self):
                if not self.sort_str:
                    self.sort_str ='status'
        
        class filters(RowFilter):
            names=['title','status']
            icontains=['title']
            range_fields=['createtime']
            

class TodoForm(ModelFields):
    nolimit=True
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
    new_todo = TbTodolist.objects.filter(createtime__gte=lasttime,category__in=cat_list).order_by('-createtime').first()
    if new_todo:
        count = TbTodolist.objects.filter(status=0,category__in=cat_list).count()
        dc={
            'count':count,
            'hasnew':True,
            'title':new_todo.title, # '有新的待办事项,请尽快处理', #
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