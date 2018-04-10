var pop_fields={
    template:'<span v-text="rowData[field].label" @click="edit_me()" class="clickable"></span>',
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
            var id = new Date().getTime()
            var pk = this.rowData[this.field].pk
            var model_name = this.head.model_name
            var ops = this.head.ops
            self.opened_layer_indx = layer.open({
                type: 1,
                area: ['700px', '400px'],
                shadeClose: true, //点击遮罩关闭
                content:`<div id="fields-pop-${id}" style="height: 100%;">
                    <com-pop-fields @del_success="on_del()" @sub_success="on_sub_success($event)"
                    :row="row" :heads="fields_heads" :ops="ops"></com-pop-fields>
                </div>`
            });
            //var copy_fields_heads = ex.copy(fields_heads)
            new Vue({
                el:'#fields-pop-'+id,
                data:{
                    row:{},
                    fields_heads:this.head.fields_heads,
                    pk:pk,
                    ops:ops
                },
                mounted:function(){
                    var self=this
                    cfg.show_load()
                    var post_data=[{fun:'get_row',pk:this.pk,model_name:model_name}]
                    ex.post('/d/ajax',JSON.stringify(post_data),function(resp){
                        self.row = resp.get_row
                        cfg.hide_load()
                    })
                },
                methods:{
                    on_sub_success:function(event){
                        // 将新建的row 插入到表格中
                        var old_row = event.old_row
                        var new_row=event.new_row
                        if(! old_row.pk){
                            self.rows.splice(0,0,new_row)
                        }else {
                            ex.assign(row,new_row)
                        }
                    },
                    on_del:function(){
                        ex.remove(self.rows,row)
                        layer.close(self.opened_layer_indx)
                    },
                }
            })
        },
    }
}
Vue.component('com-table-pop-fields',pop_fields)