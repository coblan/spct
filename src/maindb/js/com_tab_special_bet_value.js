require('./scss/com_tab_special_bet_value.scss')

var com_tab_special_bet_value={
    props:['tab_head','par_row'],
    data:function(){
        return {
            match_opened:true,
            oddstype:[],
            specialbetvalue:[],

            ops:this.tab_head.ops,
        }
    },
    mixins:[mix_fields_data],
    template:`<div class="com_tab_special_bet_value" style="position: absolute;top:0;right:0;left:0;bottom: 0;overflow: auto">
    <div style="text-align: center;">
        <span v-text="par_row.matchdate"></span>/
        <span v-text="par_row.matchid"></span>/
        <span v-text="par_row.team1zh"></span>
        <span>VS</span>
        <span v-text="par_row.team2zh"></span>

    </div>
    <div>
           <div class="box">

                <el-switch
                      v-model="match_opened"
                      active-color="#13ce66"
                      inactive-color="#ff4949">
                </el-switch>
                <span>整场比赛</span>
            </div>
            <div class="box">
                <div v-for="odtp in normed_oddstype">
                    <el-switch
                          v-model="odtp.opened"
                          active-color="#13ce66"
                          inactive-color="#ff4949">
                    </el-switch>
                    <span v-text="odtp.name"></span>
                     <!--<span v-text="odtp.oddstypeid"></span>-->
                      <!--<span v-text="odtp.oddstypegroup"></span>-->
                </div>
            </div>
            <div class="box">
                <div v-for="spbet in normed_specailbetvalue" :class="spbet.cls">
                    <el-switch
                          v-model="spbet.opened"
                          active-color="#13ce66"
                          inactive-color="#ff4949">
                    </el-switch>
                    <span v-text="spbet.name"></span>
                    <!--<span v-text="spbet.specialbetvalue"></span>-->
                     <!--<span v-text="spbet.oddsid"></span>-->
                </div>
            </div>

             <div class="oprations">
                <component style="padding: 0.5em;" v-for="op in ops" :is="op.editor" :ref="'op_'+op.fun" :head="op" @operation="on_operation(op)"></component>
            </div>
    </div>


    </div>`,
    mounted:function(){
        this.getRowData()

        var self=this
        ex.assign(this.op_funs,{
            refresh:function(){
                self.getRowData()
            },
            save:function(){
                self.save()
            }
        })
    },
    computed:{
        normed_oddstype:function(){
            if(!this.match_opened){
                return []
            }else{
                return ex.sortOrder(this.oddstype,'sort')
            }
        },
        normed_specailbetvalue:function(){
            if(!this.match_opened){
                return []
            }
            var self=this
            var ss = ex.filter(this.specialbetvalue,function(bet){
                var oddtyps = ex.findone(self.oddstype,{oddstypegroup:bet.oddstypegroup})
                bet.sort=oddtyps.sort
                return oddtyps.opened
            })
            var ss = ex.sortOrder(ss,'name')
            var ss = ex.sortOrder(ss,'sort')

            var crt=''
            var cls='oven'
            ex.each(ss,function(bet){
                var name =bet.name.split(' ')[0]
                if(name !=crt){
                    crt=name
                    cls = cls=='oven'?'even':'oven'
                }
                bet.cls=cls
            })

            return ss
        }
    },
    methods:{
        save:function(){
            var post_data=[{fun:'save_special_bet_value',
                matchid:this.par_row.matchid,
                match_opened:this.match_opened,
                oddstype:this.oddstype,
                specialbetvalue:this.specialbetvalue,
            }]
            cfg.show_load()
            ex.post('/d/ajax/maindb',JSON.stringify(post_data),function(resp){
                //cfg.hide_load(2000,'封盘成功')
                if(resp.save_special_bet_value.status=='success'){
                    cfg.hide_load(2000,'封盘成功')
                }else{
                    cfg.showMsg('error')
                }
            })
        },
        on_show:function(){

        },
        getRowData:function(){
            var self=this
            var post_data=[{fun:'update_special_bet_value',matchid:this.par_row.matchid}]
            cfg.show_load()
            ex.post('/d/ajax/maindb',JSON.stringify(post_data),function(resp){
                self.match_opened=resp.update_special_bet_value.match_opened
                self.oddstype= resp.update_special_bet_value.oddstype,
                self.specialbetvalue= resp.update_special_bet_value.specialbetvalue,
                cfg.hide_load()

            })

        }
    }
}
Vue.component('com-tab-special-bet-value',com_tab_special_bet_value)