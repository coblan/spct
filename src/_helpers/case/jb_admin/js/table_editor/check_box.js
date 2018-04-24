
var check_box = {
    props:['rowData','field','index'],
    template:`<div ><input style="width: 100%" @change="on_changed()" type="checkbox" v-model="rowData[field]"></div>`,
    data:function(){
        return {
        }
    },
    methods:{
        on_changed:function(){
            this.$emit('on-custom-comp',{name:'row_changed',row:this.rowData})
        }
    }
}

Vue.component('com-table-checkbox',check_box)
