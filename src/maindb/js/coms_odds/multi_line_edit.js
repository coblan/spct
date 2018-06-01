
var odds_multi_line = {
    props:['rowData','field','index'],
    data:function(){
        return {
            crt_row:{}
        }
    },
    template:`<div >
        <div v-for="row in rows" style="position: relative" @click="show_editor(row)">
        <div v-text="row[field]" ></div>
        <div style="position: absolute;top:0;left:0;right:0;bottom: 0">
            <input v-show="is_show_editor(row)" v-model="row[field]" @blur="on_blur(row)"  type="number" step="0.01"  style="width: 100%;text-align:center; height: 95%;">
        </div>
       </div>
    </div>`,
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
        on_blur:function(row){
            if(this.crt_row==row){
                this.crt_row={}
            }
        }
    },
    computed:{

        rows:function(){
            return this.rowData.odds
        }
    }

}

Vue.component('com-odds-multi-line-edit',odds_multi_line)


