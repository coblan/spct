
var odds_multi_line = {
    props:['rowData','field','index'],
    data:function(){
        return {
            plus_value:0.01
        }
    },
    template:`<div >
        <div v-for="row in rows" >
        <button type="button" class="btn btn-default btn-xs"><i class="fa fa-plus"></i></button>
        <input  type="number" step="0.01" v-model="plus_value" style="width: 40px;height: 20px">
        <button type="button" class="btn btn-default btn-xs"><i class="fa fa-minus"></i></button>
        </div>
    </div>`,

    computed:{
        rows:function(){
            return this.rowData.odds
        }
    }

}

Vue.component('com-odds-plus',odds_multi_line)


