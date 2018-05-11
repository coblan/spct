var activity_logic={
    mounted:function(){
        var self=this
        ex.assign(this.op_funs,{
            update_activity_file:function(){
                cfg.show_load()
                var post_data=[{fun:'update_activity_file'}]
                ex.post('/d/ajax/maindb',JSON.stringify(post_data),function(resp){
                    if(resp.update_activity_file.status=='success'){
                        cfg.hide_load(500)
                    }else{
                        cfg.warning(resp)
                        cfg.hide_load()
                    }

                })
            }
        })

    }
}

window.activity_logic = activity_logic