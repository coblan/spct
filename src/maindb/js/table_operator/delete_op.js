// 无用了。准备删除
var delete_op = {
    props:['name'],
    template:` <a class="clickable" @click="delete_op()" :disabled="!enable">删除</a>`,
    data:function(){
        return {
            enable:false
        }
    },
    methods:{
        delete_op:function(){
            this.$emit('operation',this.name)
        },
        set_enable:function(yes){
            this.enable= yes
        }
    }
}
Vue.component('com-op-delete',delete_op)