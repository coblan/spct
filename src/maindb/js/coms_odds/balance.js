
var bool_shower = {
    props:['rowData','field','index'],
    template:`<div >
        <span v-text="minus_value"></span>
    </div>`,
    computed:{
        minus_value:function(){
            return (this.rowData.FavTurnover - this.rowData.UnderTurnover).toFixed(2)
        }
    }

}

Vue.component('com-odds-balance',bool_shower)


