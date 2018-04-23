
var ajax_table={
    props:['tab_head','par_row'],//['heads','row_filters','kw'],
    data:function(){
        var heads_ctx = this.tab_head.heads_ctx
        return {
            heads:heads_ctx.heads,
            row_filters:heads_ctx.row_filters,
            row_sort:heads_ctx.row_sort,

            rows:[],
            row_pages:{},
            //search_tip:this.kw.search_tip,

            selected:[],
            del_info:[],

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
        on_show:function(){
            if(! this.fetched){
                this.get_data()
                this.fetched = true
            }
        },
        data_getter:function(){
        // 这里clear，数据被清空，造成table的pagenator上下抖动
//                       com.clear()

//                        var getter_name = 'get_'+tab.name
            var self=this
            var fun = get_data[this.tab_head.get_data.fun ]
            fun(function(rows,row_pages){
                self.rows = rows
                self.row_pages =row_pages
            },this.par_row,this.tab_head.get_data.kws,this.search_args)

//            var self=this
//            var relat_pk = this.par_row[this.relat_field]
//        var relat_field = this.relat_field
//        this.search_args[relat_field] = relat_pk
//        var post_data=[{fun:'get_rows',search_args:this.search_args,model_name:this.model_name}]
//            cfg.show_load()
//        $.post('/d/ajax',JSON.stringify(post_data),function(resp){
//            cfg.hide_load()
//            self.rows = resp.get_rows.rows
//            self.row_pages =resp.get_rows.row_pages
//        })
    },
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

Vue.component('com_tab_table',ajax_table)

var get_data={
    get_rows:function(callback,row,kws,search_args){
        var relat_field = kws.relat_field
        var model_name = kws.model_name

        var self=this
        var relat_pk = row[kws.relat_field]
        var relat_field = kws.relat_field
        search_args[relat_field] = relat_pk
        var post_data=[{fun:'get_rows',search_args:search_args,model_name:model_name}]
        cfg.show_load()
        $.post('/d/ajax',JSON.stringify(post_data),function(resp){
            cfg.hide_load()
            callback(resp.get_rows.rows,resp.get_rows.row_pages)
            //self.rows = resp.get_rows.rows
            //self.row_pages =resp.get_rows.row_pages
        })
    }
}