var match_logic = {
    mounted:function(){
        var self=this
        ex.assign(this.op_funs,{
            close_match:function(kws){
                if(self.selected.length!=1){
                    cfg.showMsg('请选择一条记录')
                    return
                }
                var crt_row = self.selected[0]
                if(crt_row.statuscode==100){
                    cfg.showMsg('比赛状态已经为结束，不需要手动结束！')
                    return
                }

                var index = layer.confirm('结束比赛?',function(index){

                    crt_row.statuscode=100
                    var post_data=[{fun:'save_row',row:crt_row}]
                    cfg.show_load()
                    ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                        layer.close(index);
                        if(resp.save_row.errors){
                            cfg.warning(JSON.stringify( resp.save_row.errors))
                        }else{
                            cfg.hide_load(2000)

                        }

                    })
                })
            },
            manual_end_money:function(kws){
                if(self.selected.length!=1){
                    cfg.showMsg('请选择一条记录')
                    return
                }

                var crt_row = self.selected[0]
                var row={
                    matchid:'123',
                    home_score:'123',
                    away_score:'213',
                    statuscode:crt_row.statuscode
                }
                pop_fields_layer(row,kws.heads,kws.ops,function(kws){
                    alert(kws.new_row)
                })
            },
            jie_suan_pai_cai:function(kws){
                if(self.selected.length!=1){
                    cfg.showMsg('请选择一条记录')
                    return
                }
            },
            recommendate:function(kws){
                if(self.selected.length==0){
                    cfg.showMsg('请选择一些记录')
                    return
                }
                ex.each(self.selected,function(row){
                    row.isrecommend=true
                })
                var post_data=[{fun:'save_rows',rows:self.selected}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    cfg.hide_load(2000)
                })
            },
            livebet:function(kws){
                if(self.selected.length==0){
                    cfg.showMsg('请选择一些记录')
                    return
                }
                ex.each(self.selected,function(row){
                    row.livebet=true
                })
                var post_data=[{fun:'save_rows',rows:self.selected}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    cfg.hide_load(2000)
                })
            }
        })
    },
    computed:{
        only_one_selected:function(){
            return this.selected.length ==1
        },
        status_is_not_100:function(){
            if(this.selected.length ==1){
                var row = this.selected[0]
                if(row.statuscode !=100){
                    return true
                }
            }
            return false
        }
    }
}

window.match_logic = match_logic