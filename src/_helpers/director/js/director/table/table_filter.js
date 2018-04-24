/**
 >5>front/table.rst>

 table的过滤器
 ============
 ::

 class SalaryFilter(RowFilter):
 names=['is_checked']
 range_fields=[{'name':'month','type':'month'}]
 model=SalaryRecords


 <-<
 */
import * as com_search from './filters/com_search.js'
import * as com_select from './filters/com_select.js'
import * as com_date_range from './filters/com_date_range.js'

require('./scss/table_filter.scss')

Vue.component('com-filter',{
    props:['heads','search_args'],
    template:`<div v-if='heads.length>0' class="com-filter flex flex-grow flex-ac">
                <div v-for="filter in heads" :id="'filter-'+filter.name" class="filter-item">
                    <component @submit="m_submit()" :is="filter.editor" :head="filter" :search_args='search_args' > </component>
                </div>
                <button name="go" type="button" class="btn btn-info btn-sm" @click='m_submit()' >
          <i class="fa fa-search"></i>
          </button>
        </div>
    `,
    created:function(){
        var self=this
        ex.each(self.heads,function(filter){
            if(ex.isin(filter.type,['month','date'])){
                if(!self.search['_start_'+filter.name]){
                    Vue.set(self.search,'_start_'+filter.name,'')
                }
                if(!self.search['_end_'+filter.name]){
                    Vue.set(self.search,'_end_'+filter.name,'')
                }

            }
        })
    },
    methods:{
        m_submit:function () {
            this.$emit('submit')
        },
        orderBy:function (array,key) {
            return  array.slice().sort(function (a,b) {
                if(isChinese(a[key])&&isChinese(b[key])){
                    return a[key].localeCompare(b[key],'zh')
                }else{
                    return compare(a[key],b[key])
                }
            })
        },
    }

})





var sim_filter_with_search={
    props:['filter','value'],
    data:function(){
        return{
            myvalue:this.value
        }

    },
    mounted:function(){
        var self=this
        ex.load_js("/static/lib/bootstrap-select.min.js",function(){
            $(self.$el).selectpicker()
        })
        ex.load_css("/static/lib/bootstrap-select.min.css")
    },
    watch:{
        myvalue:function(v){
            this.$emit('input',v)
        }
    },
    methods:{
        orderBy:function (array,key) {
            return  array.slice().sort(function (a,b) {
                if(isChinese(a[key])&&isChinese(b[key])){
                    return a[key].localeCompare(b[key],'zh')
                }else{
                    return compare(a[key],b[key])
                }
            })
        },
    },
    template:`<select class="selectpicker form-control"  data-live-search="true" v-model='myvalue'>
        <option :value="undefined" v-text='filter.label'></option>
        <option value="">-------</option>
        <option v-for='option in orderBy( filter.options,"label")' :value="option.value"
           :data-tokens="option.label" v-text='option.label'>
        </option>
        </select>
    `
}
Vue.component('sel-search-filter',sim_filter_with_search)

