
var switch_to_tab = {
    props:['rowData','field','index'],
    template:'<span v-text="rowData[field]" @click="goto_tab()" class="clickable"></span>',
    created:function(){
        // find head from parent table
        var table_par = this.$parent
        while (true){
            if (table_par.heads){
                break
            }
            table_par = table_par.$parent
            if(!table_par){
                break
            }
        }
        var head  = ex.findone(table_par.heads,{name:this.field})
        this.head = head
    },
    methods:{
        goto_tab:function(){
            this.$emit('on-custom-comp',
                {name:'switch_to_tab',
                tab_name:this.head.tab_name,
                row:this.rowData})
        }
    }
}

Vue.component('com-table-switch-to-tab',switch_to_tab)
