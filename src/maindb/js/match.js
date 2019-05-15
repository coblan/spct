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

function manul_outcome_panel_ctx(row,kws,sp_id){
    var ctx_dict = kws.ctx_dict
    var play_type = kws.play_type
    var row_adapt = kws.row_adapt

    var type = type_find(play_type,sp_id)
    var cus_ctx = ex.copy(ctx_dict[type])
    cus_ctx.row=ex.copy(row)
    cus_ctx.row.meta_type='manul_outcome'
    if(row_adapt[type]){

        ex.eval( row_adapt[type],{row:cus_ctx.row,adaptor:row_adaper})
    }
    return cus_ctx
}



var row_adaper={
    parse_score:function (row){
        var crt_row = row
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

        var ex_row={
            home_score:home_score,
            away_score:away_score,
            home_half_score:home_half_score,
            away_half_score:away_half_score,
        }
        ex.assign(row,ex_row)
    }
}



window.manul_outcome_panel_express_parse = manul_outcome_panel_express_parse
window.manul_outcome_panel_ctx=manul_outcome_panel_ctx

// 只有这个函数有用，其他都无用了。
window.out_come_save=function(rows,matchid){
    var maped_row =[]

    ex.each(rows,function(row){
        if(row.outcome){
            let dc ={pk:row.pk}
            ex.assign(dc,row.outcome)
            //row.outcome.pk=row.pk
            maped_row.push(dc)
        }
    })
    return new Promise((resolve,reject)=>{
        if(maped_row.length >0){
            cfg.show_load()
    
            ex.director_call('out_com_save',{rows:maped_row,matchid:matchid}).then(res=>{
                cfg.hide_load(2000)
                resolve()
            })
        }else{
            cfg.showError('请至少填写一条结算信息!')
        }
    })

}


