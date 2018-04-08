/*
 Argments:
 ==========

 nums = ['1','...','6_a','7','8','...','999']

 Events:
 =======

 goto_page,num

 */

Vue.component('paginator',{
    props:['nums','crt','set'],
    data:function(){
        return {
            input_num:this.crt ||1,
        }
    },

    methods:{
        goto_page:function (num) {
            if (!isNaN(parseInt(num))){
                this.$emit('goto_page',num)
            }
        }
    },
    template:ex.template(`
    <div class="paginator">
    <ul class="pagination page-num">
    <li v-for='num in nums' track-by="$index" :class='{"clickable": !isNaN(parseInt(num))}' @click='goto_page(num)'>
    <span v-text='!isNaN(parseInt(num))? parseInt(num):num' :class='{"active":parseInt(num) ==parseInt(crt)}'></span>
    </li>
    </ul>
    <div v-if="set=='jump'" class="page-input-block">
        <input type="text" v-model="input_num"/>
        <button type="button" class="btn btn-success btn-xs" @click="goto_page(input_num)">{jump}</button>
    </div>
    </div>
    `,ex.trList(['jump']))
})