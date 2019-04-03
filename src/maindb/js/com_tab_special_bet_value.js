require('./scss/com_tab_special_bet_value.scss')

var com_tab_special_bet_value={
    props:['tab_head','par_row'],
    data:function(){
        var self=this
        var vc = this
        this.childStore = new Vue({
            methods:{
                refresh:function(){
                    vc.getRowData()
                },
                save:function(){
                    vc.save()
                },
                filter_name:function(head){
                    vc.market_filter_name = head.value
                }
            }
        })

        return {
            match_opened:true,
            oddstype:[],
            specialbetvalue:[],
            market_filter_name:'',
            ops:this.tab_head.ops || [],
        }
    },
    //mixins:[mix_fields_data],
    template:`<div class="com_tab_special_bet_value" style="position: absolute;top:0;right:0;left:0;bottom: 0;">
    <div class="oprations">
                <component style="padding: 0.5em;" v-for="op in ops" :is="op.editor" :ref="'op_'+op.fun" :head="op" @operation="on_operation($event)"></component>
    </div>
        <div style="text-align: center;">
            <span v-text="par_row.matchdate"></span>/
            <span v-text="par_row.matchid"></span>/
            <span v-text="par_row.team1zh"></span>
            <span>VS</span>
            <span v-text="par_row.team2zh"></span>

        </div>
        <div class="content-wrap">
            <div class="inn-wrap">
            <!--<div class="box">-->

                    <!--<el-switch-->
                          <!--v-model="match_opened"-->
                          <!--active-color="#13ce66"-->
                          <!--inactive-color="#ff4949">-->
                    <!--</el-switch>-->
                    <!--<span>整场比赛</span>-->
                <!--</div>-->
                <div class="box">
                    <div style="text-align: center">
                        <b>玩法</b>
                    </div>
                    <div class="box-content">
                          <div v-for="odtp in normed_oddstype" >
                            <el-switch
                                  v-model="odtp.opened"
                                  active-color="#13ce66"
                                  inactive-color="#ff4949">
                            </el-switch>
                            <span v-text="odtp.name"></span>
                        </div>
                    </div>

                </div>
                <div class="box"  style="width: 500px;overflow-x: hidden">
                    <div style="text-align: center">
                        <b>盘口</b>
                    </div>
                      <div class="box-content">
                            <table class="table">
                            <tr>
                            <td></td>
                            <td>玩法名</td>
                            <td>盘口值</td>
                            <td>盘口名</td>
                            </tr>
                            <tr v-for="spbet in normed_specailbetvalue" :class="spbet.cls">
                                <td>
                                <el-switch
                                      v-model="spbet.opened"
                                      active-color="#13ce66"
                                      inactive-color="#ff4949">
                                </el-switch>
                                </td>
                                <td>
                                 <span v-text="spbet.marketname"></span>
                                </td>
                                <td>
                                <span v-text="spbet.specialbetvalue"></span>
                                </td>
                                <td>
                                  <span v-text="spbet.specialbetname"></span>
                                </td>

                                <!--<span v-text="spbet.specialbetvalue"></span>-->
                                 <!--<span v-text="spbet.oddsid"></span>-->
                            </tr>
                            </table>

                    </div>
                </div>
            </div>


        <div>

    </div>

    </div>


    </div>`,
    mounted:function(){
        this.getRowData()
    },
    computed:{
        normed_oddstype:function(){
            if(!this.match_opened){
                return []
            }else{
                if(this.market_filter_name){
                    var ls = ex.filter(this.oddstype,(market)=>{
                        return market.name.indexOf(this.market_filter_name)!=-1
                    })
                }else{
                    var ls=this.oddstype
                }

                return ex.sortOrder(ls,'sort')
            }
        },
        normed_specailbetvalue:function(){
            if(!this.match_opened){
                return []
            }
            var self=this

            if(this.market_filter_name){
                var filtered_list = ex.filter(this.specialbetvalue,(market)=>{
                    return market.name.indexOf(this.market_filter_name)!=-1
                })
            }else{
                var filtered_list=this.specialbetvalue
            }

            var ordered_spval = ex.filter(filtered_list,function(spval){
                var market = ex.findone(self.oddstype,{marketid:spval.marketid})
                spval.sort=market.sort
                return market.opened
            })
            var sorted_spval = ex.sortOrder(ordered_spval,'name')
            var sorted_spval = ex.sortOrder(sorted_spval,'sort')

            var crt=''
            var cls='oven'
            ex.each(sorted_spval,function(spval){
                var name =spval.name.split(' ')[0]
                if(name !=crt){
                    crt=name
                    cls = cls=='oven'?'even':'oven'
                }
                spval.cls=cls
            })

            return sorted_spval
        }
    },
    methods:{
        on_operation:function(op){
            this.childStore[op.fun](op)
        },
        save:function(){
            var self=this
            var data={
                    matchid:this.par_row.matchid,
                    //match_opened:this.match_opened,
                    markets:this.oddstype,
                    specialbetvalue:this.specialbetvalue,
            }
            cfg.show_load()
            ex.director_call(this.tab_head.save_director,data,function(resp){
                    if(resp.success==true){
                        cfg.hide_load(2000,'封盘成功')
                       setTimeout(function(){
                           self.getRowData()
                       },10)
                    }
            })
        },
        on_show:function(){

        },
        getRowData:function(){
            var self=this
            cfg.show_load()
            ex.director_call(this.tab_head.update_director,{matchid:this.par_row.matchid},function(resp){
                    self.match_opened=resp.match_opened
                    self.oddstype= resp.markets
                    self.specialbetvalue= resp.specialbetvalue
                    cfg.hide_load()
            })

        }
    }
}
Vue.component('com-tab-special-bet-value',com_tab_special_bet_value)