var com_vue_table={
    props: {
        has_check: {},
        heads: {},
        rows: {
            default: function () {
                return []
            }
        },
        map: {},
        row_sort: {
            default: function () {
                return {sort_str: '', sortable: []}
            }
        },
        value: {},
        height:{},
    } ,
    data:function(){
        return {
        }


    },
    computed:{
        tableData:function(){
            return this.rows
        } ,
        selected:{
            get:function(){
                return this.value
            },
            set:function(v){
                this.$emit('input',v)
            }
        },
        columns:function(){
            var cols =ex.map(heads,function(head){
                    var col =ex.copy(head)
                    var dc = {
                        field:head.name,
                        title:head.label,
                        isResize:true,
                        width:200,
                    }
                    if (head.type){
                        dc.componentName=head.type
                    }
                    ex.assign(col,dc)
                    return col
                })
            return cols
        }
    },
    methods:{
        m_map:function(name,row){
            if(this.map){
                return this.map(name,row)
            }else{
                return row[name]
            }
        },
        is_sorted:function (sort_str,name) {
            var ls=sort_str.split(',')
            var norm_ls=this.filter_minus(ls)
            return ex.isin(name,norm_ls)
        },
        filter_minus:function (array) {
            return ex.map(array,function (v) {
                if(v.startsWith('-')){
                    return v.slice(1)
                }else{
                    return v
                }
            })
        },
        is_sortable:function(name){
            return ex.isin(name,this.row_sort.sortable)
        },
        toggle:function (sort_str,name) {
            if(sort_str == name){
                return '-'+name
            }else {
                return name
            }
            //var ls=ex.split(sort_str,',')
            //var norm_ls=this.filter_minus(ls)
            //var idx = norm_ls.indexOf(name)
            //if(idx!=-1){
            //    ls[idx]=ls[idx].startsWith('-')?name:'-'+name
            //}else{
            //    ls.push(name)
            //}
            //return ls.join(',')
        },
        toggle_all:function(e){
            var checked = e.currentTarget.checked
            if(checked){
                this.selected=ex.map(this.rows,function(row){return row.pk})
            }else{
                this.selected=[]
            }
        }


    },
    //is-horizontal-resize
    //column-width-drag
    template:`<v-table is-horizontal-resize
            column-width-drag
            :height="height"
             style="width: 100%"
            :columns="columns"
            :table-data="tableData"
            row-hover-color="#eee"
            row-click-color="#edf7ff">
    </v-table>`,
    beforeMount:function(){


        //ex.load_css("https://cdn.bootcss.com/bootstrap-table/1.12.1/bootstrap-table.min.css")
        //ex.load_js("https://cdn.bootcss.com/bootstrap-table/1.12.1/bootstrap-table.min.js",function(){
        //
        //})
    },
    mounted:function(){
        //ex.load_js('https://unpkg.com/vue-easytable/umd/js/index.js',function(){
        //
        //})

    }
}
Vue.component('com-vue-table',com_vue_table)