Vue.component('com-pop-fields',{
    props:['row','heads','ops'],
    mixins:[mix_fields_data,mix_nice_validator],

    methods:{
        before_save:function(){
            eventBus.$emit('sync_data')
            if(this.nice_validator.isValid()){
                return 'continue'
            }else{
                return 'break'
            }
        },
        after_save:function(new_row){
            this.$emit('sub_success',{new_row:new_row,old_row:this.row})
            ex.assign(this.row,new_row)
        },
        del_row:function(){
            var self=this
            layer.confirm('真的删除吗?', {icon: 3, title:'确认'}, function(index){
                layer.close(index);
                var ss = layer.load(2);
                var post_data = [{fun:'del_rows',rows:[self.row]}]
                $.post('/d/ajax',JSON.stringify(post_data),function(resp){
                    layer.close(ss)
                    self.$emit('del_success',self.row)
                })
            });
        }

    },
    template:`<div class="flex-v" style="margin: 0;height: 100%;">
    <div>
        <component v-for="op in ops" :is="op.editor" @operation="on_operation(op)" :head="op"></component>
        <!--<button @click="save()">保存</button>-->
        <!--<button @click="del_row()" v-if="row.pk">删除</button>-->
    </div>
    <div class = "flex-grow" style="overflow: scroll;margin: 0;">
        <div class="field-panel msg-hide" >
            <field  v-for="head in heads" :key="head.name" :head="head" :row="row"></field>
        </div>
    </div>
     </div>`,
    data:function(){
        return {
            fields_kw:{
                heads:this.heads,
                row:this.row,
                errors:{},
            },
        }
    }
})