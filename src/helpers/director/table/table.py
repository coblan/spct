# encoding:utf-8

from __future__ import unicode_literals
from django.utils.translation import ugettext as _
#from core.db_tools import to_dict,model_to_head,model_stringfy
import json
from django.db.models import Q,fields
from django.core.exceptions import PermissionDenied
from ..access.permit import ModelPermit
from ..model_func.dictfy import model_to_name,to_dict,model_to_head,model_to_name
from django.db import models
import math
import time
#import pinyin
#from forms import MobilePageForm


from django.core.paginator import Paginator


class PageNum(object):
    perPage=20
    def __init__(self,pageNumber=1,perpage=None,kw={}):
        self.pageNumber = int(pageNumber)
        if perpage:
            self.perPage= int(perpage)
        
    
    def get_query(self,query):
        #count = query.count()
        #totalpage = int( math.ceil( float( count )/self.perPage) )
        #self.totalpage = max(totalpage,1)
        
        #self.query = query  
        #crt_page=min(self.totalpage,abs(int( self.pageNumber)))
        #start = (crt_page -1)*self.perPage
        #end = min(crt_page*self.perPage,count)
        #return query[start:end]
        self.pagenator = Paginator(query,self.perPage)
        self.pageNumber = min(self.pagenator.num_pages,abs(int( self.pageNumber)))
        return self.pagenator.page(self.pageNumber)
        #return self.pagenator.page(self.pageNumber)
        
        
    
    def get_context(self):
        """
        rt: {'options':[1,2,3,4,...,100],
             'crt_page':2
            }
        """
        #choice_len = len(self.pagenator.page_range)
        #k=3
        #a=-1
        #while a < 1:
            #a=self.pageNumber-k
            #k-=1
        #page_nums = range(a,min(choice_len,self.pageNumber+(5-k))+1)
        #if page_nums[0] != 1:
            #page_nums=[1,'...']+ page_nums
        #if page_nums[-1] != choice_len:
            #page_nums = page_nums +['...',choice_len]
        #for i in range(len(page_nums)):
            #num = page_nums[i]
        #page_nums=[str(x) for x in page_nums]

        #return {'options':page_nums,'crt_page':self.pageNumber}    
        return {'crt_page':self.pageNumber,
                'total':self.pagenator.count,
                'perpage':self.perPage}

class TrivalPageNum(object):
    def __init__(self,pageNumber=1,kw={}):
        pass    
    def get_query(self,query):
        return query
    def get_context(self):
        return {}
    

class RowSearch(object):
    names=[]
    model=''
    def __init__(self,q,user,allowed_names,kw={}):
        self.valid_name=[x for x in self.names if x in allowed_names]
        self.crt_user=user
        self._names=[x for x in self.names if x in allowed_names]        
        self.q=q
        #for k in self.names:
            #v = dc.pop(k,None)
            #if v:
                #self.search_args[k]=v
         
    def get_context(self):
        """
        """
        if self.valid_name:
            ls=[]
            for name in self.valid_name:
                ls.append(_(self.model._meta.get_field(name).verbose_name) )
            dc = {
                'search_tip':','.join(ls),
                'editor':'com-search-filter',
                'name':'_q'
            }
            return dc
    
    def get_query(self,query):
        if self.q:
            exp=None
            for name in self.valid_name:
                kw ={}
                kw['%s__icontains'%name] =self.q    
                if exp is None:
                    exp = Q(**kw)
                else:
                    exp = exp | Q(**kw) 
            return query.filter(exp)
        else:
            return query

