function  type_find(play_type,sp_id){
    for(var k in play_type){
        var types = play_type[k]
        if(ex.isin(sp_id,types)){
            return k
        }
    }
}


function manul_outcome_panel_express_parse(panel_map,play_type,sp_id){
    var type =type_find(play_type,sp_id)
    return panel_map[type]
}

function manul_outcome_panel_ctx(row,ctx_dict,play_type,sp_id){
    var type = type_find(play_type,sp_id)
    var cus_ctx = ex.copy(ctx_dict[type])
    cus_ctx.row=row
    return cus_ctx

}

window.manul_outcome_panel_express_parse = manul_outcome_panel_express_parse
window.manul_outcome_panel_ctx=manul_outcome_panel_ctx

var manual_end_money=function(self,kws){
    //if(self.selected.length!=1){
    //    cfg.showMsg('请选择一条记录')
    //    return
    //}

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
    var mt = /(\d+):(\d+)/.exec(crt_row.period1score)
    if(mt){
        var home_half_score= mt[1]
        var away_half_score=mt[2]
    }else{
        var home_half_score= ''
        var away_half_score=''
    }

    var row={
        matchid:crt_row.matchid,
        _matchid_label:crt_row._matchid_label,
        home_score:home_score,
        away_score:away_score,
        home_half_score:home_half_score,
        away_half_score:away_half_score,

        //statuscode:crt_row.statuscode
    }

    var ctx=ex.copy(kws.fields_ctx)
    ctx.row=row

     cfg.pop_middle('com-form-produceMatchOutcomePanel',ctx,function(new_row){
        ex.vueAssign(self.selected[0],new_row)

    })
}

window.manual_end_money=manual_end_money

var produce_match_outcome={
    mounted:function(){
        var self=this
        ex.assign(this.op_funs, {
            produce_match_outcome: function (kws) {
                //
                if(!self.isValid()){
                    return
                }
                //var rt =ex.vueBroadCall(self.$parent,'isValid')
                //for(var i=0;i<rt.length;i++){
                //    if(!rt[i]){
                //        return
                //    }
                //}
                var half=false
                var full=false
                if(self.row.home_half_score && self.row.away_half_score){
                    half=true
                }
                if(self.row.home_score && self.row.away_score){
                    full = true
                }
                var msg=''
                if( !half && !full ){
                    cfg.showError('请至少完成一行数据填写！')
                    return
                }
                if(half && full){
                    msg='【上半场】&【全场】'
                    if(parseInt(self.row.home_score) < parseInt(self.row.home_half_score) || parseInt(self.row.away_score) < parseInt(self.row.away_half_score)){
                        cfg.showError('全场得分不能少于半场得分，请纠正后再提交！')
                        return
                    }
                    self.row.PeriodType=2
                }else{
                    if(half){
                        msg='【上半场】'
                        self.row.PeriodType=1
                    }else {
                        msg='【全场】'
                        self.row.PeriodType=0
                    }
                }


                var index = layer.confirm(`确认手动结算${msg}?`,function(index){
                    layer.close(index)
                    //var post_data = [{fun:'produce_match_outcome',row:self.row}]
                    //cfg.show_load()
                    //ex.post('/d/ajax/maindb',JSON.stringify(post_data),function(resp){
                    //    cfg.hide_load()
                    //    cfg.showMsg(resp.produce_match_outcome.Message)
                    //    //ex.vueAssign(self.row,resp.produce_match_outcome.row)
                    //    self.$emit('submit-success',resp.produce_match_outcome.row)
                    //
                    //})
                    cfg.show_load()
                    var post_data={
                        row:self.row,
                        matchid:self.par_row
                    }
                    ex.director_call(self.ctx.produce_match_outcome_director,{row:self.row},function(resp){
                            cfg.hide_load()
                            cfg.showMsg(resp.Message)
                            //ex.vueAssign(self.row,resp.produce_match_outcome.row)
                            self.$emit('finish',resp.row)
                    })

                })

            }
        })

    }
}

var produceMatchOutcomePanel={
        props:['ctx'],
        //props:['row','heads','option'],
        mixins:[mix_fields_data,mix_nice_validator,produce_match_outcome],

        data:function(){

            var crt_row = this.ctx.row
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
            var mt = /(\d+):(\d+)/.exec(crt_row.period1score)
            if(mt){
                var home_half_score= mt[1]
                var away_half_score=mt[2]
            }else{
                var home_half_score= ''
                var away_half_score=''
            }

            var row={
                matchid:crt_row.matchid,
                _matchid_label:crt_row._matchid_label,
                home_score:home_score,
                away_score:away_score,
                home_half_score:home_half_score,
                away_half_score:away_half_score,

                //statuscode:crt_row.statuscode
            }

            return {
                //ops:this.option.ops,
                row:row,
                heads:this.ctx.heads,
                ops:this.ctx.ops,

                //fields_kw:{
                //    heads:this.heads,
                //    row:this.row,
                //    errors:{},
                //},
            }
        },
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
                 <input type="text" v-model="row.home_half_score" data-rule="integer(+0);length(~6)"></td>
                 <td><input type="text" v-model="row.away_half_score" data-rule="integer(+0);length(~6)"></td>
             </tr>

            <tr>
                <td style="padding: 1em 1em">全场得分</td><td><input type="text" v-model="row.home_score" data-rule="integer(+0);length(~6)"></td>
                <td><input type="text" v-model="row.away_score" data-rule="integer(+0);length(~6)"></td>
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

 }


Vue.component('com-form-produceMatchOutcomePanel',produceMatchOutcomePanel)

//window.match_logic = match_logic
window.produce_match_outcome = produce_match_outcome
window.produceMatchOutcomePanel=produceMatchOutcomePanel