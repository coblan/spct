var notice_logic={

    mounted:function(){

        var self=this
        ex.assign(this.op_funs,{
            update_notice_file:function(){
                cfg.show_load()
                var post_data=[{fun:'update_notice_file'}]
                ex.post('/d/ajax/maindb',JSON.stringify(post_data),function(resp){
                    if(resp.update_notice_file.status=='success'){
                        cfg.hide_load(500)
                    }else{
                        cfg.warning(resp)
                        cfg.hide_load()
                    }

                })
            }
        })


    },

    //computed:{
    //    row_count:function(){
    //        return this.rows.length
    //    }
    //},
    //watch:{
    //    row_count:function(v){
    //        var post_data=[{fun:'get_help_options'}]
    //        ex.post('/d/ajax/maindb',JSON.stringify(post_data),function(resp){
    //            var mtype_filter = ex.findone(row_filters,{name:'mtype'})
    //            mtype_filter.options = resp.get_help_options
    //        })
    //    }
    //},
}
window.notice_logic=notice_logic