class RowFilter(object):
    """
    @names : 普通字段，用于过滤用.
    @range_fields: span字段，例如时间段
    
     range_fields=[{'name':'create_time','type':'date'}]
    """
    names=[]
    range_fields=[]
    model=''
    def __init__(self,dc,user,allowed_names,kw={}):
        self.names = self.names + self.range_fields #+ [x.get('name') for x in self.range_fields]
        self.valid_name=[x for x in self.names if x in allowed_names]
        self.crt_user=user
        #self._names=[x for x in self.names if x in allowed_names]        
        self.filter_args={}
        for k in self.names:
            v = dc.pop(k,None)
            if v != None:
                self.filter_args[k]=v   
            if v=='0':
                self.filter_args[k]=False
            elif v=='1':
                self.filter_args[k]=True
        for k in self.range_fields: #[x.get('name') for x in self.range_fields]:
            if kw.get('_start_%s'%k):
                start=kw.get('_start_%s'%k)
                self.filter_args['%s__gte'%k]=start
            if kw.get('_end_%s'%k):
                end=kw.get('_end_%s'%k)
                self.filter_args['%s__lte'%k]=end            
    
    def get_context(self):
        ls=[]
        for name in self.valid_name:
            f = self.model._meta.get_field(name)
            #mt = [x for x in self.range_fields if x.get('name')==name]
            #if mt:
            if name in self.range_fields:
                if isinstance(f,fields.DateField):
                    ls.append({'name':name,
                               'label':_(f.verbose_name),
                               'editor':'com-date-range-filter'
                               })
            elif isinstance(f,fields.BooleanField):
                ls.append({'name':name,
                           'label':_(f.verbose_name),
                           'editor':'com-select-filter',
                           'options':[
                               {'value':'1','label':'Yes'},
                               {'value':"0",'label':'No'}]})
            else:
                ls.append({'name':name,
                           'editor':'com-select-filter',
                           'label':_(f.verbose_name),
                           'options':self.get_options(name)})
        return ls
      
    def get_query(self,query):
        self.query=query
        query=query.filter(**self.filter_args)
        return query    
    
    def get_options(self,name):
        this_field= self.model._meta.get_field(name)
        if this_field.choices:
            return [{'value':x[0],'label':x[1]} for x in this_field.choices]
        elif isinstance(this_field,models.ForeignKey):
            ls=this_field.get_choices()
            ls=ls[1:]
            out= [{'value':x[0],'label':x[1]} for x in ls]
            #out= self.sort_option(out) # 用pinyin排序 sorted(out,key=lambda x:x['label'].encode('gbk'))  # 尼玛，用GBK才能对常用的中国字进行拼音排序
                                                                   # 不常用的字，以及unicode都是按照笔画排序的
            return out
        # 这里需要考虑下，过滤的选项是来自于model的所有记录，还是来自于table过滤后的query
        # 这里暂时是使用model的所有记录
        elif not hasattr(self,'query'):
            self.query = self.model.objects.all()
    
        ls = list(set(self.query.values_list(name,flat=True)))
        #ls.sort()
        out=[{'value':x,'label':unicode(x)} for x in ls]
        #out= self.sort_option(out) # 用pinyin排序 sorted(out,key=lambda x:x['label'].encode('gbk'))  
        return out   
    
    # def sort_option(self,option):
        # index=0
        # for opt in option:
            # if opt['value']:
                # break
            # else:
                # index+=1
        # option[index:]=sorted(option[index:],key=lambda x:pinyin.get_initial(x['label']))
        # return option
    
    
class RowSort(object):
    """
    row_sort: 'name1,-name2'
    """
    names=[]
    chinese_words=[]
    def __init__(self,row_sort=[],user=None,allowed_names=[],kw={}):
        self.valid_name=[x for x in self.names if x in allowed_names]
        ls=[]
        for x in row_sort:
            if x.lstrip('-') in self.valid_name:
                ls.append(x)
        self.sort_str=','.join(ls)
        
    def get_context(self):
        return {'sortable':self.valid_name,'sort_str':self.sort_str}
    
  
    
    def get_query(self,query):
        if self.sort_str:
            ls=self.sort_str.split(',')
            for name in ls:
                if name.startswith('-'):
                    norm_name=name.lstrip('-')
                    direction='-'
                else:
                    norm_name=name
                    direction=''                    
                if norm_name in self.chinese_words:
                    query= query.extra(select={'converted_%s'%norm_name: 'CONVERT(%s USING gbk)'%norm_name},order_by=['%sconverted_%s'%(direction,norm_name)])
                else:
                    query= query.order_by(name)

        return query

  