Vue.component('com-outcome-score',{
    props:['ctx'],
    template:`<div class="com-outcome-score flex-v" style="margin: 0;height: 100%;">
    <div class = "flex-grow" style="overflow: auto;margin: 0;">
        <div style="width: 40em;margin: auto;">
              <table class="field-panel msg-bottom" style="display: inline-block;">
                    <tr><td></td> <td >主队</td><td>客队</td></tr>
                    <tr v-for="dh in doubleHeads">
                         <td style="padding: 1em 1em" v-text="dh[0].label"></td>
                         <td>
                            <div class="field-input" style="position: relative">
                                <component :is="dh[0].editor"
                                     @field-event="$emit('field-event',$event)"
                                     :head="dh[0]" :row="row"></component>
                            </div>
                         </td>

                         <td>
                            <div class="field-input" style="position: relative">
                                <component :is="dh[1].editor"
                                     @field-event="$emit('field-event',$event)"
                                     :head="dh[1]" :row="row"></component>
                            </div>
                         </td>
                     </tr>
              </table>
        </div>
      <div style="height: 1em;">
      </div>
    </div>
     <div style="text-align: right;padding: 8px 3em;">
        <component v-for="op in ctx.ops" :is="op.editor" :head="op"></component>
    </div>

    </div>`,
    data:function(){
        var self=this
        var childStore=new Vue({
            data:function(){
                return {
                    vc:self
                }
            },
            methods:{
                record_row:function(){
                    //this.vc.ctx.row.outcome = this.vc.row
                    var pp  = JSON.stringify(this.vc.row)
                    this.vc.$emit('finish',pp)
                },

            }
        })
        var row = {}
        ex.each(this.ctx.heads,function(head){
            row[head.name] = ''
        })
        if(this.ctx.row.outcome){
            var org_outcome  = JSON.parse(this.ctx.row.outcome)
            ex.vueAssign(row ,org_outcome)
        }
        return {
            row:row,
            childStore:childStore,
        }
    },
    mounted:function(){
        if(! this.ctx.row.outcome && this.ctx.init_express){
            ex.eval(this.ctx.init_express,{par_row:this.ctx.par_row,row:this.row})
        }
    },
    computed:{
        doubleHeads:function(){
            var ls =[]
            var pair=[]
            var count =0
            ex.each(this.ctx.heads,function(head){
                pair.push(head)
                if(count==1){
                    count=0
                    ls.push(pair)
                    pair=[]
                }else{
                    count+=1
                }
            })
            return ls
        }
    },

})




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
        mixins:[mix_fields_data,mix_nice_validator,produce_match_outcome],

        data:function(){
            return {
                //ops:this.option.ops,
                row:this.ctx.row,
                heads:this.ctx.heads,
                ops:this.ctx.ops,
            }
        },
    computed:{
        doubleHeads:function(){
            var ls =[]
            var pair=[]
            var count =0
            ex.each(this.heads,function(head){
                pair.push(head)
                if(count==1){
                    count=0
                    ls.push(pair)
                    pair=[]
                }else{
                    count+=1
                }
            })
            return ls
        }
    },
        methods:{
            submit:function(){
                var self=this
                if(!self.isValid()){
                    return
                }
                var msg=''

                var index = layer.confirm(`确认手动结算${msg}?`,function(index){
                    layer.close(index)
                    self.save()

                })
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
              <table class="field-panel msg-bottom" style="display: inline-block;">
                    <tr><td></td> <td >主队</td><td>客队</td></tr>
                    <!--<tr v-for="head in heads">-->
                        <!--<td>-->
                                <!--<div class="field-input" style="position: relative">-->
                                <!--<component :is="head.editor"-->
                                     <!--@field-event="$emit('field-event',$event)"-->
                                     <!--:head="head" :row="row"></component>-->
                                <!--</div>-->
                        <!--</td>-->
                    <!--</tr>-->
                    <tr v-for="dh in doubleHeads">
                         <td style="padding: 1em 1em" v-text="dh[0].label"></td>
                         <td>
                            <div class="field-input" style="position: relative">
                                <component :is="dh[0].editor"
                                     @field-event="$emit('field-event',$event)"
                                     :head="dh[0]" :row="row"></component>
                            </div>
                         </td>

                         <td>
                            <div class="field-input" style="position: relative">
                                <component :is="dh[1].editor"
                                     @field-event="$emit('field-event',$event)"
                                     :head="dh[1]" :row="row"></component>

                            </div>
                         </td>
                     </tr>

                     <!--<tr>-->
                         <!--<td style="padding: 1em 1em">半场得分</td><td>-->
                         <!--<input type="text" v-model="row.home_half_score" data-rule="integer(+0);length(~6)"></td>-->
                         <!--<td><input type="text" v-model="row.away_half_score" data-rule="integer(+0);length(~6)"></td>-->
                     <!--</tr>-->

                    <!--<tr>-->
                        <!--<td style="padding: 1em 1em">全场得分</td><td><input type="text" v-model="row.home_score" data-rule="integer(+0);length(~6)"></td>-->
                        <!--<td><input type="text" v-model="row.away_score" data-rule="integer(+0);length(~6)"></td>-->
                    <!--</tr>-->

              </table>
        </div>


        <!--<div class="field-panel msg-hide" >-->
            <!--<field  v-for="head in heads" :key="head.name" :head="head" :row="row"></field>-->
        <!--</div>-->
      <div style="height: 1em;">
      </div>
    </div>
     <div style="text-align: right;padding: 8px 3em;">
        <component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>
    </div>
     </div>`,

 }


Vue.component('com-form-produceMatchOutcomePanel',produceMatchOutcomePanel)


var produceBasketballMatchOutcomePanel={
    mixins:[produceMatchOutcomePanel],
    methods:{
        submit:function(){
            var self=this
            if(!self.isValid()){
                return
            }
            self.row.PeriodType=2

            var msg=''

            var index = layer.confirm(`确认手动结算${msg}?`,function(index){
                layer.close(index)
                self.save()
            })
        }
    }
}

window.produce_match_outcome = produce_match_outcome
window.produceMatchOutcomePanel=produceMatchOutcomePanel