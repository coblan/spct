
var odds_multi_line = {
    props:['rowData','field','index'],
    template:`<div >
        <div v-for="row in rows" >
        <input type="checkbox">
        </div>
    </div>`,
    
    computed:{
        rows:function(){
            return this.rowData.odds
        }
    }

}

Vue.component('com-odds-switch-checkbox',odds_multi_line)


