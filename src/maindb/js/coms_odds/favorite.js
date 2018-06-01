
var bool_shower = {
    props:['rowData','field','index'],
    template:`<div >
        <span v-text="label"></span>
    </div>`,
    computed:{
        label:function(){
            if( this.rowData.FavTurnover > this.rowData.UnderTurnover){
                return this.rowData.Team2ZH
            }else{
                return this.rowData.Team1ZH
            }
        }
    }

}

Vue.component('com-odds-favorite',bool_shower)


