Vue.component('com-field-op-btn',{
    props:['head'],
    template:`<button @click="$emit('operate')"><span v-text="head.label"></span></button>`,

})