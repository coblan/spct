export var table_time_group={
    data:{
        grouped_rows:[],
    },
    mounted:function(){
        this.grouped_rows=  ex.group_add([],this.rows,this.get_group_key)
    },
    computed:{
//            grouped_rows:function(){
//                var new_rows = ex.group_add([],this.rows,function(row){return row.create_time.slice(0,10)})
//                return new_rows
//            },

    },
    methods:{
        append_rows:function(new_rows){
            this.rows = this.rows.concat(new_rows);
            this.grouped_rows = ex.group_add(this.grouped_rows,new_rows,this.get_group_key)
        },
        get_group_key:function(row){
            alert('must custom get_group_key callback')
        },
        norm_date:function(date){
            var span= moment()-moment(date)
            var span_days= moment.duration(span).days()
            if(span_days<1){
                return '今天'
            }else if(span_days<2){
                return '昨天'
            }else{
                return date
            }
        },
        norm_time:function(date_time){
            return date_time.slice(11,19)
        },
        load_next_page: function () {
            var self = this;
            ex.get(ex.appendSearch({ _page: row_pages.crt_page + 1 }), function (resp) {
                ex.assign(row_pages, resp.row_pages);
                self.append_rows(resp.rows);
            });
        },
    }
}