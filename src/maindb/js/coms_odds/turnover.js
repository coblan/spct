
var bool_shower = {
    props:['rowData','field','index'],
    template:`<div style="position: absolute;top:0;left:0;right:0;bottom:0;overflow: hidden">
        <table width= "100% " height= "100% " >
        <tr style="height: 1em;background-color: transparent;"><td width="50%">Home</td><td>Away</td></tr>
        <tr style="background-color: transparent;"><td><span v-text="rowData.FavTurnover"></span></td><td><span v-text="rowData.UnderTurnover"></span></td></tr>
        </table>
    </div>
    `,
    computed:{
    }

}

Vue.component('com-odds-turnover',bool_shower)


