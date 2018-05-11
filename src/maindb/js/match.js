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
                    layer.close(index);
                    crt_row.statuscode=100
                    var post_data=[{fun:'save_row',row:crt_row}]
                    cfg.show_load()
                    ex.post('/d/ajax',JSON.stringify(post_data),function(resp){

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
                //if(crt_row.statuscode !=100){
                //    cfg.showMsg('请先结束比赛')
                //    return
                //}

                var mt = /(\d+):(\d+)/.exec(crt_row.matchscore)
                if(mt){
                    var home_score= mt[1]
                    var away_score=mt[2]
                }else{
                    var home_score= 0
                    var away_score=0
                }

                var row={
                    matchid:crt_row.matchid,
                    _matchid_label:crt_row._matchid_label,
                    home_score:home_score,
                    away_score:away_score,
                    //statuscode:crt_row.statuscode
                }
                pop_fields_layer(row,kws.fields_ctx,function(e){
                    alert(e.new_row)
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

var produce_match_outcome={
    mounted:function(){
        var self=this
        ex.assign(this.op_funs, {
            produce_match_outcome: function (kws) {

                var index = layer.confirm('确认手动结算?',function(index){
                    layer.close(index);

                    var post_data = [{fun:'produce_match_outcome',row:self.row}]
                    cfg.show_load()
                    ex.post('/d/ajax/maindb',JSON.stringify(post_data),function(resp){
                        cfg.hide_load()
                        cfg.showMsg(resp.produce_match_outcome.Message)
                    })
                })

            }
        })

    }
}

window.match_logic = match_logic
window.produce_match_outcome = produce_match_outcome