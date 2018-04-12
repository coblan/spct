var  mix_table_base_op={
    data:function(){
        return {
            changed_rows:[]
        }
    },
    mounted:function(){
        this.$refs.op_save_changed_rows[0].set_enable(false)
        this.$refs.op_delete[0].set_enable(false)
    },
    watch:{
        changed_rows:function(v){
            this.$refs.op_save_changed_rows[0].set_enable(v.length != 0)
        },
        selected:function(v){
            this.$refs.op_delete[0].set_enable(v.length != 0)
        }
    },
    methods:{
        on_operation:function(operation){
            if(operation=='add_new'){
                this.add_new()
            }
            if(operation=='delete'){
                this.del_selected()
            }
            if(operation=='save_changed_rows'){
                this.save_rows(this.changed_rows)
                this.changed_rows=[]
            }
        },
    }
}

window.mix_table_base_op=mix_table_base_op