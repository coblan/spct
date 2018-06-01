
var odds_multi_line = {
    props:['rowData','field','index'],
    template:`<div >
        <div v-for="row in rows" style="position: relative" >
        <div v-text="row[field]"></div>
         </div>
    </div>`,

    methods:{
    },
    computed:{

        rows:function(){
            return this.rowData.odds
        }
    }

}

Vue.component('com-odds-multi-line',odds_multi_line)


