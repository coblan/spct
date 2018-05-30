
var bool_shower = {
    props:['rowData','field','index'],
    template:`<span >
        <span v-text="rowData.FavTurnover"> </span>
        <span v-text="rowData.UnderTurnover"></span>
    </span>`,
    computed:{
    }

}

Vue.component('com-odds-turnover',bool_shower)


