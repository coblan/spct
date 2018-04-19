
var picture = {
        props:['rowData','field','index'],
        template:`<span>
        <img @click="open()" :src="rowData[field]" alt="" height="96px" style="cursor: pointer;">
        </span>`,
    methods:{
        open:function(){
            window.open(this.rowData[this.field])
        }
    }
    }

Vue.component('com-table-picture',picture)
