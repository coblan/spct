var oddstypegroup_logic={
    mounted:function() {
        var self = this
        ex.assign(this.op_funs, {
            set_enable: function () {
                if (self.selected.length == 0) {
                    cfg.showMsg('请选择【一些】记录')
                    return
                }
                ex.each(self.selected,function(row){
                    row.enabled=1
                })
                var post_data=[{fun:'save_rows',rows:self.selected}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    cfg.hide_load(2000)
                })
            },
            set_disable: function () {
                if (self.selected.length == 0) {
                    cfg.showMsg('请选择【一些】记录')
                    return
                }
                ex.each(self.selected,function(row){
                    row.enabled=0
                })
                var post_data=[{fun:'save_rows',rows:self.selected}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    cfg.hide_load(2000)
                })
            }
        })
    }

}

window.oddstypegroup_logic=oddstypegroup_logic