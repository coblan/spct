
var odds_multi_line = {
    props:['rowData','field','index'],
    template:`<div >
        <div v-for="row in rows" >
<com-odds-status-check-btn :row="row"></com-odds-status-check-btn>

        </div>
    </div>`,

    computed:{
        rows:function(){
            return this.rowData.odds
        },

    }

}

Vue.component('com-odds-status',odds_multi_line)

Vue.component('com-odds-status-check-btn',{
    props:['row'],
    template:`<el-switch
              v-model="is_true"
              active-color="#13ce66"
              inactive-color="#ff4949">
        </el-switch>`,
    computed: {
        is_true: {
            get: function () {
                return this.row.LineStatus == 1
            },
            set: function (newValue) {
                if (newValue) {
                    this.row.LineStatus = 1
                } else {
                    this.row.LineStatus = 0
                }
            }
        },
    }
})