class ModelTable(object):
    """
    
    Getter Method:
    ===============
    get_heads(self):
        return [{name:'xxx',label:'xxx',sortable:true}]
        
    get_rows(self):
        return [{}]
    

    over-load Method:
    =================
    inn_filter(self,query):
        process inn filter logic . Get gid of ,Ex: user-ware ,group-ware data.
        these data will be used for sort and filter in front-end
        
    """
    model=''
    sort=RowSort
    search=RowSearch
    filters=RowFilter
    include=None
    exclude=[]
    pagenator=PageNum
    fields_sort=[]
    def __init__(self,_page=1,row_sort=[],row_filter={},row_search={},crt_user=None,perpage=None,**kw):
        self.kw=kw
        self.crt_user=crt_user 
        self.page=_page
        
        self.custom_permit()
        allowed_names=self.permited_fields()
        
        self.row_sort=self.sort(row_sort,crt_user,allowed_names,kw)
        self.row_filter=self.filters(row_filter, crt_user, allowed_names,kw) 
        self.row_search = self.search( row_search,crt_user,allowed_names,kw)
        if not self.row_filter.model:
            self.row_filter.model=self.model
        if not self.row_search.model:
            self.row_search.model=self.model
        self.pagenum = self.pagenator(pageNumber=self.page,perpage=perpage)
        
        
        
    
    def custom_permit(self):
        self.permit=ModelPermit(model=self.model, user=self.crt_user)

    @classmethod
    def parse_request(cls,request):
        """
        传入参数的形式：
        row_search: key=value&..
        row_sort: _sort=key1,-key2
        page: _page=1
        row_filter:key=value&..
        """
        kw = request.GET.dict()
        return cls.gen_from_search_args(kw,request.user)
        #page = kw.pop('_page','1')
        #perpage = kw.pop('_perpage')
        #row_sort = kw.pop('_sort','').split(',')
        #row_sort=filter(lambda x: x!='',row_sort)
        #q=kw.pop('_q',None)
        #row_filter={}
        #for k in cls.filters.names:
            #arg = kw.pop(k,None)
            #if arg:
                #row_filter[k]=arg
        #return cls(page,row_sort,row_filter,q,request.user,**kw)
    
    @classmethod
    def gen_from_search_args(cls,search_args,user):
        kw = search_args
        page = kw.pop('_page','1')
        perpage = kw.pop('_perpage',None)
        row_sort = kw.pop('_sort','').split(',')
        row_sort=filter(lambda x: x!='',row_sort)
        q=kw.pop('_q',None)
        row_filter={}
        for k in cls.filters.names:
            arg = kw.pop(k,None)
            if arg:
                row_filter[k]=arg
        return cls(page,row_sort,row_filter,q,user,perpage=perpage,**kw)
        
    def get_context(self):
        ls=[]
        search_head = self.row_search.get_context()
        row_filters = self.row_filter.get_context()
        # 合并search和rowfilter 为rowfilter
        if search_head:
            ls.append( search_head)
        if row_filters:
            ls.extend(row_filters)
        return {
            'heads':self.get_heads(),
            'rows': self.get_rows(),
            'row_pages' : self.pagenum.get_context(),
            'row_sort':self.row_sort.get_context(),
            'row_filters':ls,
            #'search_tip':self.row_search.get_context(),
            'model':model_to_name(self.model),
            'ops' : self.get_operation()
        }
    
    def get_head_context(self):
        """
        有些时候，最先不需要返回rows，而只返回filters，head等，等待用户选择后，才返回rows
        """
        return {
            'heads':self.get_heads(),
            'rows': [], #self.get_rows(),
            'row_pages':{}, # self.pagenum.get_context(),
            'row_sort':self.row_sort.get_context(),
            'row_filters':self.row_filter.get_context(),
            'search_tip':self.row_search.get_context(),
            'model':model_to_name(self.model),
            'ops' : self.get_operation()
        }        
    
    def get_data_context(self):
        return {
            'rows': self.get_rows(),
            'row_pages' : self.pagenum.get_context(),            
        }
    
    def permited_fields(self):
        ls = self.permit.readable_fields()
        
        if 'id' not in self.exclude and 'id' not in ls:
            ls.insert(0,'id')
        elif 'id' in self.exclude and 'id' in ls:
            ls.remove('id')
            
        if self.include:
            return [x for x in self.include if x in ls]
        if self.exclude:
            return [x for x in ls if x not in self.exclude]
        return ls
    
    def get_heads(self):
        """
        return:[{"name": "name", "label": "\u59d3\u540d"}, {"sortable": true, "name": "age", "label": "\u5e74\u9f84"}]
        """
        ls = self.permited_fields()   
        heads = model_to_head(self.model,include=ls)
        heads = self.fields_sort_heads(heads)
        heads=[self.fields_map_head(head) for head in heads]
        heads = [self.dict_head(head) for head in heads]
        
        return heads
    
    def dict_head(self,head):
        return head
    
    def fields_map_head(self,head):
        field = self.model._meta.get_field(head['name'])
        if field.choices:
            head['options']=dict(field.choices)
            head['editor']='com-table-mapper'
        return head

    def fields_sort_heads(self,heads):
        if not self.fields_sort:
            return heads
        
        tmp_heads = []
        for k in self.fields_sort:
            for head in heads:
                if head['name'] == k:
                    tmp_heads.append(head)
                    #heads.remove(head)
                    break
        #tmp_heads.extend(heads)
        return tmp_heads
            
    def get_rows(self):
        """
        return: [{"name": "heyul0", "age": "32", "user": null, "pk": 1, "_class": "user_admin.BasicInfo", "id": 1}]
        """
        query=self.get_query()
        out=[]
        for inst in query:

            dc= to_dict(inst, include=self.permited_fields(),filt_attr=self.dict_row( inst))
            out.append(dc)
        return out
    

    
    def dict_row(self,inst):
        """
        重写该函数，定制row输出字典
        """
        return {}
    
    def get_query(self):
        if not self.crt_user.is_superuser and not self.permit.readable_fields():
            raise PermissionDenied,'no permission to browse %s'%self.model._meta.model_name
        
        query = self.inn_filter(self.model.objects.all())
        query=self.row_filter.get_query(query)
    
        query=self.row_search.get_query(query)
        query = self.row_sort.get_query(query)
        query = self.pagenum.get_query(query)  
        return query
 
    def inn_filter(self,query):
        return query.order_by('-pk')
    
    def get_operation(self):
        return [{'name':'add_new','editor':'com-op-a','label':'创建'},
                {'name':'save_changed_rows','editor':'com-op-a','label':'保存','hide':'!changed'},
                {'name':'delete','editor':'com-op-a','label':'删除','disabled':'!has_select'},
                ]      
    
    #def search_filter(self,query):
        #return self.row_search.get_query(query)
        #for field in self.search_fields:
            #kw ={}
            #kw['%s__icontains'%field] =self.row_search            
        #return query
    
    #def sort_filter(self,query):
        
        #return query
    
    #def out_filter(self,query):
        #if self.search_fields and self.row_search:
            #exp = None
            #for field in self.search_fields:
                #if isinstance(field,SearchQuery):
                    #query=field.get_query(query,self.row_search,self.crt_user)
                #else:
                    #kw ={}
                    #kw['%s__icontains'%field] =self.row_search
                    #if exp is None:
                        #exp = Q(**kw)
                    #else:
                        #exp = exp | Q(**kw)
            #if exp:
                #query= query.filter(exp)
        #if self.row_sort:
            #return query.filter(**self.row_filter).order_by(*self.row_sort)
        #else:
            #return query.filter(**self.row_filter)
    
    #def get_options(self):
        #query = self.inn_filter(self.model.objects.all())
        #options=[]
        #for name in self.filters:
            #tmp = []
            #option =[]
            #field = self.model._meta.get_field(name)
            #label = field._verbose_name
            #value = self.row_filter.get(name,'')
            #for x in query: # get rid of duplicated row
                #if getattr(x,name) not in tmp:
                    #tmp.append(getattr(x,name))
                    #if value == getattr(x,name):
                        #option.append({'label': '%s:%s'%(name,getattr(x,name)),'name':getattr(x,name)})
                    #else:
                        #option.append({'label': getattr(x,name),'name':getattr(x,name)})
            #options.append({
                #'name':name,
                #'label':label,
                #'value': value,
                #'options':option,
            #})
        #return options    
    
    #def get_placeholder(self):
        #ls=[]
        #for field in self.search_fields:
            #if isinstance(field,SearchQuery):
                #ls.append(field.get_placeholder())
            #else:
                #ls.append(self.model._meta.get_field(field).verbose_name)
        #return ','.join(ls)
        # return ','.join([self.model._meta.get_field(name).verbose_name for name in self.search_fields])



# from models import MobilePage
# class PageTable(ModelTable):
    # model = MobilePage
    # sortable=['name','label']
    # filters = ['name','label']
    # include= ['name','label']
    # search_fields=['name']
    # per_page=2
  