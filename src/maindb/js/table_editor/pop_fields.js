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
            var self=this
            var pop_id = new Date().getTime()
            eventBus.$on('pop-win-'+pop_id,function(kws){
                if(kws.name =='after_save'){
                    var fun = after_save[self.head.after_save.fun]
                    fun(self,kws.new_row,kws.old_row)
                }
            })

            var ops = this.head.ops

            var fun= get_row[this.head.get_row.fun]
            var kws= this.head.get_row.kws
            fun(function(pop_row){
                pop_fields_layer(pop_row,self.head.fields_heads,ops,pop_id)
            },this.rowData,kws)

        }

    }
}
Vue.component('com-table-pop-fields',pop_fields)


var get_row={
    use_table_row:function(callback,row,kws){
        callback(row)
    },
    get_table_row:function(callback,row,kws){
        var cache_row=ex.copy(row)
        callback(cache_row)
    },
    get_with_relat_field:function(callback,row,kws){
        var model_name=kws.model_name
        var relat_field = kws.relat_field

        var dc ={fun:'get_row',model_name:model_name}
        dc[relat_field] = row[relat_field]
        var post_data=[dc]
        cfg.show_load()
        ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
            cfg.hide_load()
            callback(resp.get_row)
        })

    }
}

var after_save={
    do_nothing:function(self,new_row,old_row,table){
        // һ���Ӧ use_table_row���������Ϊ���ʱ��table_row�Ѿ��Զ��������ˡ�
        //alert('fuck 111')
    },
    update_or_insert:function(self,new_row,old_row){
        self.$emit('on-custom-comp',{name:'update_or_insert',new_row:new_row,old_row:old_row})
        //if(! old_row.pk) {
        //    table.rows.splice(0, 0, new_row)
        //}else{
        //    ex.assign(table.rowData,new_row)
        //}


    }
}