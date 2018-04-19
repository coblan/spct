
var label_shower = {
    props:['rowData','field','index'],
    template:`<span v-text="rowData[label]"></span>`,
    data:function(){
        return {
            label:'_'+this.field+'_label'
        }
    }
}

Vue.component('com-table-label-shower',label_shower)
