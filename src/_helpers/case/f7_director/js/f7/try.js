Vue.component('com-fuck-try',{
    props:['name'],
    template:`<span v-text="name" @click="back()"></span>`,
    methods:{
        back:function(){
            this.$parent.callback()
            history.back()
        }
    }

})