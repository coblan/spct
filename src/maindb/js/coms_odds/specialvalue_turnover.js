
var odds_multi_line = {
    props:['rowData','field','index'],
    data:function(){
        return {
            crt_row:{}
        }
    },
    template:`<div >
        <div v-for="row in rows" style="position: relative" @click="show_editor(row)">
        <div v-text="show_turnover(row)"></div>
        <!--<input ref="editor" v-show="is_show_editor(row)" v-model="row[field]" type="text" style="position: absolute;top:0;left:0;right:0;bottom: 0">-->
        </div>
        <!--<span v-text="rowData.FavTurnover"> </span>-->
        <!--<span v-text="rowData.UnderTurnover"></span>-->
    </div>`,
    //

    methods:{
        show_editor:function (row){
            this.crt_row=row
            var self=this
            Vue.nextTick(function(){
                $(self.$el).find('input').focus()
            })
        },
        is_show_editor:function(row){
            return this.crt_row == row
        },
        show_turnover:function(row){
            return row.FavTurnover - row.UnderTurnover
        },
    },
    computed:{

        rows:function(){
            return this.rowData.odds
        }
    }

}

Vue.component('com-odds-special-turnover',odds_multi_line)


