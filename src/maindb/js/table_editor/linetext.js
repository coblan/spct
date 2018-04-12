
var line_text = {
    props:['rowData','field','index'],
    template:`<div ><input @change="on_changed()" style="width: 100%" type="text" v-model="rowData[field]"></div>`,
    data:function(){
        return {
        }
    },
    methods:{
        on_changed:function(){
            this.$emit('on-custom-comp',{name:'row-changed',row:this.rowData})
        }
    }
}

Vue.component('com-table-linetext',line_text)
