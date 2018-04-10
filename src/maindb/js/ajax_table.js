
var ajax_table={
    props:['kw'],//['heads','row_filters','kw'],
    data:function(){
        return {
            heads:this.kw.heads,
            row_filters:this.kw.row_filters,

            row_sort:this.kw.row_sort,
            rows:[],
            row_pages:{},
            //search_tip:this.kw.search_tip,

            selected:[],
            del_info:[],

            can_add:this.kw.can_add,
            can_del:this.kw.can_del,
            can_edit:this.kw.can_edit,

            search_args: {}
        }
    },
    mixins:[mix_table_data,mix_v_table_adapter],
    //watch:{
    //    // 排序变换，获取数据
    //    'row_sort.sort_str':function(v){
    //        this.search_args._sort=v
    //        this.get_data()
    //    }
    //},
    template:`<div class="rows-block">
        <div class='flex' style="min-height: 3em;" v-if="row_filters.length > 0">
            <com-filter class="flex" :heads="row_filters" :search_args="search_args"
                        @submit="search()"></com-filter>
            <div class="flex-grow"></div>
        </div>
        <div class="box box-success">
            <div class="table-wraper">
                <v-table ref="vtable"
                         is-horizontal-resize
                         is-vertical-resize
                         :title-row-height="30"
                         :vertical-resize-offset="80"
                         :row-height="24"
                         odd-bg-color="#f0f6f8"
                         column-width-drag
                         style="width: 100%;"
                         :columns="columns"
                         :table-data="rows"
                         @sort-change="sortChange"
                         row-hover-color="#eee"
                         row-click-color="#edf7ff">
                </v-table>
            </div>
            <div style="margin-top: 10px;">
                <v-pagination @page-change="get_page($event)"
                              :total="row_pages.total"
                              size="small"
                              :page-size="row_pages.perpage"
                              @page-size-change="on_perpage_change($event)"
                              :layout="['total', 'prev', 'pager', 'next', 'sizer', 'jumper']">
                </v-pagination>
            </div>
        </div>
    </div>`,

    methods:{
        del_item:function () {
            if (this.selected.length==0){
                return
            }
            var del_obj={}
            for(var j=0;j<this.selected.length;j++){
                var pk = this.selected[j]
                for(var i=0;i<this.rows.length;i++){
                    if(this.rows[i].pk.toString()==pk){
                        if(!del_obj[this.rows[i]._class]){
                            del_obj[this.rows[i]._class]=[]
                        }
                        del_obj[this.rows[i]._class].push(pk)
                    }
                }
            }
            var out_str=''
            for(var key in del_obj){
                out_str += (key+':'+ del_obj[key].join(':')+',')
            }
            location=ex.template("{engine_url}/del_rows?rows={rows}&next={next}",{engine_url:engine_url,
                rows:encodeURI(out_str),
                next:encodeURIComponent(location.href)})
        },
        goto_page:function (page) {
            this.search_args._page=page
            this.search()
        },
        add_new:function () {
            var  url = ex.template('{engine_url}/{page}.edit/?next={next}',{
                engine_url:engine_url,
                page:page_name,
                next:encodeURIComponent(ex.appendSearch(location.pathname,search_args))
            })
            location = url
        },
    }
}

Vue.component('com_ajax_table',ajax_table)