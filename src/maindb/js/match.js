var manual_end_money=function(self,kws){
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
        var home_score= ''
        var away_score=''
    }

    var row={
        matchid:crt_row.matchid,
        _matchid_label:crt_row._matchid_label,
        home_score:home_score,
        away_score:away_score,
        //statuscode:crt_row.statuscode
    }
    pop_fields_layer(row,kws.fields_ctx,function(e){
        alert(new_row)
    })
}
window.manual_end_money=manual_end_money

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
                    var home_score= ''
                    var away_score=''
                }

                var row={
                    matchid:crt_row.matchid,
                    _matchid_label:crt_row._matchid_label,
                    home_score:home_score,
                    away_score:away_score,
                    //statuscode:crt_row.statuscode
                }
                pop_fields_layer(row,kws.fields_ctx,function(e){
                    alert(new_row)
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
            un_recommendate:function(kws){
                if(self.selected.length==0){
                    cfg.showMsg('请选择一些记录')
                    return
                }
                ex.each(self.selected,function(row){
                    row.isrecommend=false
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
            },
            un_livebet:function(kws){
                if(self.selected.length==0){
                    cfg.showMsg('请选择一些记录')
                    return
                }
                ex.each(self.selected,function(row){
                    row.livebet=false
                })
                var post_data=[{fun:'save_rows',rows:self.selected}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    cfg.hide_load(2000)
                })
            },
            show_match:function(kws){
                if(self.selected.length==0){
                    cfg.showMsg('请选择一些记录')
                    return
                }
                ex.each(self.selected,function(row){
                    row.ishidden=false
                })
                var post_data=[{fun:'save_rows',rows:self.selected}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    cfg.hide_load(2000)
                })
            },
            hide_match:function(){
                if(self.selected.length==0){
                    cfg.showMsg('请选择一些记录')
                    return
                }
                ex.each(self.selected,function(row){
                    row.ishidden=true
                })
                var post_data=[{fun:'save_rows',rows:self.selected}]
                cfg.show_load()
                ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    cfg.hide_load(2000)
                })
            },
            closeHandicap:function(){
                if(self.selected.length !=1){
                    cfg.showMsg('请选择一条记录')
                    return
                }
                self.op_funs.switch_to_tab({tab_name:'special_bet_value',row:self.selected[0]})
            },
            change_maxsinglepayout:function(){
                if(self.selected.length !=1){
                    cfg.showMsg('请选择一条记录')
                    return
                }

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
                var rt =ex.vueBroadCall(self.$parent,'isValid')
                for(var i=0;i<rt.length;i++){
                    if(!rt[i]){
                        return
                    }
                }

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

var produceMatchOutcomePanel={
        props:['row','heads','ops'],
        mixins:[mix_fields_data,mix_nice_validator],

        methods:{
            update_nice:function(){
                this.nice_validator= $(this.$el).validator({
                    msgClass:'n-bottom'
                });
            },
            isValid:function(){
                var nice_rt = this.nice_validator.isValid()
                return nice_rt
            },
            after_save:function(new_row){
                this.$emit('submit-success',new_row) //{new_row:new_row,old_row:this.row})
                ex.assign(this.row,new_row)
            },
        },
        template:`<div class="flex-v" style="margin: 0;height: 100%;">
    <div class = "flex-grow" style="overflow: auto;margin: 0;">


        <div style="width: 40em;margin: auto;">
        <div style="text-align: center;margin:1em;">
            <span v-text="row._matchid_label"></span>
        </div>
          <table style="display: inline-block;">
            <tr><td></td> <td >主队</td><td>客队</td></tr>

             <tr>
                 <td style="padding: 1em 1em">半场得分</td><td>
                 <input type="text" v-model="row.home_half_score" data-rule="required;integer(+0)"></td>
                 <td><input type="text" v-model="row.away_half_score" data-rule="required;integer(+0)"></td>
             </tr>

            <tr>
                <td style="padding: 1em 1em">全场得分</td><td><input type="text" v-model="row.home_score" data-rule="required;integer(+0)"></td>
                <td><input type="text" v-model="row.away_score" data-rule="required;integer(+0)"></td>
            </tr>

            <!--<tr><td>角球</td><td><input type="text" v-model="row.home_corner"></td><td><input type="text" v-model="row.away_corner"></td></tr>-->
            </table>
        </div>


        <!--<div class="field-panel msg-hide" >-->
            <!--<field  v-for="head in heads" :key="head.name" :head="head" :row="row"></field>-->
        <!--</div>-->
      <div style="height: 15em;">
      </div>
    </div>
     <div style="text-align: right;padding: 8px 3em;">
        <component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>
    </div>
     </div>`,
        data:function(){
            return {
                fields_kw:{
                    heads:this.heads,
                    row:this.row,
                    errors:{},
                },
            }
        }
 }



window.match_logic = match_logic
window.produce_match_outcome = produce_match_outcome
window.produceMatchOutcomePanel=produceMatchOutcomePanel