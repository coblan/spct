

var check_box={
    model: {
        prop: 'checked',
        event: 'change',
    },
    props:['value','checked'],
    methods:{
        on_click:function(){
            $(this.$el).find('input').click()
            this.$emit('change',this.checked)
        },
    },
    data:function(){
        var checked = this.checked || []
        return {
            inn_checked:checked,
        }
    },
    watch:{
        inn_checked:function(v){
            this.$emit('change',v)
        },
        checked:function(v){
            this.inn_checked=v
        }
    },
    computed:{
        is_checked:function(){
            if(this.value){
                return this.inn_checked.indexOf(this.value)!=-1
            }else{
                return this.inn_checked
            }
        }
    },
    template:` <span class="com-checkbox" @click="on_click()">
                <input type="checkbox" :value="value" v-model='inn_checked' style="display: none"/>
                  <i class="fa fa-check-circle" aria-hidden="true" v-if='is_checked' style="color: #009926"></i>
                  <i class="fa fa-circle-thin" aria-hidden="true" v-else></i>
              </span>`
}
Vue.component('com-check-box',check_box)