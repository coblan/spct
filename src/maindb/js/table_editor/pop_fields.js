var pop_fields={
    template:'<span v-text="rowData[field]" @click="edit_me()" class="clickable"></span>',
    props:['rowData','field','index'],
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
        if(table_par){
            var value = this.rowData[this.field]
            this.head  = ex.findone(table_par.heads,{name:this.field})
        }

    },
    methods:{
        edit_me:function(){
            this.open_layer()
        },
        open_layer:function(){

            //if(! trigger.head.use_table_row){
            //    var self=this
            //    cfg.show_load()
            //    var dc ={fun:'get_row',model_name:model_name}
            //    dc[relat_field] = trigger.rowData[relat_field]
            //    var post_data=[dc]
            //    ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
            //        self.row = resp.get_row
            //        cfg.hide_load()
            //    })
            //}

            var relat_field = this.head.relat_field
            var model_name = this.head.model_name
            var ops = this.head.ops
            if(this.head.use_table_row){
                pop_fields_layer(this.rowData,this.head.fields_heads,ops)
            }


        }

    }
}
Vue.component('com-table-pop-fields',pop_fields)