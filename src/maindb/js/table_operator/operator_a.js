var op_a = {
    props:['head'],
    template:` <a class="clickable" @click="operation_call()" :disabled="!enable" v-text="head.label" ></a>`,
    data:function(){
        return {
            enable:true
        }
    },
    methods:{
        operation_call:function(){
            this.$emit('operation',this.head.name)
        },
        set_enable:function(yes){
            this.enable= yes
        }
    }
}
Vue.component('com-op-a',op_a)